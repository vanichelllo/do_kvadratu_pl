import os
import io
import base64
import hashlib
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
from django.conf import settings

from users.forms import UserProfileForm
from .models import StudyMaterial, Category, Cart, CartItem, Order, OrderItem, Question, AnswerOption, DiagnosticTopic, \
    MatchItem, PracticeAttempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudyMaterialSerializer, PurchasedMaterialSerializer

User = get_user_model()


def diagnostic_test_view(request):
    questions = Question.objects.all().prefetch_related('options', 'match_items')

    if request.method == 'POST':
        topics_stats = {}
        for topic in DiagnosticTopic.objects.all():
            topics_stats[topic.name] = {
                'topic': topic,
                'correct': 0,
                'total': 0
            }

        total_score = 0
        max_score = 0

        for question in questions:
            topic_name = question.topic.name

            if question.question_type == 'CHOICE':
                topics_stats[topic_name]['total'] += 1
                max_score += 1

                user_answer = request.POST.get(f'question_{question.id}')
                if user_answer:
                    try:
                        selected_option = AnswerOption.objects.get(id=int(user_answer))
                        if selected_option.is_correct:
                            total_score += 1
                            topics_stats[topic_name]['correct'] += 1
                    except AnswerOption.DoesNotExist:
                        pass

            elif question.question_type == 'MATCH':
                topics_stats[topic_name]['total'] += 3
                max_score += 3

                match_correct_count = 0
                for item in question.match_items.all():
                    user_match_answer = request.POST.get(f'match_{item.id}')
                    if user_match_answer and int(user_match_answer) == item.correct_option.id:
                        match_correct_count += 1

                total_score += match_correct_count
                topics_stats[topic_name]['correct'] += match_correct_count

            elif question.question_type == 'SHORT':
                topics_stats[topic_name]['total'] += 2
                max_score += 2

                user_answer = request.POST.get(f'question_{question.id}')
                if user_answer:
                    user_clean = str(user_answer).strip().replace(',', '.')
                    correct_clean = str(question.correct_short_answer).strip().replace(',', '.')
                    if user_clean == correct_clean:
                        total_score += 2
                        topics_stats[topic_name]['correct'] += 2

        weak_topics = []
        for stat in topics_stats.values():
            if stat['total'] > 0:
                percent = (stat['correct'] / stat['total']) * 100
                if percent < 50:
                    weak_topics.append(stat['topic'])

        # === МАГІЯ РЕКОМЕНДАЦІЙ ===
        recommended_materials = set()
        for topic in weak_topics:
            # Шукаємо конспекти, у назві яких міститься ім'я слабкої теми
            mats = StudyMaterial.objects.filter(
                title__icontains=topic.name,
                is_published=True
            )
            for mat in mats:
                recommended_materials.add(mat)
        # ==========================

        percent_total = int((total_score / max_score) * 100) if max_score > 0 else 0

        # === СОРТУВАННЯ ЗА НОМЕРОМ ===
        def extract_number(text):
            match = re.match(r'^(\d+)', text)
            if match:
                return int(match.group(1))
            return 99999

        weak_topics.sort(key=lambda t: extract_number(t.name))
        recommendations_list = list(recommended_materials)
        recommendations_list.sort(key=lambda m: extract_number(m.title))
        sorted_stats = sorted(topics_stats.values(), key=lambda s: extract_number(s['topic'].name))

        context = {
            'total_score': total_score,
            'max_score': max_score,
            'percent_total': percent_total,
            'weak_topics': weak_topics,
            'topics_stats': sorted_stats,
            'recommendations': recommendations_list,
        }
        return render(request, 'materials/diagnostic_results.html', context)

    return render(request, 'materials/diagnostic_test.html', {'questions': questions})


# ==========================================
# НОВИЙ ВУЗОЛ: ПРАКТИКА НМТ ПІСЛЯ УРОКУ
# ==========================================
@login_required
def practice_session_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    # ПЕРЕВІРКА ВІДПОВІДЕЙ ТА ЗБЕРЕЖЕННЯ (Режим POST)
    if request.method == 'POST':
        total_score = 0
        max_score = 0

        # Отримуємо рядок з ID питань і перетворюємо у список
        question_ids_str = request.POST.get('question_ids', '')
        if question_ids_str:
            q_id_list = [int(x) for x in question_ids_str.split(',')]
        else:
            q_id_list = []

        questions = Question.objects.filter(id__in=q_id_list).prefetch_related('options', 'match_items')

        for q in questions:
            if q.question_type == 'CHOICE':
                max_score += 1
                user_ans = request.POST.get(f'q_{q.id}')
                if user_ans:
                    try:
                        opt = AnswerOption.objects.get(id=int(user_ans))
                        if opt.is_correct:
                            total_score += 1
                    except AnswerOption.DoesNotExist:
                        pass

            elif q.question_type == 'MATCH':
                max_score += 3
                for item in q.match_items.all():
                    user_match = request.POST.get(f'match_{item.id}')
                    if user_match and int(user_match) == item.correct_option.id:
                        total_score += 1

            elif q.question_type == 'SHORT':
                max_score += 2
                user_ans = request.POST.get(f'q_{q.id}')
                if user_ans:
                    user_clean = str(user_ans).strip().replace(',', '.')
                    correct_clean = str(q.correct_short_answer).strip().replace(',', '.')
                    if user_clean == correct_clean:
                        total_score += 2

        # Зберігаємо результат у базу
        PracticeAttempt.objects.create(
            user=request.user,
            material=material,
            score=total_score,
            max_score=max_score
        )

        messages.success(request, f"🎯 Практику завершено! Ваш результат: {total_score} з {max_score} балів.")
        return redirect('cabinet')

    # ГЕНЕРАЦІЯ НОВОГО ВАРІАНТА (Режим GET)
    pool = Question.objects.filter(materials=material).prefetch_related('options', 'match_items')

    choice_pool = list(pool.filter(question_type='CHOICE'))
    match_pool = list(pool.filter(question_type='MATCH'))
    short_pool = list(pool.filter(question_type='SHORT'))

    q_choice = random.sample(choice_pool, min(10, len(choice_pool)))
    q_match = random.sample(match_pool, min(2, len(match_pool)))
    q_short = random.sample(short_pool, min(1, len(short_pool)))

    # Перемішуємо тільки тестові питання
    random.shuffle(q_choice)

    selected_questions = q_choice + q_match + q_short

    if len(selected_questions) == 0:
        messages.info(request, "Для цієї теми ще не додано практичних завдань.")
        return redirect('cabinet')

    # Збираємо ID для прихованого поля форми
    question_ids_str = ','.join(str(q.id) for q in selected_questions)

    context = {
        'material': material,
        'q_choice': q_choice,
        'q_match': q_match,
        'q_short': q_short,
        'question_ids_str': question_ids_str,
        'total_selected': len(selected_questions)
    }

    return render(request, 'materials/practice_session.html', context)


# ==========================================


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'materials/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    if material in request.user.purchased_materials.all():
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
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, "Матеріал видалено з кошика.")
    return redirect('cart_detail')


class HomeView(TemplateView):
    template_name = 'materials/home.html'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.object

        if material.is_bundle:
            total_original_price = sum(item.price for item in material.included_materials.all())
            context['total_original_price'] = total_original_price
            context['savings'] = total_original_price - material.price

        return context


class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'materials/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        purchased_qs = self.request.user.purchased_materials.all()
        purchased_list = list(purchased_qs)

        def get_number(material):
            match = re.match(r'^(\d+)', material.title)
            if match:
                return int(match.group(1))
            return 99999

        purchased_list.sort(key=get_number)

        context['purchased_materials'] = purchased_list
        context['form'] = UserProfileForm(instance=self.request.user)
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

    if material not in request.user.purchased_materials.all():
        raise Http404("У вас немає доступу до цього матеріалу.")

    # ПЕРЕВІРКА НА ІНТЕРАКТИВНУ ПРЕЗЕНТАЦІЮ
    if getattr(material, 'html_content', None):
        html_code = material.html_content

        # МАГІЯ: Динамічно генеруємо кнопку "Практика НМТ"
        practice_btn = f'''
            <a href="/practice/{material.id}/" class="btn-primary" style="background-color: var(--brand-yellow); color: #fff; text-decoration: none; margin-right: 15px; border-radius: 6px; padding: 7px 15px; font-weight: bold;">
                🎯 Практика НМТ
            </a>
        '''

        # Вставляємо кнопку ПЕРЕД блоком <div class="nav-controls">
        html_code = html_code.replace('<div class="nav-controls">', f'{practice_btn}<div class="nav-controls">')

        return HttpResponse(html_code)

    # ЯКЩО HTML НЕМАЄ - ПРАЦЮЄМО З PDF
    if not material.file:
        raise Http404("Файл ще не завантажено на сервер.")

    try:
        file_url = material.file.url
        if file_url.startswith('http://'):
            file_url = file_url.replace('http://', 'https://')

        response = requests.get(file_url, timeout=10)

        if response.status_code == 200:
            file_bytes = response.content
        else:
            raise Exception(f"Cloudinary повернув статус: {response.status_code}")

    except Exception as e:
        raise Http404(f"Помилка завантаження файлу з хмари. Деталі: {e}")

    pdf_base64 = base64.b64encode(file_bytes).decode('utf-8')

    context = {
        'material': material,
        'pdf_base64': pdf_base64
    }
    return render(request, 'materials/reader.html', context)


@login_required(login_url='/login/')
def buy_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    my_user = request.user

    if material in my_user.purchased_materials.all():
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
def pay_from_balance(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()

    if not cart.items.exists():
        messages.error(request, "Ваш кошик порожній.")
        return redirect('materials_list')

    if request.user.balance >= total_price:
        with transaction.atomic():
            request.user.balance -= total_price
            request.user.save()

            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,
                status='paid',
                mono_invoice_id='balance_payment'
            )

            for item in cart.items.all():
                if item.material.is_bundle:
                    for sub_material in item.material.included_materials.all():
                        request.user.purchased_materials.add(sub_material)
                else:
                    request.user.purchased_materials.add(item.material)

                OrderItem.objects.create(
                    order=order,
                    material=item.material,
                    price=item.material.price
                )

            cart.items.all().delete()

        messages.success(request,
                         f"Оплата пройшла успішно! Списано {total_price} ₴. Матеріали вже у вашому кабінеті. 🎉")
        return redirect('cabinet')
    else:
        messages.error(request, "На вашому балансі недостатньо коштів. Будь ласка, оберіть оплату карткою (Monobank).")
        return redirect('cart_detail')


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
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Помилка відправки в Telegram: {e}")


@login_required
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
        "redirectUrl": "https://dokvadratu.onrender.com/cabinet/",
        "webHookUrl": "https://dokvadratu.onrender.com/mono/webhook/",
    }

    try:
        response = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=payload, headers=headers)
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
        amount_str = request.POST.get('amount')
        try:
            amount = float(amount_str)
            if amount < 1:
                messages.error(request, "Мінімальна сума поповнення — 1 грн.")
                return redirect('cabinet')
        except (ValueError, TypeError):
            messages.error(request, "Будь ласка, введіть коректну суму.")
            return redirect('cabinet')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=amount,
                status='pending'
            )

        amount_kopecks = int(amount * 100)

        headers = {
            'X-Token': getattr(settings, 'MONOBANK_TOKEN', ''),
            'Content-Type': 'application/json'
        }

        payload = {
            "amount": amount_kopecks,
            "ccy": 980,
            "reference": str(order.id),
            "redirectUrl": "https://dokvadratu.onrender.com/cabinet/",
            "webHookUrl": "https://dokvadratu.onrender.com/mono/webhook/",
        }

        try:
            response = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=payload,
                                     headers=headers)
            data = response.json()

            if 'pageUrl' in data:
                order.mono_invoice_id = data['invoiceId']
                order.save()
                return redirect(data['pageUrl'])
            else:
                messages.error(request, "Помилка платіжної системи. Спробуйте пізніше.")
                return redirect('cabinet')
        except Exception:
            messages.error(request, "Помилка з'єднання з Monobank.")
            return redirect('cabinet')


@csrf_exempt
def mono_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            invoice_id = data.get('invoiceId')
            status = data.get('status')

            if status == 'success' and invoice_id:
                try:
                    order = Order.objects.get(mono_invoice_id=invoice_id)

                    if order.status != 'paid':
                        with transaction.atomic():
                            order.status = 'paid'
                            order.save()

                            order_items = OrderItem.objects.filter(order=order)

                            if order_items.exists():
                                for item in order_items:
                                    if item.material.is_bundle:
                                        for sub_material in item.material.included_materials.all():
                                            order.user.purchased_materials.add(sub_material)
                                    else:
                                        order.user.purchased_materials.add(item.material)

                                CartItem.objects.filter(cart__user=order.user).delete()

                                msg = f"🛒 Нова покупка!\nУчень: {order.user.email}\nОплачено: {order.total_amount} ₴"
                                send_telegram_notification(msg)

                            else:
                                order.user.balance += float(order.total_amount)
                                order.user.save()

                                msg = f"💰 Нове поповнення!\nУчень: {order.user.email}\nСума: {order.total_amount} ₴"
                                send_telegram_notification(msg)

                except Order.DoesNotExist:
                    pass

            return HttpResponse("OK", status=200)
        except Exception as e:
            print(f"Webhook Error: {e}")
            return HttpResponse("Error", status=400)

    return HttpResponse("Method not allowed", status=405)