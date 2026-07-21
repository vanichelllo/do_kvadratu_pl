import base64
import hashlib
import ecdsa
import re
import requests
import json
import time
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
    MatchItem

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

        percent_total = int((total_score / max_score) * 100) if max_score > 0 else 0

        context = {
            'total_score': total_score,
            'max_score': max_score,
            'percent_total': percent_total,
            'weak_topics': weak_topics,
            'topics_stats': topics_stats.values(),
        }
        return render(request, 'materials/diagnostic_results.html', context)

    return render(request, 'materials/diagnostic_test.html', {'questions': questions})


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
        context['purchased_materials'] = self.request.user.purchased_materials.all()
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
# ОНОВЛЕНО: Безпечне читання матеріалу
# ==========================================
@login_required(login_url='/login/')
def download_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    # Перевірка доступу
    if material not in request.user.purchased_materials.all():
        raise Http404("У вас немає доступу до цього файлу.")

    if not material.file:
        raise Http404("Файл ще не завантажено на сервер.")

    # Читаємо файл у пам'ять і кодуємо в текст (Base64)
    file_bytes = material.file.read()
    pdf_base64 = base64.b64encode(file_bytes).decode('utf-8')

    context = {
        'material': material,
        'pdf_base64': pdf_base64
    }
    # Замість видачі файлу, відкриваємо сторінку-читалку
    return render(request, 'materials/reader.html', context)


@login_required(login_url='/login/')
def buy_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    my_user = request.user

    if material in my_user.purchased_materials.all():
        messages.info(request, f"Ви вже маєте конспект «{material.title}».")
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
    serializer = StudyMaterialSerializer(materials, many=True)
    return Response({
        'status': 'success',
        'materials': serializer.data
    })


@api_view(['GET'])
def api_bot_user_library(request, telegram_id):
    user = User.objects.filter(telegram_id=telegram_id).first()

    if not user:
        return Response({'status': 'error', 'message': 'Учня не знайдено в базі платформи.'}, status=404)

    purchased = user.purchased_materials.all()
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
    domain = request.build_absolute_uri('/')[:-1]

    headers = {
        'X-Token': getattr(settings, 'MONOBANK_TOKEN', ''),
        'Content-Type': 'application/json'
    }

    payload = {
        "amount": amount_kopecks,
        "ccy": 980,
        "reference": str(order.id),
        "redirectUrl": f"{domain}/cabinet/",
        "webHookUrl": f"{domain}/mono/webhook/",
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

        amount_kopecks = int(amount * 100)
        domain = request.build_absolute_uri('/')[:-1]

        headers = {
            'X-Token': getattr(settings, 'MONOBANK_TOKEN', ''),
            'Content-Type': 'application/json'
        }

        reference = f"topup_{request.user.id}_{int(time.time())}"

        payload = {
            "amount": amount_kopecks,
            "ccy": 980,
            "reference": reference,
            "redirectUrl": f"{domain}/cabinet/",
            "webHookUrl": f"{domain}/mono/webhook/",
        }

        try:
            response = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=payload,
                                     headers=headers)
            data = response.json()

            if 'pageUrl' in data:
                return redirect(data['pageUrl'])
            else:
                messages.error(request, "Помилка платіжної системи. Спробуйте пізніше.")
                return redirect('cabinet')
        except Exception:
            messages.error(request, "Помилка з'єднання з Monobank.")
            return redirect('cabinet')

    return redirect('cabinet')


@csrf_exempt
def mono_webhook(request):
    if request.method == 'POST':
        try:
            x_sign = request.headers.get('X-Sign')
            if not x_sign:
                return HttpResponse("Missing X-Sign", status=400)

            body_bytes = request.body

            mono_pub_key_base64 = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZrd0V3WUhLb1pJemowQ0FRWUlLb1pJemowREFRY0RRZ0FFc0NsNUJ4MWhwaXgvZ083aFVwWENwTThNdm9XRApyVlBOMlV6bXV5NUpvMHR6WjcwMmlSM29YRW1Wb3BwSW9qOGxKOFZ3aEd1T0o2bVhtYnJtQWpnWlB3PT0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t"
            mono_pub_key_pem = base64.b64decode(mono_pub_key_base64).decode('utf-8')

            try:
                vk = ecdsa.VerifyingKey.from_pem(mono_pub_key_pem)
                signature = base64.b64decode(x_sign)
                vk.verify(signature, body_bytes, sigdecode=ecdsa.util.sigdecode_der, hashfunc=hashlib.sha256)
            except ecdsa.BadSignatureError:
                return HttpResponse("Invalid Signature", status=403)

            data = json.loads(body_bytes)
            invoice_id = data.get('invoiceId')
            status = data.get('status')
            reference = data.get('reference', '')

            if status == 'success':
                if reference.startswith('topup_'):
                    parts = reference.split('_')
                    if len(parts) >= 2:
                        user_id = parts[1]
                        user = User.objects.get(id=user_id)

                        amount_uah = data.get('amount', 0) / 100
                        user.balance += amount_uah
                        user.save()

                        msg = f"💰 Нове поповнення балансу!\nУчень: {user.email}\nСума: {amount_uah} ₴"
                        send_telegram_notification(msg)
                else:
                    order = Order.objects.get(mono_invoice_id=invoice_id)
                    if order.status != 'paid':
                        order.status = 'paid'
                        order.save()

                        for item in order.items.all():
                            order.user.purchased_materials.add(item.material)

                        cart = Cart.objects.filter(user=order.user).first()
                        if cart:
                            cart.items.all().delete()

                        msg = f"🛒 Нова покупка на сайті!\nУчень: {order.user.email}\nОплачено: {order.total_amount} ₴"
                        send_telegram_notification(msg)

            return HttpResponse("OK", status=200)
        except Exception as e:
            print(f"Webhook Error: {e}")
            return HttpResponse("Error", status=400)

    return HttpResponse("Method not allowed", status=405)