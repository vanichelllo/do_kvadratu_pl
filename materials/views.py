import base64
import hashlib
import hmac
import html
import ecdsa
import re
import requests
import json
import logging
import random
from functools import wraps
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.templatetags.static import static
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Case, F, Prefetch, Q, When
from django.conf import settings
from django.core.cache import cache

from users.forms import UserProfileForm
from users.views import terms_required
from .forms import StudentReportForm

# ОНОВЛЕНІ ІМПОРТИ: Видалено Category та DiagnosticTopic, додано CurriculumTopic
from .models import (
    StudyMaterial, Cart, CartItem, Order, OrderItem, Question,
    PracticeAttempt, TutorStudentRequest, Review, StudentPresentation,
    QuestionError, StudentReport, CurriculumSubject, CurriculumGrade, CurriculumTopic, DEFAULT_MATERIAL_DESCRIPTION
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudyMaterialSerializer, PurchasedMaterialSerializer
from django.utils import timezone

User = get_user_model()
logger = logging.getLogger(__name__)


def is_teacher(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)


MAX_DB_INT = 2 ** 63 - 1


def to_int(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if -MAX_DB_INT <= number <= MAX_DB_INT else None


def post_required(redirect_to):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method != 'POST':
                return redirect(redirect_to(**kwargs) if callable(redirect_to) else redirect_to)
            return view(request, *args, **kwargs)

        return wrapper

    return decorator


def material_page(material_id, **kwargs):
    return reverse('material_detail', args=[material_id])


def parse_id_list(ids_str):
    return [i for i in (to_int(x) for x in (ids_str or '').split(',')) if i is not None]


def questions_in_order(q_id_list):
    if not q_id_list:
        return []
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(q_id_list)])
    return (Question.objects.filter(id__in=q_id_list)
            .prefetch_related('options', 'match_items__correct_option').order_by(preserved_order))


# ОНОВЛЕНО: Тепер використовуємо curriculum_topic_id
def is_own_question(question, material, material_num=None):
    if question.curriculum_topic_id and material.curriculum_topic_id:
        return question.curriculum_topic_id == material.curriculum_topic_id
    return False


def seen_question_ids(user):
    seen = set()
    for answers in PracticeAttempt.objects.filter(user=user).values_list('answers_json', flat=True):
        if isinstance(answers, dict):
            seen.update(parse_id_list(str(answers.get('question_ids') or '')))
    return seen


def sample_unseen_first(pool, count, seen_ids):
    unseen = [q for q in pool if q.id not in seen_ids]
    picked = random.sample(unseen, min(count, len(unseen)))
    if len(picked) < count:
        seen = [q for q in pool if q.id in seen_ids]
        picked += random.sample(seen, min(count - len(picked), len(seen)))
    return picked


def find_option(question, option_id):
    option_id = to_int(option_id)
    if option_id is None:
        return None
    return next((opt for opt in question.options.all() if opt.id == option_id), None)


DIAGNOSTIC_MATERIAL_TITLE = "Вхідне діагностичне тестування НМТ"


def user_owns_material(user, material):
    if not user.is_authenticated:
        return False
    if user.purchased_materials.filter(id=material.id).exists():
        return True
    if material.is_bundle:
        included_ids = list(material.included_materials.values_list('id', flat=True))
        return bool(included_ids) and \
            user.purchased_materials.filter(id__in=included_ids).count() == len(included_ids)
    return False


def rate_limit_exceeded(key, limit, window):
    key = f'rate-limit:{key}'
    cache.add(key, 0, window)
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, window)
        count = 1
    return count > limit


def safe_back_url(request, fallback='cabinet'):
    referer = request.META.get('HTTP_REFERER', '')
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()},
                                                   require_https=request.is_secure()):
        return referer
    return fallback


# ==========================================
# ОНОВЛЕНИЙ ГЕНЕРАТОР ДІАГНОСТИКИ
# ==========================================
def diagnostic_test_view(request):
    if request.method == 'POST':
        question_ids_str = request.POST.get('question_ids', '')
        q_id_list = parse_id_list(question_ids_str)

        saved_answers = {
            'q_choice': {}, 'q_match': {}, 'q_short': {},
            'question_ids': question_ids_str, 'note': 'Вхідна діагностика НМТ'
        }

        questions = questions_in_order(q_id_list)

        topics_stats = {}
        total_score = 0
        max_score = 0

        for question in questions:
            topic = question.curriculum_topic
            topic_id = topic.id if topic else 0

            if topic_id not in topics_stats:
                topics_stats[topic_id] = {'topic': topic, 'correct': 0, 'total': 0}

            stat = topics_stats[topic_id]

            if question.question_type == 'CHOICE':
                stat['total'] += 1
                max_score += 1
                user_answer = request.POST.get(f'question_{question.id}')
                saved_answers['q_choice'][str(question.id)] = user_answer

                selected_option = find_option(question, user_answer)
                if selected_option and selected_option.is_correct:
                    total_score += 1
                    stat['correct'] += 1

            elif question.question_type == 'MATCH':
                stat['total'] += 3
                max_score += 3
                match_correct_count = 0
                saved_answers['q_match'][str(question.id)] = {}

                for item in question.match_items.all():
                    user_match_answer = request.POST.get(f'match_{item.id}')
                    saved_answers['q_match'][str(question.id)][str(item.id)] = user_match_answer

                    if to_int(user_match_answer) == item.correct_option_id:
                        match_correct_count += 1
                total_score += match_correct_count
                stat['correct'] += match_correct_count

            elif question.question_type == 'SHORT':
                stat['total'] += 2
                max_score += 2
                user_answer = request.POST.get(f'question_{question.id}')
                saved_answers['q_short'][str(question.id)] = user_answer

                if user_answer:
                    user_clean = str(user_answer).strip().replace(',', '.')
                    correct_clean = str(question.correct_short_answer).strip().replace(',', '.')
                    if user_clean == correct_clean:
                        total_score += 2
                        stat['correct'] += 2

        if request.user.is_authenticated:
            diag_material, _ = StudyMaterial.objects.get_or_create(
                title=DIAGNOSTIC_MATERIAL_TITLE,
                defaults={'price': 0, 'is_published': False, 'is_free': True}
            )
            PracticeAttempt.objects.create(
                user=request.user, material=diag_material,
                score=total_score, max_score=max_score, answers_json=saved_answers
            )

        weak_topics = [s['topic'] for s in topics_stats.values() if
                       s['topic'] and s['total'] > 0 and (s['correct'] / s['total']) * 100 < 50]

        recommended_materials = set()
        if weak_topics:
            recommended_materials.update(
                StudyMaterial.objects.filter(curriculum_topic__in=weak_topics, is_published=True).distinct())

        percent_total = int((total_score / max_score) * 100) if max_score > 0 else 0

        recommendations_list = sorted(list(recommended_materials),
                                      key=lambda m: m.curriculum_topic.order if m.curriculum_topic else 999)
        sorted_stats = sorted([s for s in topics_stats.values() if s['topic']], key=lambda s: s['topic'].order)

        return render(request, 'materials/diagnostic_results.html', {
            'total_score': total_score, 'max_score': max_score, 'percent_total': percent_total,
            'weak_topics': weak_topics, 'topics_stats': sorted_stats, 'recommendations': recommendations_list,
        })

    buckets = {}

    for q_id, q_type, chapter_order in Question.objects.exclude(curriculum_topic__isnull=True).values_list('id',
                                                                                                           'question_type',
                                                                                                           'curriculum_topic__chapter__order'):
        is_algebra = (chapter_order <= 540)
        buckets.setdefault((q_type, is_algebra), []).append(q_id)

    def pick(q_type, is_algebra, count):
        ids = buckets.get((q_type, is_algebra), [])
        return random.sample(ids, min(count, len(ids)))

    sel_choice = pick('CHOICE', True, 10) + pick('CHOICE', False, 5)
    sel_match = pick('MATCH', True, 2) + pick('MATCH', False, 1)
    sel_short = pick('SHORT', True, 2) + pick('SHORT', False, 2)

    random.shuffle(sel_choice)
    random.shuffle(sel_match)
    random.shuffle(sel_short)

    final_questions = list(questions_in_order(sel_choice + sel_match + sel_short))
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
    has_access = is_teacher(request.user) or user_owns_material(request.user, material)

    if not material.is_published and not has_access:
        raise Http404("Матеріал не знайдено.")
    if not (material.is_free or has_access):
        messages.error(request, f"Практика доступна після придбання матеріалу «{material.title}».")
        return redirect('material_detail', pk=material.id)

    if request.method == 'POST':
        total_score = 0
        max_score = 0
        results_data = []

        saved_answers = {'q_choice': {}, 'q_match': {}, 'q_short': {}}

        question_ids_str = request.POST.get('question_ids', '')
        saved_answers['question_ids'] = question_ids_str

        questions = questions_in_order(parse_id_list(question_ids_str))
        if questions:
            questions = questions.filter(materials=material).distinct()

        for q in questions:
            q_result = {
                'question': q, 'type': q.question_type, 'is_correct': False,
                'user_answer': None, 'correct_answer': None, 'points_earned': 0, 'max_points': 0
            }

            if q.question_type == 'CHOICE':
                q_result['max_points'] = 1
                q_result['correct_answer'] = next((opt for opt in q.options.all() if opt.is_correct), None)
                user_ans = request.POST.get(f'q_{q.id}')
                saved_answers['q_choice'][str(q.id)] = user_ans

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
                    saved_answers['q_match'][str(q.id)][str(item.id)] = user_match

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
                saved_answers['q_short'][str(q.id)] = user_ans
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

    match_current = re.match(r'^(\d+)', material.title)
    current_topic_num = int(match_current.group(1)) if match_current else 0
    # ОНОВЛЕНО: select_related('curriculum_topic')
    raw_pool = (Question.objects.filter(materials=material).select_related('curriculum_topic')
                .prefetch_related('options', 'match_items', 'materials'))

    safe_pool = []
    for q in raw_pool:
        is_safe = is_own_question(q, material, current_topic_num)
        if not is_safe:
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

    seen_ids = seen_question_ids(request.user)
    q_choice = sample_unseen_first(choice_pool, 10, seen_ids)
    q_match = sample_unseen_first(match_pool, 2, seen_ids)
    q_short = sample_unseen_first(short_pool, 1, seen_ids)

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
# КОШИК
# ==========================================
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

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

    return render(request, 'materials/cart.html', {'cart': cart, 'cart_items': cart.cached_items()})


@login_required
@post_required(material_page)
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
@post_required('cart_detail')
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


def web_manifest(request):
    icons = [{'src': static(f'images/icon-{size}.png'), 'sizes': f'{size}x{size}', 'type': 'image/png'}
             for size in (192, 512)]
    icons += [{'src': static(f'images/icon-maskable-{size}.png'), 'sizes': f'{size}x{size}', 'type': 'image/png',
               'purpose': 'maskable'} for size in (192, 512)]
    data = {
        'name': 'ДО КВАДРАТУ — підготовка до НМТ з математики',
        'short_name': 'ДО КВАДРАТУ',
        'start_url': '/',
        'display': 'browser',
        'background_color': '#344e86',
        'theme_color': '#344e86',
        'icons': icons,
    }
    response = JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    response['Content-Type'] = 'application/manifest+json'
    return response


def booking_view(request):
    return render(request, 'booking.html')


# ==========================================
# ОНОВЛЕНА ВІТРИНА
# ==========================================
class MaterialListView(ListView):
    model = StudyMaterial
    template_name = 'materials/list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        queryset = StudyMaterial.objects.filter(is_published=True) \
            .select_related('curriculum_topic__chapter__grade__subject') \
            .prefetch_related('tags')

        filter_type = self.request.GET.get('type')
        if filter_type == 'free':
            queryset = queryset.filter(is_free=True)
        elif filter_type == 'bundle':
            queryset = queryset.filter(is_bundle=True)

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        subject_id = self.request.GET.get('subject')
        grade_id = self.request.GET.get('grade')

        if grade_id:
            queryset = queryset.filter(curriculum_topic__chapter__grade_id=grade_id)
        elif subject_id:
            queryset = queryset.filter(curriculum_topic__chapter__grade__subject_id=subject_id)

        materials_list = list(queryset)

        def get_sort_key(material):
            if material.curriculum_topic:
                ct = material.curriculum_topic
                return (
                    ct.chapter.grade.subject.order,
                    ct.chapter.grade.order,
                    ct.chapter.order,
                    ct.order
                )
            else:
                match = re.match(r'^(\d+)', material.title)
                num = int(match.group(1)) if match else 99999
                return (999, 999, 999, num)

        materials_list.sort(key=get_sort_key)
        return materials_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = CurriculumSubject.objects.prefetch_related('grades').all()
        context['current_subject'] = self.request.GET.get('subject', '')
        context['current_grade'] = self.request.GET.get('grade', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class MaterialDetailView(DetailView):
    model = StudyMaterial
    template_name = 'materials/detail.html'
    context_object_name = 'material'

    def get_object(self, queryset=None):
        material = super().get_object(queryset)
        user = self.request.user
        if not (material.is_published or is_teacher(user) or user_owns_material(user, material)):
            raise Http404("Матеріал не знайдено.")
        return material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.object
        context['is_owned'] = user_owns_material(self.request.user, material)
        context['default_description'] = DEFAULT_MATERIAL_DESCRIPTION
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

        with_tree = 'curriculum_topic__chapter__grade__subject'
        purchased_list = list(self.request.user.purchased_materials.select_related(with_tree).prefetch_related(
            Prefetch('included_materials', queryset=StudyMaterial.objects.select_related(with_tree))))

        def get_number(material):
            if material.curriculum_topic:
                ct = material.curriculum_topic
                return (ct.chapter.grade.subject.order, ct.chapter.grade.order, ct.chapter.order, ct.order)

            match = re.match(r'^(\d+)', material.title)
            if match:
                return (999, 999, 999, int(match.group(1)))
            return (999, 999, 999, 99999)

        purchased_list.sort(key=get_number)
        context['purchased_materials'] = purchased_list

        # Бібліотека: окремі теми групуємо за курсом і класом (список уже відсортовано за деревом тем)
        library_groups = []
        for material in purchased_list:
            if material.is_bundle:
                continue
            grade = material.curriculum_grade
            label = grade.short_label if grade else 'Інші матеріали'
            if not library_groups or library_groups[-1]['label'] != label:
                library_groups.append({'label': label, 'materials': []})
            library_groups[-1]['materials'].append(material)
        context['library_groups'] = library_groups

        # Пакет сам не має контенту — показуємо його теми; посилання лише на ті, до яких є доступ
        owned_ids = {m.id for m in purchased_list}
        context['library_bundles'] = [
            {'bundle': bundle, 'topics': [{'material': m, 'owned': m.id in owned_ids}
                                          for m in sorted(bundle.included_materials.all(), key=get_number)]}
            for bundle in purchased_list if bundle.is_bundle
        ]

        context['form'] = UserProfileForm(instance=self.request.user)
        context['tutor_request'] = getattr(self.request.user, 'tutor_request', None)
        context['course_choices'] = TutorStudentRequest.COURSE_CHOICES
        context['personal_presentations'] = self.request.user.personal_presentations.all()
        context['my_attempts'] = PracticeAttempt.objects.filter(
            user=self.request.user
        ).select_related('material').defer('material__html_content').order_by('-created_at')[:15]

        if is_teacher(self.request.user):
            context['students_attempts'] = PracticeAttempt.objects.filter(
                user__tutor_request__status='approved'
            ).select_related('user', 'user__tutor_request', 'material').defer(
                'material__html_content').order_by('-created_at')[:50]
            context['my_students'] = TutorStudentRequest.objects.filter(status='approved').order_by('-created_at')
            context['nmt_materials'] = StudyMaterial.objects.filter(is_published=True).order_by('title')

            # ОНОВЛЕНО: Теми для звітів НУШ
            context['all_curriculum_topics'] = CurriculumTopic.objects.exclude(
                chapter__grade__subject__name="Підготовка до НМТ / ЗНО"
            ).select_related('chapter__grade').order_by('chapter__grade__subject__order', 'chapter__grade__order',
                                                        'chapter__order', 'order')

        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('cabinet')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


@login_required(login_url='/login/')
def download_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    if not request.user.purchased_materials.filter(id=material.id).exists() and not is_teacher(request.user):
        raise Http404("У вас немає доступу до цього матеріалу.")

    return render(request, 'materials/reader.html', {'material': material})


@api_view(['GET'])
def api_materials_list(request):
    materials = StudyMaterial.objects.filter(is_published=True).select_related('curriculum_topic')
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
@post_required('cart_detail')
@terms_required('/cart/')
def pay_from_balance(request):
    cart = get_object_or_404(Cart, user=request.user)

    if request.POST.get('agree') != 'on':
        messages.error(request, "Щоб перейти до оплати, поставте галочку про згоду з умовами "
                                "і з відкриттям матеріалів одразу після оплати.")
        return redirect('cart_detail')

    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=request.user.pk)
        cart_items = list(cart.items.select_related('material').defer('material__html_content'))

        if not cart_items:
            messages.error(request, "Ваш кошик порожній.")
            return redirect('materials_list')

        total_price = cart.get_total_price()
        if user.balance < total_price:
            messages.error(request,
                           "На вашому балансі недостатньо коштів. Будь ласка, оберіть оплату карткою (Monobank).")
            return redirect('cart_detail')

        user.balance -= total_price
        user.save(update_fields=['balance'])

        order = Order.objects.create(
            user=user,
            total_amount=total_price,
            status='paid',
            paid_at=timezone.now(),
            mono_invoice_id='balance_payment',
            instant_access_agreed_at=timezone.now(),
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

    messages.success(request, f"Оплата пройшла успішно! Списано {total_price} ₴. Матеріали вже у вашому кабінеті. 🎉")
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
                logger.warning("Telegram відхилив повідомлення: %s %s", response.status_code, response.text[:300])
        except Exception as e:
            logger.warning("Помилка відправки в Telegram: %s", e)


SITE_URL = "https://dokvadratu.com.ua"
MONO_API_URL = "https://api.monobank.ua/api/merchant"


def mono_headers():
    return {'X-Token': getattr(settings, 'MONOBANK_TOKEN', '') or '', 'Content-Type': 'application/json'}


def create_mono_invoice(order, amount_kopecks):
    payload = {
        "amount": amount_kopecks,
        "ccy": 980,
        "reference": str(order.id),
        "redirectUrl": f"{SITE_URL}{reverse('payment_result', args=[order.id])}",
        "webHookUrl": f"{SITE_URL}/mono/webhook/",
    }
    try:
        response = requests.post(f"{MONO_API_URL}/invoice/create", json=payload, headers=mono_headers(), timeout=15)
        data = response.json()
    except Exception:
        logger.exception("Не вдалося створити рахунок Monobank для замовлення #%s", order.id)
        return None

    if 'pageUrl' not in data:
        logger.error("Monobank не створив рахунок для замовлення #%s: %s", order.id, str(data)[:300])
        return None
    order.mono_invoice_id = data['invoiceId']
    order.save(update_fields=['mono_invoice_id'])
    return data['pageUrl']


@login_required
@post_required('cart_detail')
@terms_required('/cart/')
def pay_with_mono(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()

    if not cart.items.exists():
        messages.error(request, "Ваш кошик порожній.")
        return redirect('materials_list')

    if request.POST.get('agree') != 'on':
        messages.error(request, "Щоб перейти до оплати, поставте галочку про згоду з умовами "
                                "і з відкриттям матеріалів одразу після оплати.")
        return redirect('cart_detail')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total_amount=total_price,
            status='pending',
            instant_access_agreed_at=timezone.now(),
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, material=item.material, price=item.material.price)

    page_url = create_mono_invoice(order, int(total_price * 100))
    if page_url:
        return redirect(page_url)
    messages.error(request, "Помилка платіжної системи. Спробуйте пізніше або спишіть з балансу.")
    return redirect('cart_detail')


@login_required
@terms_required('/cabinet/')
def topup_balance_view(request):
    if request.method == 'POST':
        amount = to_int(request.POST.get('amount'))
        if amount is None or not 1 <= amount <= 100000:
            messages.error(request, "Введіть коректну суму (ціле число гривень від 1 до 100 000).")
            return redirect('cabinet')

        order = Order.objects.create(
            user=request.user,
            total_amount=amount,
            status='pending',
            source='web'
        )

        page_url = create_mono_invoice(order, amount * 100)
        if page_url:
            return redirect(page_url)
        messages.error(request, "Помилка платіжної системи. Спробуйте пізніше.")
        return redirect('cabinet')

    return redirect('cabinet')


def apply_mono_status(invoice_id, status):
    msg = None
    with transaction.atomic():
        order = Order.objects.select_for_update().filter(mono_invoice_id=invoice_id).first()
        if order is None:
            return None
        email = html.escape(order.buyer_email)
        if order.user_id is None:
            if status == 'success' and order.status in ('pending', 'cancelled'):
                order.status = 'paid'
                order.paid_at = timezone.now()
                order.save(update_fields=['status', 'paid_at'])
                msg = (f"⚠️ <b>Оплата за замовленням видаленого акаунта</b>\nЗамовлення #{order.id}, {email}, "
                       f"{order.total_amount} ₴. Зв'яжіться з покупцем і за потреби поверніть кошти.")
            elif status in ('failure', 'expired') and order.status == 'pending':
                order.status = 'cancelled'
                order.save(update_fields=['status'])
            elif status == 'reversed' and order.status in ('pending', 'paid', 'cancelled'):
                order.status = 'refunded'
                order.save(update_fields=['status'])
        elif status == 'success' and order.status in ('pending', 'cancelled'):
            order.status = 'paid'
            order.paid_at = timezone.now()
            order.save(update_fields=['status', 'paid_at'])

            order_items = list(order.items.select_related('material').defer('material__html_content'))
            if order_items:
                materials = [item.material for item in order_items if item.material]
                for material in materials:
                    if material.is_bundle:
                        for sub_material in material.included_materials.all():
                            order.user.purchased_materials.add(sub_material)
                    else:
                        order.user.purchased_materials.add(material)

                CartItem.objects.filter(cart__user=order.user, material__in=materials).delete()
                msg = f"🛒 Нова покупка!\nУчень: {email}\nОплачено: {order.total_amount} ₴"
            else:
                User.objects.filter(pk=order.user_id).update(balance=F('balance') + int(order.total_amount))
                msg = f"💰 Нове поповнення!\nУчень: {email}\nСума: {order.total_amount} ₴"

        elif status in ('failure', 'expired') and order.status == 'pending':
            order.status = 'cancelled'
            order.save(update_fields=['status'])

        elif status == 'reversed' and order.status in ('pending', 'paid', 'cancelled'):
            was_paid = order.status == 'paid'
            order.status = 'refunded'
            order.save(update_fields=['status'])
            if was_paid:
                what = "матеріали з замовлення" if order.items.exists() else "суму поповнення з балансу"
                msg = (f"↩️ <b>Повернення коштів через Monobank</b>\nЗамовлення #{order.id}, {email}, "
                       f"{order.total_amount} ₴.\nАвтоматично нічого не змінено — за потреби заберіть {what} в адмінці.")

    if msg:
        send_telegram_notification(msg)
    return order


def check_mono_invoice(order):
    if not order.mono_invoice_id or order.mono_invoice_id == 'balance_payment':
        return order
    try:
        response = requests.get(f"{MONO_API_URL}/invoice/status", params={'invoiceId': order.mono_invoice_id},
                                headers=mono_headers(), timeout=10)
        response.raise_for_status()
        status = response.json().get('status')
    except Exception:
        logger.warning("Не вдалося перевірити статус рахунку Monobank для замовлення #%s", order.id, exc_info=True)
        return order
    return apply_mono_status(order.mono_invoice_id, status) or order


@login_required
def payment_result(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ('pending', 'cancelled'):
        order = check_mono_invoice(order)
    return render(request, 'materials/payment_result.html', {
        'order': order,
        'is_topup': not order.items.exists(),
    })


MONO_PUBKEY_URL = "https://api.monobank.ua/api/merchant/pubkey"
MONO_PUBKEY_CACHE_KEY = 'monobank_pubkey'
MONO_PUBKEY_REFRESHED_KEY = 'monobank_pubkey_refreshed'


class MonoPubKeyUnavailable(Exception):
    pass


def get_mono_pubkey(force_refresh=False):
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
        return False


def verify_mono_signature(body, x_sign):
    if not x_sign:
        return False
    try:
        signature = base64.b64decode(x_sign, validate=True)
    except Exception:
        return False

    if _signature_matches(get_mono_pubkey(), signature, body):
        return True

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
        logger.error("Webhook Monobank: не вдалося отримати ключ: %s", e)
        return HttpResponse("Temporary error", status=503)

    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponse("Error", status=400)

    invoice_id = data.get('invoiceId')
    if invoice_id:
        apply_mono_status(invoice_id, data.get('status'))
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
@post_required('cabinet')
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

    if rate_limit_exceeded(f'review:user:{request.user.pk}', limit=5, window=60 * 60):
        messages.error(request, "Ви вже надіслали кілька відгуків. Спробуйте пізніше.")
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
            q_result['correct_answer'] = next((opt for opt in q.options.all() if opt.is_correct), None)
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
    return render(request, 'materials/practice_results.html', context)


@login_required
def report_question_error(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            data = None
        if not isinstance(data, dict):
            return JsonResponse({'status': 'error', 'message': 'Некоректні дані'}, status=400)
        try:
            question_id = to_int(data.get('question_id'))
            message = str(data.get('message') or '').strip()[:2000]
            if not message:
                return JsonResponse({'status': 'error', 'message': 'Опишіть помилку'}, status=400)

            if rate_limit_exceeded(f'question-error:user:{request.user.pk}', limit=20, window=60 * 60):
                return JsonResponse({'status': 'error', 'message': 'Забагато скарг. Спробуйте пізніше.'}, status=429)

            question = get_object_or_404(Question, id=question_id)

            QuestionError.objects.create(
                question=question,
                user=request.user,
                message=message
            )

            msg = f"🚨 <b>СКАРГА НА ЗАВДАННЯ!</b>\n\n"
            msg += f"<b>ID Завдання:</b> {question.id}\n"
            msg += f"<b>Учень:</b> {html.escape(request.user.email)}\n\n"
            msg += f"<b>Що не так:</b> <i>{html.escape(message)}</i>\n\n"
            msg += f"Зайди в адмінку (розділ 'Скарги на завдання'), щоб виправити."

            send_telegram_notification(msg)

            return JsonResponse({'status': 'success'})
        except Http404:
            return JsonResponse({'status': 'error', 'message': 'Завдання не знайдено'}, status=404)
        except Exception:
            logger.exception("Помилка збереження скарги на завдання")
            return JsonResponse({'status': 'error', 'message': 'Не вдалося надіслати скаргу'}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)


def parent_dashboard_view(request, parent_token):
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved')

    presentations = StudentPresentation.objects.filter(student=student_request.user).order_by('-created_at')

    context = {
        'student': student_request,
        'presentations': presentations,
    }

    if student_request.course == 'nmt':
        attempts = (PracticeAttempt.objects.filter(user=student_request.user).select_related('material')
                    .defer('material__html_content').order_by('-created_at'))
        context['attempts'] = attempts
        context['is_nmt'] = True
        passed = list(parent_viewable_materials(student_request))

        def topic_number(material):
            match = re.match(r'^(\d+)', material.title)
            return int(match.group(1)) if match else 99999

        context['passed_materials'] = sorted(passed, key=topic_number)
    else:
        reports = StudentReport.objects.filter(student=student_request).order_by('-date')
        context['reports'] = reports
        context['is_nmt'] = False

    return render(request, 'materials/parent_dashboard.html', context)


def parent_viewable_materials(student_request):
    return (StudyMaterial.objects.filter(attempts__user_id=student_request.user_id)
            .filter(Q(is_published=True) | Q(id__in=student_request.user.purchased_materials.values('id')))
            .exclude(html_content__isnull=True).exclude(html_content='')
            .exclude(title=DIAGNOSTIC_MATERIAL_TITLE).distinct())


def parent_view_material(request, parent_token, material_id):
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved',
                                        course='nmt')
    material = get_object_or_404(parent_viewable_materials(student_request), id=material_id)

    response = render(request, 'materials/reader.html', {
        'material': material,
        'is_personal': True,
        'back_url': reverse('parent_dashboard', args=[parent_token]),
    })
    response['Referrer-Policy'] = 'no-referrer'
    return response


def parent_view_presentation(request, parent_token, presentation_id):
    student_request = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved')
    presentation = get_object_or_404(StudentPresentation, id=presentation_id, student=student_request.user)

    context = {
        'material': presentation,
        'is_personal': True,
        'back_url': reverse('parent_dashboard', args=[parent_token]),
    }
    response = render(request, 'materials/reader.html', context)
    response['Referrer-Policy'] = 'no-referrer'
    return response


@login_required
@post_required('cabinet')
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
@post_required('cabinet')
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
        student_req = get_object_or_404(TutorStudentRequest, parent_token=parent_token, status='approved')

        rating = parse_rating(request.POST.get('rating', 5))
        text = request.POST.get('text', '').strip()
        reviewer_name = request.POST.get('reviewer_name', '').strip()[:100]

        if not text or not reviewer_name or rating is None:
            messages.error(request, "Будь ласка, введіть своє ім'я, оцінку та текст відгуку.")
            return redirect('parent_dashboard', parent_token=parent_token)

        if rate_limit_exceeded(f'parent-review:{student_req.pk}', limit=3, window=60 * 60):
            messages.error(request, "Ви вже надіслали кілька відгуків. Спробуйте пізніше.")
            return redirect('parent_dashboard', parent_token=parent_token)

        Review.objects.create(
            user=student_req.user,
            reviewer_name=reviewer_name,
            rating=rating,
            text=text
        )

        msg = f"⭐️ <b>Новий відгук від батьків!</b>\n\n"
        msg += f"Від: <b>{html.escape(reviewer_name)}</b> <i>(Батьки учня: {html.escape(student_req.real_name)})</i>\n"
        msg += f"Оцінка: {'⭐' * rating}\n\n"
        msg += f"<i>«{html.escape(text)}»</i>\n\n"
        msg += f"Зайди в адмінку, щоб схвалити публікацію на головній сторінці."

        send_telegram_notification(msg)

        messages.success(request, "Щиро дякуємо за ваш відгук! Ваша думка дуже важлива для нас.")

    return redirect('parent_dashboard', parent_token=parent_token)
def math_sprint_game(request):
  """Ігровий тренажер 'Математичний Спринт (60 секунд)'."""
  import json
  import random
  from django.http import JsonResponse
  from django.shortcuts import render
  from django.utils import timezone
  from .models import Question, StudyMaterial

  # POST: збереження результату та щоденний бонус на баланс
  if request.method == 'POST':
    if not request.user.is_authenticated:
      return JsonResponse({
          'rewarded': False,
          'message': (
              'Зареєструйтеся на платформі, щоб зберігати рекорди та отримувати'
              ' бонусні бали!'
          ),
      })
    try:
      data = json.loads(request.body)
      correct_count = int(data.get('correct_count', 0))
    except (ValueError, TypeError, json.JSONDecodeError):
      correct_count = 0

    today_str = str(timezone.localdate())
    last_reward_date = request.session.get('sprint_reward_date')

    if correct_count >= 5 and last_reward_date != today_str:
      request.user.balance = (request.user.balance or 0) + 2
      request.user.save(update_fields=['balance'])
      request.session['sprint_reward_date'] = today_str
      return JsonResponse({
          'rewarded': True,
          'message': (
              '🎁 Вітаємо! Ви дали 5+ правильних відповідей і отримали +2'
              ' бонусні бали на баланс!'
          ),
      })

    return JsonResponse({
        'rewarded': False,
        'message': (
            '👏 Чудовий результат! Щоденний бонус (+2 бали) сьогодні вже'
            ' нараховано.'
            if last_reward_date == today_str
            else (
                'Наберіть щонайменше 5 правильних відповідей за хвилину, щоб'
                ' отримати +2 бонусні бали!'
            )
        ),
    })

  # GET: визначаємо доступні теми залежно від ролі користувача
  user = request.user
  if user.is_authenticated and (
      user.is_staff
      or user.is_superuser
      or getattr(user, 'role', '') == 'teacher'
  ):
    available_materials = StudyMaterial.objects.filter(is_bundle=False)
    access_label = 'Повний доступ викладача'
  elif user.is_authenticated:
    purchased_ids = list(
        user.purchased_materials.values_list('id', flat=True)
    )
    free_ids = list(
        StudyMaterial.objects.filter(is_free=True).values_list('id', flat=True)
    )
    available_materials = StudyMaterial.objects.filter(
        id__in=set(purchased_ids + free_ids), is_bundle=False
    )
    access_label = 'Ваші відкриті та безкоштовні теми'
  else:
    available_materials = StudyMaterial.objects.filter(
        is_free=True, is_bundle=False
    )
    access_label = 'Безкоштовні демо-теми'

  selected_material = None
  material_id = request.GET.get('material_id')
  if material_id and material_id.isdigit():
    selected_material = available_materials.filter(id=int(material_id)).first()

  # Безпечна для PostgreSQL вибірка випадкових ID питань без .distinct().order_by('?')
  base_qs = Question.objects.filter(question_type='CHOICE')
  if selected_material:
    base_qs = base_qs.filter(materials=selected_material)
  elif available_materials.exists():
    base_qs = base_qs.filter(materials__in=available_materials)

  all_q_ids = list(set(base_qs.values_list('id', flat=True)))
  sampled_ids = random.sample(all_q_ids, min(len(all_q_ids), 30))

  qs = Question.objects.filter(id__in=sampled_ids).prefetch_related('options')

  questions_list = []
  for q in qs:
    opts = [
        {'text': o.body, 'is_correct': o.is_correct} for o in q.options.all()
    ]
    if len(opts) >= 2 and any(o['is_correct'] for o in opts):
      questions_list.append({
          'id': q.id,
          'text': q.text,
          'svg_code': q.svg_code or '',
          'options': opts,
      })

  return render(
      request,
      'materials/math_sprint.html',
      {
          'available_materials': available_materials,
          'selected_material': selected_material,
          'access_label': access_label,
          'questions_list': questions_list,
      },
  )
