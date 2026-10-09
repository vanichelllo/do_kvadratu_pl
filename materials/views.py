import os
import io
import base64
import hashlib
import hmac
import html
import ecdsa
import re
import requests
import json
import time
import random  # ДОДАНО ДЛЯ ГЕНЕРАЦІЇ ПРАКТИКИ
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Case, Q, When
from django.conf import settings
from django.core.cache import cache
from django.db.models import F

from users.forms import UserProfileForm
from .forms import StudentReportForm
from .models import StudyMaterial, Category, Cart, CartItem, Order, OrderItem, Question, AnswerOption, DiagnosticTopic, \
    MatchItem, PracticeAttempt, TutorStudentRequest, Review, StudentPresentation, QuestionError, StudentReport

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudyMaterialSerializer, PurchasedMaterialSerializer
import datetime
from django.utils import timezone
User = get_user_model()


def is_teacher(user):
    """Доступ до панелі вчителя. Поле role учень обирає сам у профілі,
    тому права даємо лише персоналу (is_staff / is_superuser, ставиться в адмінці)."""
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def to_int(value):
    """int із даних форми; None для порожніх або зіпсованих значень замість помилки 500."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_id_list(ids_str):
    """'1,2,3' -> [1, 2, 3]; некоректні шматки ігноруються."""
    return [i for i in (to_int(x) for x in (ids_str or '').split(',')) if i is not None]


def questions_in_order(q_id_list):
    if not q_id_list:
        return []
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(q_id_list)])
    return Question.objects.filter(id__in=q_id_list).prefetch_related('options', 'match_items').order_by(preserved_order)


def find_option(question, option_id):
    """Варіант відповіді лише з цього завдання, щоб не можна було підставити id правильного варіанта з іншого."""
    option_id = to_int(option_id)
    if option_id is None:
        return None
    return next((opt for opt in question.options.all() if opt.id == option_id), None)


def user_owns_material(user, material):
    """Пакет у покупки не додається — лише його вміст, тому пакет вважається купленим,
    коли куплено всі матеріали, що в нього входять."""
    if not user.is_authenticated:
        return False
    if material.is_bundle:
        included_ids = list(material.included_materials.values_list('id', flat=True))
        return bool(included_ids) and \
            user.purchased_materials.filter(id__in=included_ids).count() == len(included_ids)
    return user.purchased_materials.filter(id=material.id).exists()


def safe_back_url(request, fallback='cabinet'):
    """Повернення на попередню сторінку лише в межах нашого сайту."""
    referer = request.META.get('HTTP_REFERER', '')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()},
                                                   require_https=request.is_secure()):
        return referer
    return fallback


def diagnostic_test_view(request):
    # ==========================================
    # 1. ПЕРЕВІРКА ВІДПОВІДЕЙ (РЕЖИМ POST)
    # ==========================================
    if request.method == 'POST':
        question_ids_str = request.POST.get('question_ids', '')
        q_id_list = parse_id_list(question_ids_str)

        # === НОВЕ: Словник для збереження історії відповідей у БД ===
        saved_answers = {
            'q_choice': {},
            'q_match': {},
            'q_short': {},
            'question_ids': question_ids_str,
            'note': 'Вхідна діагностика НМТ'
        }

        # Витягуємо тільки ті запитання, які випали в тесті, зберігаючи порядок
        questions = questions_in_order(q_id_list)

        topics_stats = {}
        for topic in DiagnosticTopic.objects.all():
            topics_stats[topic.name] = {'topic': topic, 'correct': 0, 'total': 0}

        total_score = 0
        max_score = 0

        for question in questions:
            topic_name = question.topic.name if question.topic else None

            if question.question_type == 'CHOICE':
                if topic_name: topics_stats[topic_name]['total'] += 1
                max_score += 1
                user_answer = request.POST.get(f'question_{question.id}')

                # Зберігаємо відповідь для історії
                saved_answers['q_choice'][str(question.id)] = user_answer

                selected_option = find_option(question, user_answer)
                if selected_option and selected_option.is_correct:
                    total_score += 1
                    if topic_name: topics_stats[topic_name]['correct'] += 1

            elif question.question_type == 'MATCH':
                if topic_name: topics_stats[topic_name]['total'] += 3
                max_score += 3
                match_correct_count = 0

                saved_answers['q_match'][str(question.id)] = {}

                for item in question.match_items.all():
                    user_match_answer = request.POST.get(f'match_{item.id}')

                    # Зберігаємо відповідь для історії
                    saved_answers['q_match'][str(question.id)][str(item.id)] = user_match_answer

                    if to_int(user_match_answer) == item.correct_option_id:
                        match_correct_count += 1
                total_score += match_correct_count
                if topic_name: topics_stats[topic_name]['correct'] += match_correct_count

            elif question.question_type == 'SHORT':
                if topic_name: topics_stats[topic_name]['total'] += 2
                max_score += 2
                user_answer = request.POST.get(f'question_{question.id}')

                # Зберігаємо відповідь для історії
                saved_answers['q_short'][str(question.id)] = user_answer

                if user_answer:
                    user_clean = str(user_answer).strip().replace(',', '.')
                    correct_clean = str(question.correct_short_answer).strip().replace(',', '.')
                    if user_clean == correct_clean:
                        total_score += 2
                        if topic_name: topics_stats[topic_name]['correct'] += 2

        # === НОВЕ: ЗБЕРЕЖЕННЯ РЕЗУЛЬТАТУ В БАЗУ ===
        # Зберігаємо тільки якщо тест пройшов зареєстрований користувач
        if request.user.is_authenticated:
            # Створюємо технічний запис "уроку" для діагностики, якщо його ще немає
            diag_material, created = StudyMaterial.objects.get_or_create(
                title="Вхідне діагностичне тестування НМТ",
                defaults={
                    'price': 0,
                    'is_published': False,  # Не показуватиметься в магазині
                    'is_free': True
                }
            )
            # Записуємо фінальний результат
            PracticeAttempt.objects.create(
                user=request.user,
                material=diag_material,
                score=total_score,
                max_score=max_score,
                answers_json=saved_answers
            )
        # ==========================================

        weak_topics = [stat['topic'] for stat in topics_stats.values() if
                       stat['total'] > 0 and (stat['correct'] / stat['total']) * 100 < 50]

        recommended_materials = set()
        for topic in weak_topics:
            for mat in StudyMaterial.objects.filter(title__icontains=topic.name, is_published=True):
                recommended_materials.add(mat)

        percent_total = int((total_score / max_score) * 100) if max_score > 0 else 0

        def extract_number(text):
            match = re.match(r'^(\d+)', text)
            return int(match.group(1)) if match else 99999

        weak_topics.sort(key=lambda t: extract_number(t.name))
        recommendations_list = sorted(list(recommended_materials), key=lambda m: extract_number(m.title))
        sorted_stats = sorted(topics_stats.values(), key=lambda s: extract_number(s['topic'].name))

        return render(request, 'materials/diagnostic_results.html', {
            'total_score': total_score,
            'max_score': max_score,
            'percent_total': percent_total,
            'weak_topics': weak_topics,
            'topics_stats': sorted_stats,
            'recommendations': recommendations_list,
        })

    # ==========================================
    # 2. ГЕНЕРАЦІЯ НОВОГО ТЕСТУ НМТ (РЕЖИМ GET)
    # [Твій старий код залишається без змін...]
    # ==========================================
    # 2. ГЕНЕРАЦІЯ НОВОГО ТЕСТУ НМТ (РЕЖИМ GET)
    # ==========================================
    all_qs = Question.objects.select_related('topic').prefetch_related('options', 'match_items')

    alg_choice, geo_choice = [], []
    alg_match, geo_match = [], []
    alg_short, geo_short = [], []

    # Сортуємо всі завдання по кошиках
    for q in all_qs:
        topic_num = 999
        if q.topic and q.topic.name:
            match = re.match(r'^(\d+)', q.topic.name)
            if match:
                topic_num = int(match.group(1))

        # Логіка: <= 29 — Алгебра, інакше — Геометрія
        is_algebra = (topic_num <= 29)

        if q.question_type == 'CHOICE':
            alg_choice.append(q) if is_algebra else geo_choice.append(q)
        elif q.question_type == 'MATCH':
            alg_match.append(q) if is_algebra else geo_match.append(q)
        elif q.question_type == 'SHORT':
            alg_short.append(q) if is_algebra else geo_short.append(q)

    # Вибираємо випадкові завдання за пропорціями НМТ
    # Тести (10 алгебра, 5 геометрія)
    sel_choice = random.sample(alg_choice, min(10, len(alg_choice))) + random.sample(geo_choice,
                                                                                     min(5, len(geo_choice)))
    # Відповідності (2 алгебра, 1 геометрія)
    sel_match = random.sample(alg_match, min(2, len(alg_match))) + random.sample(geo_match, min(1, len(geo_match)))
    # Коротка відповідь (2 алгебра, 2 геометрія)
    sel_short = random.sample(alg_short, min(2, len(alg_short))) + random.sample(geo_short, min(2, len(geo_short)))

    # Перемішуємо завдання всередині своїх блоків
    random.shuffle(sel_choice)
    random.shuffle(sel_match)
    random.shuffle(sel_short)

    # Збираємо фінальний варіант: спочатку вибір, потім відповідність, потім коротка відповідь (як на НМТ)
    final_questions = sel_choice + sel_match + sel_short

    # Створюємо строку з ID вибраних завдань, щоб перевірити саме їх, коли учень натисне "Завершити"
    question_ids_str = ','.join(str(q.id) for q in final_questions)

    return render(request, 'materials/diagnostic_test.html', {
        'questions': final_questions,
        'question_ids_str': question_ids_str,
        'total_selected': len(final_questions)
    })


# ==========================================
# ПРАКТИКА НМТ ПІСЛЯ УРОКУ
# ==========================================
@login_required
def practice_session_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    if not (material.is_free or is_teacher(request.user) or user_owns_material(request.user, material)):
        messages.error(request, f"Практика доступна після придбання матеріалу «{material.title}».")
        if material.is_published:
            return redirect('material_detail', pk=material.id)
        return redirect('cabinet')

    if request.method == 'POST':
        total_score = 0
        max_score = 0
        results_data = []

        # Словник для збереження історії відповідей у БД
        saved_answers = {'q_choice': {}, 'q_match': {}, 'q_short': {}}

        question_ids_str = request.POST.get('question_ids', '')
        saved_answers['question_ids'] = question_ids_str

        questions = questions_in_order(parse_id_list(question_ids_str))

        for q in questions:
            q_result = {
                'question': q, 'type': q.question_type, 'is_correct': False,
                'user_answer': None, 'correct_answer': None, 'points_earned': 0, 'max_points': 0
            }

            if q.question_type == 'CHOICE':
                q_result['max_points'] = 1
                q_result['correct_answer'] = q.options.filter(is_correct=True).first()
                user_ans = request.POST.get(f'q_{q.id}')

                saved_answers['q_choice'][str(q.id)] = user_ans  # Зберігаємо для історії

                opt = find_option(q, user_ans)
                if opt:
                    q_result['user_answer'] = opt
                    if opt.is_correct:
                        total_score += 1
                        q_result['points_earned'] = 1
                        q_result['is_correct'] = True
                max_score += 1

            elif q.question_type == 'MATCH':
                q_result['max_points'] = 3
                q_result['matches'] = []
                match_points = 0
                saved_answers['q_match'][str(q.id)] = {}

                for item in q.match_items.all():
                    user_match = request.POST.get(f'match_{item.id}')
                    saved_answers['q_match'][str(q.id)][str(item.id)] = user_match  # Зберігаємо для історії

                    user_opt = find_option(q, user_match)
                    is_match_correct = user_opt is not None and user_opt.id == item.correct_option_id
                    if is_match_correct:
                        match_points += 1
                        total_score += 1

                    q_result['matches'].append({
                        'item': item, 'user_option': user_opt,
                        'correct_option': item.correct_option, 'is_correct': is_match_correct
                    })

                q_result['points_earned'] = match_points
                q_result['is_correct'] = (match_points == 3)
                max_score += 3

            elif q.question_type == 'SHORT':
                q_result['max_points'] = 2
                q_result['correct_answer'] = q.correct_short_answer
                user_ans = request.POST.get(f'q_{q.id}')

                saved_answers['q_short'][str(q.id)] = user_ans  # Зберігаємо для історії
                q_result['user_answer'] = user_ans

                if user_ans:
                    user_clean = str(user_ans).strip().replace(',', '.')
                    correct_clean = str(q.correct_short_answer).strip().replace(',', '.')
                    if user_clean == correct_clean:
                        total_score += 2
                        q_result['points_earned'] = 2
                        q_result['is_correct'] = True
                max_score += 2

            results_data.append(q_result)

        # Записуємо спробу в базу разом із JSON-історією
        PracticeAttempt.objects.create(
            user=request.user,
            material=material,
            score=total_score,
            max_score=max_score,
            answers_json=saved_answers
        )

        context = {
            'material': material,
            'total_score': total_score,
            'max_score': max_score,
            'results_data': results_data,
        }
        return render(request, 'materials/practice_results.html', context)

    # Режим GET залишається без змін
    match_current = re.match(r'^(\d+)', material.title)
    current_topic_num = int(match_current.group(1)) if match_current else 0
    raw_pool = Question.objects.filter(materials=material).prefetch_related('options', 'match_items', 'materials')

    safe_pool = []
    for q in raw_pool:
        is_safe = True
        for mat in q.materials.all():
            match_mat = re.match(r'^(\d+)', mat.title)
            mat_num = int(match_mat.group(1)) if match_mat else 0
            if mat_num > current_topic_num:
                is_safe = False
                break
        if is_safe:
            safe_pool.append(q)

    choice_pool = [q for q in safe_pool if q.question_type == 'CHOICE']
    match_pool = [q for q in safe_pool if q.question_type == 'MATCH']
    short_pool = [q for q in safe_pool if q.question_type == 'SHORT']

    q_choice = random.sample(choice_pool, min(10, len(choice_pool)))
    q_match = random.sample(match_pool, min(2, len(match_pool)))
    q_short = random.sample(short_pool, min(1, len(short_pool)))

    selected_questions = q_choice + q_match + q_short
    random.shuffle(selected_questions)

    if len(selected_questions) == 0:
        messages.info(request, "Для цієї теми ще не додано практичних завдань.")
        return redirect('cabinet')

    question_ids_str = ','.join(str(q.id) for q in selected_questions)
    context = {
        'material': material, 'q_choice': q_choice, 'q_match': q_match,
        'q_short': q_short, 'question_ids_str': question_ids_str, 'total_selected': len(selected_questions)
    }
    return render(request, 'materials/practice_session.html', context)


# ==========================================

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Обробка застосування/скасування промокоду
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'apply_promo':
            promo = request.POST.get('promo_code', '').strip().upper()
            if promo == Cart.PROMO_CODE:
                now = timezone.localdate()
                start_date, end_date = Cart.PROMO_START, Cart.PROMO_END

                if start_date <= now <= end_date:
                    cart.promo_code = promo
                    cart.save()
                    messages.success(request, "🎉 Промокод ВЧИТЕЛЬ успішно застосовано! Ваша знижка 40%.")
                elif now < start_date:
                    messages.error(request, f"⏳ Цей промокод почне діяти з {start_date:%d.%m}!")
                else:
                    messages.error(request, "❌ Термін дії цього промокоду минув.")
            else:
                messages.error(request, "❌ Невірний промокод.")

        elif action == 'remove_promo':
            cart.promo_code = None
            cart.save()
            messages.info(request, "Промокод скасовано.")

        return redirect('cart_detail')

    return render(request, 'materials/cart.html', {'cart': cart})

@login_required
@require_POST
def add_to_cart(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, is_published=True)

    if user_owns_material(request.user, material):
        messages.warning(request, "Ви вже придбали цей матеріал!")
        return redirect('cabinet')

    if material.is_free or material.price == 0:
        if material.is_bundle:
            for sub_material in material.included_materials.all():
                request.user.purchased_materials.add(sub_material)
            messages.success(request, f"🎉 Всі матеріали з пакету «{material.title}» додано до вашого кабінету!")
        else:
            request.user.purchased_materials.add(material)
            messages.success(request, f"🎉 Безкоштовний матеріал «{material.title}» додано до вашого кабінету!")
        return redirect('cabinet')

    cart, created = Cart.objects.get_or_create(user=request.user)

    if CartItem.objects.filter(cart=cart, material=material).exists():
        messages.info(request, "Цей матеріал вже є у вашому кошику.")
    else:
        CartItem.objects.create(cart=cart, material=material)
        messages.success(request, f"«{material.title}» додано до кошика! 🛒")

    return redirect('cart_detail')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, "Матеріал видалено з кошика.")
    return redirect('cart_detail')


class HomeView(TemplateView):
    template_name = 'materials/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general_reviews'] = Review.objects.filter(material__isnull=True, is_approved=True)
        return context


class AboutView(TemplateView):
    template_name = 'materials/about.html'


class OfferView(TemplateView):
    template_name = 'materials/offer.html'


class PrivacyView(TemplateView):
    template_name = 'materials/privacy.html'


def booking_view(request):
    return render(request, 'booking.html')


class MaterialListView(ListView):
    model = StudyMaterial
    template_name = 'materials/list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        queryset = StudyMaterial.objects.filter(is_published=True) \
            .select_related('category') \
            .prefetch_related('tags')

        filter_type = self.request.GET.get('type')
        if filter_type == 'free':
            queryset = queryset.filter(is_free=True)
        elif filter_type == 'bundle':
            queryset = queryset.filter(is_bundle=True)

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        materials_list = list(queryset)

        def get_number(material):
            match = re.match(r'^(\d+)', material.title)
            if match:
                return int(match.group(1))
            return 99999

        materials_list.sort(key=get_number)
        return materials_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class MaterialDetailView(DetailView):
    model = StudyMaterial
    template_name = 'materials/detail.html'
    context_object_name = 'material'

    def get_queryset(self):
        # Неопубліковані матеріали бачать лише персонал і ті, хто їх уже має
        user = self.request.user
        if is_teacher(user):
            return StudyMaterial.objects.all()
        visible = Q(is_published=True)
        if user.is_authenticated:
            visible |= Q(id__in=user.purchased_materials.values('id'))
        return StudyMaterial.objects.filter(visible)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.object
        context['is_owned'] = user_owns_material(self.request.user, material)
        context['approved_reviews'] = material.reviews.filter(is_approved=True).select_related('user')

        if material.is_bundle:
            total_original_price = sum(item.price for item in material.included_materials.all())
            context['total_original_price'] = total_original_price
            context['savings'] = total_original_price - material.price

        return context


class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'materials/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Завантаження конспектів (StudyMaterial)
        purchased_qs = self.request.user.purchased_materials.all()
        purchased_list = list(purchased_qs)

        def get_number(material):
            match = re.match(r'^(\d+)', material.title)
            if match:
                return int(match.group(1))
            return 99999

        purchased_list.sort(key=get_number)
        context['purchased_materials'] = purchased_list

        # 2. Інші дані кабінету
        context['form'] = UserProfileForm(instance=self.request.user)
        context['tutor_request'] = getattr(self.request.user, 'tutor_request', None)

        # 3. Індивідуальні презентації
        context['personal_presentations'] = self.request.user.personal_presentations.all()

        # 4. Власна статистика учня (останні 15 спроб)
        context['my_attempts'] = PracticeAttempt.objects.filter(
            user=self.request.user
        ).select_related('material').order_by('-created_at')[:15]

        # 5. ПАНЕЛЬ ВЧИТЕЛЯ (Показується тільки тобі)
        if is_teacher(self.request.user):
            # Дістаємо результати тестів усіх учнів зі статусом 'approved'
            context['students_attempts'] = PracticeAttempt.objects.filter(
                user__tutor_request__status='approved'
            ).select_related('user', 'user__tutor_request', 'material').order_by('-created_at')[:50]
            context['my_students'] = TutorStudentRequest.objects.filter(status='approved').order_by('-created_at')
            context['nmt_materials'] = StudyMaterial.objects.filter(is_published=True).order_by('title')

        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('cabinet')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


# ==========================================
# Безпечне читання матеріалу з Cloudinary + HTML Презентації + Кнопка Практики
# ==========================================
@login_required(login_url='/login/')
def download_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    if not request.user.purchased_materials.filter(id=material.id).exists() and not is_teacher(request.user):
        raise Http404("У вас немає доступу до цього матеріалу.")

    # Раніше тут PDF щоразу завантажувався з Cloudinary (до 10 с) і кодувався в base64,
    # хоча шаблон його не використовує
    return render(request, 'materials/reader.html', {'material': material})


@login_required(login_url='/login/')
@require_POST
def buy_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, is_published=True)
    my_user = request.user

    if user_owns_material(my_user, material):
        messages.info(request, f"Ви вже маєте конспект «{material.title}».")
        return redirect('cabinet')

    if material.is_free or material.price == 0:
        if material.is_bundle:
            for sub_material in material.included_materials.all():
                my_user.purchased_materials.add(sub_material)
        else:
            my_user.purchased_materials.add(material)
        messages.success(request, f"Успіх! «{material.title}» успішно отримано.")
        return redirect('cabinet')

    success = my_user.buy_material(material)

    if success:
        messages.success(request, f"Успіх! Конспект «{material.title}» додано. Залишок: {my_user.balance} грн.")
        return redirect('cabinet')
    else:
        messages.error(request, f"Недостатньо коштів для придбання «{material.title}». Поповніть баланс.")
        return redirect('materials_list')


@api_view(['GET'])
def api_materials_list(request):
    materials = StudyMaterial.objects.filter(is_published=True).select_related('category')
    materials_list = list(materials)

    def get_number(material):
        match = re.match(r'^(\d+)', material.title)
        return int(match.group(1)) if match else 99999

    materials_list.sort(key=get_number)
    serializer = StudyMaterialSerializer(materials_list, many=True)
    return Response({
        'status': 'success',
        'materials': serializer.data
    })


@api_view(['GET'])
def api_bot_user_library(request, telegram_id):
    # Віддає email і покупки учня, тому доступно лише боту із секретним токеном
    expected_token = getattr(settings, 'BOT_API_TOKEN', '') or ''
    provided_token = request.headers.get('X-Bot-Token', '')
    if not expected_token or not hmac.compare_digest(provided_token, expected_token):
        return Response({'status': 'error', 'message': 'Forbidden'}, status=403)

    user = User.objects.filter(telegram_id=telegram_id).first()

    if not user:
        return Response({'status': 'error', 'message': 'Учня не знайдено в базі платформи.'}, status=404)

    purchased = list(user.purchased_materials.all())

    def get_number(material):
        match = re.match(r'^(\d+)', material.title)
        return int(match.group(1)) if match else 99999

    purchased.sort(key=get_number)
    serializer = PurchasedMaterialSerializer(purchased, many=True)

    return Response({
        'status': 'success',
        'student_email': user.email,
        'library': serializer.data
    })


@login_required
@require_POST
def pay_from_balance(request):
    cart = get_object_or_404(Cart, user=request.user)

    with transaction.atomic():
        # Блокуємо рядок користувача, щоб подвійний клік або паралельне поповнення
        # не затерли баланс одне одного
        user = User.objects.select_for_update().get(pk=request.user.pk)
        cart_items = list(cart.items.select_related('material'))

        if not cart_items:
            messages.error(request, "Ваш кошик порожній.")
            return redirect('materials_list')

        total_price = cart.get_total_price()
        if user.balance < total_price:
            messages.error(request, "На вашому балансі недостатньо коштів. Будь ласка, оберіть оплату карткою (Monobank).")
            return redirect('cart_detail')

        user.balance -= total_price
        user.save(update_fields=['balance'])

        order = Order.objects.create(
            user=user,
            total_amount=total_price,
            status='paid',
            paid_at=timezone.now(),
            mono_invoice_id='balance_payment'
        )

        for item in cart_items:
            if item.material.is_bundle:
                for sub_material in item.material.included_materials.all():
                    user.purchased_materials.add(sub_material)
            else:
                user.purchased_materials.add(item.material)

            OrderItem.objects.create(
                order=order,
                material=item.material,
                price=item.material.price
            )

        cart.items.all().delete()

    messages.success(request,
                     f"Оплата пройшла успішно! Списано {total_price} ₴. Матеріали вже у вашому кабінеті. 🎉")
    return redirect('cabinet')


def send_telegram_notification(message):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_ADMIN_ID', '')

    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(url, json=payload, timeout=5)
            if not response.ok:
                print(f"Telegram відхилив повідомлення: {response.status_code} {response.text[:300]}")
        except Exception as e:
            print(f"Помилка відправки в Telegram: {e}")


@login_required
@require_POST
def pay_with_mono(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()

    if not cart.items.exists():
        messages.error(request, "Ваш кошик порожній.")
        return redirect('materials_list')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total_amount=total_price,
            status='pending'
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, material=item.material, price=item.material.price)

    amount_kopecks = int(total_price * 100)

    headers = {
        'X-Token': getattr(settings, 'MONOBANK_TOKEN', ''),
        'Content-Type': 'application/json'
    }

    payload = {
        "amount": amount_kopecks,
        "ccy": 980,
        "reference": str(order.id),
        "redirectUrl": "https://dokvadratu.com.ua/cabinet/",
        "webHookUrl": "https://dokvadratu.com.ua/mono/webhook/",
    }
    try:
        response = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=payload, headers=headers,
                                 timeout=15)
        data = response.json()

        if 'pageUrl' in data:
            order.mono_invoice_id = data['invoiceId']
            order.save()
            return redirect(data['pageUrl'])
        else:
            messages.error(request, "Помилка платіжної системи. Спробуйте пізніше або спишіть з балансу.")
            return redirect('cart_detail')

    except Exception:
        messages.error(request, "Помилка з'єднання з Monobank.")
        return redirect('cart_detail')


@login_required
def topup_balance_view(request):
    if request.method == 'POST':
        # Баланс зберігається в цілих гривнях, тому й поповнення — лише цілими гривнями
        amount = to_int(request.POST.get('amount'))
        if amount is None or not 1 <= amount <= 100000:
            messages.error(request, "Введіть коректну суму (ціле число гривень від 1 до 100 000).")
            return redirect('cabinet')

        amount_kopecks = amount * 100

        # Створюємо технічне замовлення для поповнення
        order = Order.objects.create(
            user=request.user,
            total_amount=amount,
            status='pending',
            source='web'
        )

        headers = {
            'X-Token': getattr(settings, 'MONOBANK_TOKEN', ''),
            'Content-Type': 'application/json'
        }

        payload = {
            "amount": amount_kopecks,
            "ccy": 980,
            "reference": str(order.id),
            "redirectUrl": "https://dokvadratu.com.ua/cabinet/",
            "webHookUrl": "https://dokvadratu.com.ua/mono/webhook/",
        }
        try:
            response = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=payload,
                                     headers=headers, timeout=15)
            data = response.json()

            if 'pageUrl' in data:
                order.mono_invoice_id = data['invoiceId']
                order.save()
                return redirect(data['pageUrl'])
            else:
                messages.error(request, "Помилка платіжної системи.")
                return redirect('cabinet')
        except Exception:
            messages.error(request, "Помилка з'єднання з Monobank.")
            return redirect('cabinet')

    return redirect('cabinet')


MONO_PUBKEY_URL = "https://api.monobank.ua/api/merchant/pubkey"
MONO_PUBKEY_CACHE_KEY = 'monobank_pubkey'
MONO_PUBKEY_REFRESHED_KEY = 'monobank_pubkey_refreshed'


class MonoPubKeyUnavailable(Exception):
    pass


def get_mono_pubkey(force_refresh=False):
    """Публічний ключ Monobank для перевірки підпису вебхуків (base64 від PEM)."""
    key = None if force_refresh else cache.get(MONO_PUBKEY_CACHE_KEY)
    if not key:
        try:
            response = requests.get(MONO_PUBKEY_URL, headers={'X-Token': getattr(settings, 'MONOBANK_TOKEN', '') or ''},
                                    timeout=10)
            response.raise_for_status()
            key = response.json()['key']
        except Exception as e:
            raise MonoPubKeyUnavailable(str(e))
        cache.set(MONO_PUBKEY_CACHE_KEY, key, 60 * 60 * 24)
        cache.set(MONO_PUBKEY_REFRESHED_KEY, True, 60 * 10)
    return key


def _signature_matches(pub_key_base64, signature, body):
    try:
        verifying_key = ecdsa.VerifyingKey.from_pem(base64.b64decode(pub_key_base64).decode())
        return verifying_key.verify(signature, body, sigdecode=ecdsa.util.sigdecode_der, hashfunc=hashlib.sha256)
    except Exception:
        # BadSignatureError, зіпсований DER чи ключ — підпис недійсний
        return False


def verify_mono_signature(body, x_sign):
    """Перевіряє заголовок X-Sign (ECDSA, SHA-256) вебхука Monobank."""
    if not x_sign:
        return False
    try:
        signature = base64.b64decode(x_sign, validate=True)
    except Exception:
        return False

    if _signature_matches(get_mono_pubkey(), signature, body):
        return True

    # Monobank міг змінити ключ: перезапитуємо, але не частіше разу на 10 хвилин,
    # щоб підроблені запити не змушували нас постійно смикати API банку
    if cache.get(MONO_PUBKEY_REFRESHED_KEY):
        return False
    return _signature_matches(get_mono_pubkey(force_refresh=True), signature, body)


@csrf_exempt
def mono_webhook(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
        if not verify_mono_signature(request.body, request.headers.get('X-Sign', '')):
            return HttpResponse("Invalid signature", status=403)
    except MonoPubKeyUnavailable as e:
        # 5xx, щоб Monobank повторив запит пізніше
        print(f"Webhook: не вдалося отримати ключ Monobank: {e}")
        return HttpResponse("Temporary error", status=503)

    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponse("Error", status=400)

    invoice_id = data.get('invoiceId')
    if data.get('status') != 'success' or not invoice_id:
        return HttpResponse("OK", status=200)

    msg = None
    with transaction.atomic():
        # select_for_update: Monobank може надіслати один вебхук кілька разів одночасно
        order = Order.objects.select_for_update().filter(mono_invoice_id=invoice_id).first()
        if order is None or order.status == 'paid':
            return HttpResponse("OK", status=200)

        order.status = 'paid'
        order.paid_at = timezone.now()
        order.save(update_fields=['status', 'paid_at'])

        order_items = list(order.items.select_related('material'))
        if order_items:
            materials = [item.material for item in order_items if item.material]
            for material in materials:
                if material.is_bundle:
                    for sub_material in material.included_materials.all():
                        order.user.purchased_materials.add(sub_material)
                else:
                    order.user.purchased_materials.add(material)

            CartItem.objects.filter(cart__user=order.user, material__in=materials).delete()
            msg = f"🛒 Нова покупка!\nУчень: {order.user.email}\nОплачено: {order.total_amount} ₴"
        else:
            User.objects.filter(pk=order.user_id).update(balance=F('balance') + int(order.total_amount))
            msg = f"💰 Нове поповнення!\nУчень: {order.user.email}\nСума: {order.total_amount} ₴"

    send_telegram_notification(msg)
    return HttpResponse("OK", status=200)


@login_required
def request_tutor_student_status(request):
    if request.method == 'POST':
        student_name = request.POST.get('real_name', '').strip()[:100]
        course_type = request.POST.get('course', 'nmt')

        if not student_name or course_type not in dict(TutorStudentRequest.COURSE_CHOICES):
            messages.error(request, "Будь ласка, заповніть усі поля форми.")
            return redirect('cabinet')

        student_req, created = TutorStudentRequest.objects.get_or_create(
            user=request.user,
            defaults={'real_name': student_name, 'course': course_type}
        )

        if created:
            course_display = dict(TutorStudentRequest.COURSE_CHOICES).get(course_type, course_type)
            messages.success(request, "Заявку успішно надіслано! Очікуйте на підтвердження.")
            msg = f"🙋‍♂️ <b>Нова заявка на статус учня!</b>\n\nУчень: <b>{html.escape(student_name)}</b>\nКлас/Курс: <b>{course_display}</b>\nEmail: {html.escape(request.user.email)}\n\nЧекає на твоє підтвердження в адмінці."
            send_telegram_notification(msg)

        elif student_req.status == 'pending':
            student_req.real_name = student_name
            student_req.course = course_type
            student_req.save()
            messages.info(request, "Вашу заявку оновлено. Вона вже розглядається.")

        elif student_req.status == 'approved':
            messages.info(request, "Ви вже є підтвердженим учнем.")

    return redirect('cabinet')


# ==========================================
# ВІДГУКИ
# ==========================================
def parse_rating(value):
    rating = to_int(value)
    return rating if rating in dict(Review.RATING_CHOICES) else None


@login_required
@require_POST
def submit_review(request):
    rating = parse_rating(request.POST.get('rating', 5))
    text = request.POST.get('text', '').strip()
    reviewer_name = request.POST.get('reviewer_name', '').strip()[:100]
    material_id = request.POST.get('material_id')
    back_url = safe_back_url(request)

    if not text or not reviewer_name:
        messages.error(request, "Будь ласка, введіть своє ім'я та текст відгуку.")
        return redirect(back_url)
    if rating is None:
        messages.error(request, "Оберіть оцінку від 1 до 5.")
        return redirect(back_url)

    review = Review(
        user=request.user,
        reviewer_name=reviewer_name,
        rating=rating,
        text=text
    )

    material_title = "Загальний відгук (про заняття)"
    if material_id:
        material = get_object_or_404(StudyMaterial, id=to_int(material_id))
        review.material = material
        material_title = f"Матеріал: {material.title}"

    review.save()

    msg = (f"⭐️ <b>Новий відгук!</b>\n\nВід: {html.escape(reviewer_name)} ({html.escape(request.user.email)})\n"
           f"Оцінка: {'⭐' * rating}\nЩодо: {html.escape(material_title)}\n\n<i>«{html.escape(text)}»</i>\n\n"
           f"Перевір та схвали його в адмінці.")
    send_telegram_notification(msg)

    messages.success(request, "Дякуємо за ваш відгук! Він з'явиться на сайті після перевірки модератором.")
    return redirect(back_url)


@login_required(login_url='/login/')
def view_student_presentation(request, presentation_id):
    presentation = get_object_or_404(StudentPresentation, id=presentation_id)

    if presentation.student != request.user and not request.user.is_staff:
        raise Http404("У вас немає доступу до цієї презентації.")

    context = {
        'material': presentation,
        'is_personal': True
    }
    return render(request, 'materials/reader.html', context)


@login_required
def view_attempt_details(request, attempt_id):
    attempt = get_object_or_404(PracticeAttempt, id=attempt_id)

    # Перевірка: дивитися може учень свої тести, або вчитель - усі
    if attempt.user != request.user and not is_teacher(request.user):
        raise Http404("У вас немає доступу до цієї статистики.")

    saved_answers = attempt.answers_json
    if not saved_answers:
        messages.info(request, "Цей тест був пройдений до оновлення системи. Деталі не збережено.")
        return redirect('cabinet')

    questions = questions_in_order(parse_id_list(saved_answers.get('question_ids', '')))

    results_data = []
    for q in questions:
        q_result = {
            'question': q, 'type': q.question_type, 'is_correct': False,
            'user_answer': None, 'correct_answer': None, 'points_earned': 0, 'max_points': 0
        }

        if q.question_type == 'CHOICE':
            q_result['max_points'] = 1
            q_result['correct_answer'] = q.options.filter(is_correct=True).first()
            user_ans = saved_answers.get('q_choice', {}).get(str(q.id))
            opt = find_option(q, user_ans)
            if opt:
                q_result['user_answer'] = opt
                if opt.is_correct:
                    q_result['points_earned'] = 1
                    q_result['is_correct'] = True

        elif q.question_type == 'MATCH':
            q_result['max_points'] = 3
            q_result['matches'] = []
            match_points = 0
            for item in q.match_items.all():
                user_match = saved_answers.get('q_match', {}).get(str(q.id), {}).get(str(item.id))
                user_opt = find_option(q, user_match)
                is_match_correct = user_opt is not None and user_opt.id == item.correct_option_id
                if is_match_correct:
                    match_points += 1
                q_result['matches'].append({
                    'item': item, 'user_option': user_opt,
                    'correct_option': item.correct_option, 'is_correct': is_match_correct
                })
            q_result['points_earned'] = match_points
            q_result['is_correct'] = (match_points == 3)

        elif q.question_type == 'SHORT':
            q_result['max_points'] = 2
            q_result['correct_answer'] = q.correct_short_answer
            user_ans = saved_answers.get('q_short', {}).get(str(q.id))
            q_result['user_answer'] = user_ans
            if user_ans:
                user_clean = str(user_ans).strip().replace(',', '.')
                correct_clean = str(q.correct_short_answer).strip().replace(',', '.')
                if user_clean == correct_clean:
                    q_result['points_earned'] = 2
                    q_result['is_correct'] = True

        results_data.append(q_result)

    context = {
        'material': attempt.material,
        'total_score': attempt.score,
        'max_score': attempt.max_score,
        'results_data': results_data,
    }
    # Використовуємо той самий шаблон результатів!
    return render(request, 'materials/practice_results.html', context)


@login_required
def report_question_error(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = to_int(data.get('question_id'))
            message = str(data.get('message') or '').strip()[:2000]
            if not message:
                return JsonResponse({'status': 'error', 'message': 'Опишіть помилку'}, status=400)

            question = get_object_or_404(Question, id=question_id)

            # Зберігаємо в базу
            QuestionError.objects.create(
                question=question,
                user=request.user,
                message=message
            )

            # Відправляємо в Telegram
            msg = f"🚨 <b>СКАРГА НА ЗАВДАННЯ!</b>\n\n"
            msg += f"<b>ID Завдання:</b> {question.id}\n"
            msg += f"<b>Учень:</b> {html.escape(request.user.email)}\n\n"
            msg += f"<b>Що не так:</b> <i>{html.escape(message)}</i>\n\n"
            msg += f"Зайди в адмінку (розділ 'Скарги на завдання'), щоб виправити."

            send_telegram_notification(msg)

            return JsonResponse({'status': 'success'})
        except Http404:
            return JsonResponse({'status': 'error', 'message': 'Завдання не знайдено'}, status=404)
        except Exception as e:
            print(f"Помилка збереження скарги: {e}")
            return JsonResponse({'status': 'error', 'message': 'Не вдалося надіслати скаргу'}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)


def parent_dashboard_view(request, parent_token):
    # Шукаємо заявку учня за унікальним токеном
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token)

    # === ДОДАНО: Дістаємо всі індивідуальні презентації цього учня ===
    presentations = StudentPresentation.objects.filter(student=student_request.user).order_by('-created_at')

    context = {
        'student': student_request,
        'presentations': presentations,  # Передаємо в шаблон
    }

    # Якщо це підготовка до НМТ -> дістаємо результати тестів
    if student_request.course == 'nmt':
        attempts = PracticeAttempt.objects.filter(user=student_request.user).order_by('-created_at')
        context['attempts'] = attempts
        context['is_nmt'] = True
    else:
        # Для шкільної програми НУШ -> дістаємо ваші ручні звіти
        reports = StudentReport.objects.filter(student=student_request).order_by('-date')
        context['reports'] = reports
        context['is_nmt'] = False

    return render(request, 'materials/parent_dashboard.html', context)


# === НОВА ФУНКЦІЯ ДЛЯ БАТЬКІВ ===
def parent_view_presentation(request, parent_token, presentation_id):
    # Перевіряємо токен батьків
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token)

    # Дістаємо презентацію, яка належить саме цьому учню
    presentation = get_object_or_404(StudentPresentation, id=presentation_id, student=student_request.user)

    context = {
        'material': presentation,
        'is_personal': True
    }
    # Використовуємо існуючий шаблон для відображення презентацій
    return render(request, 'materials/reader.html', context)

@login_required
@require_POST
def add_quick_report(request):
    if not is_teacher(request.user):
        return redirect('cabinet')

    student = get_object_or_404(TutorStudentRequest, id=to_int(request.POST.get('student_id')))
    form = StudentReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        report.student = student
        report.save()
        messages.success(request, f"✅ Звіт для {student.real_name} успішно надіслано на дашборд!")
    else:
        errors = '; '.join(err for field_errors in form.errors.values() for err in field_errors)
        messages.error(request, f"Звіт не збережено: {errors}")
    return redirect('cabinet')


@login_required
@require_POST
def add_nmt_score(request):
    if not is_teacher(request.user):
        return redirect('cabinet')

    student_req = get_object_or_404(TutorStudentRequest, id=to_int(request.POST.get('student_id')))
    material = get_object_or_404(StudyMaterial, id=to_int(request.POST.get('material_id')))
    score = to_int(request.POST.get('score'))
    max_score = to_int(request.POST.get('max_score', 18))

    if score is None or max_score is None or max_score <= 0 or not 0 <= score <= max_score:
        messages.error(request, "Бал має бути числом від 0 до максимуму, а максимум — більшим за 0.")
        return redirect('cabinet')

    # Створюємо спробу з позначкою в JSON
    PracticeAttempt.objects.create(
        user=student_req.user,
        material=material,
        score=score,
        max_score=max_score,
        answers_json={'note': 'Спільна робота на уроці (демонстрація екрана)'}
    )
    messages.success(request, f"✅ Результат роботи на уроці для {student_req.real_name} успішно додано!")
    return redirect('cabinet')


def submit_parent_review(request, parent_token):
    if request.method == 'POST':
        # Знаходимо учня за батьківським токеном
        student_req = get_object_or_404(TutorStudentRequest, parent_token=parent_token)

        rating = parse_rating(request.POST.get('rating', 5))
        text = request.POST.get('text', '').strip()
        reviewer_name = request.POST.get('reviewer_name', '').strip()[:100]

        if not text or not reviewer_name or rating is None:
            messages.error(request, "Будь ласка, введіть своє ім'я, оцінку та текст відгуку.")
            return redirect('parent_dashboard', parent_token=parent_token)

        # Створюємо відгук і прив'язуємо його до профілю учня
        Review.objects.create(
            user=student_req.user,
            reviewer_name=reviewer_name,
            rating=rating,
            text=text
        )

        # Відправляємо тобі сповіщення у Telegram із подвійним ім'ям (ім'я на сайті + чиї це батьки)
        msg = f"⭐️ <b>Новий відгук від батьків!</b>\n\n"
        msg += f"Від: <b>{html.escape(reviewer_name)}</b> <i>(Батьки учня: {html.escape(student_req.real_name)})</i>\n"
        msg += f"Оцінка: {'⭐' * rating}\n\n"
        msg += f"<i>«{html.escape(text)}»</i>\n\n"
        msg += f"Зайди в адмінку, щоб схвалити публікацію на головній сторінці."

        send_telegram_notification(msg)

        messages.success(request, "Щиро дякуємо за ваш відгук! Ваша думка дуже важлива для нас.")

    return redirect('parent_dashboard', parent_token=parent_token)