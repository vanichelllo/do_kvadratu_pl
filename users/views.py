import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentRegistrationForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ПРЯМО ВКАЗУЄМО БЕКЕНД АВТОРИЗАЦІЇ, ЩОБ DJANGO НЕ ПЛУТАВСЯ З ALLAUTH
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('cabinet')  # Редирект у кабінет
    else:
        form = StudentRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def pay_with_mono(request):
    """Генерація посилання на оплату Monobank"""
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()

    if not cart.items.exists():
        messages.error(request, "Ваш кошик порожній.")
        return redirect('materials_list')

    # 1. Створюємо замовлення зі статусом "Очікує"
    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total_amount=total_price,
            status='pending'
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, material=item.material, price=item.material.price)

    # 2. Формуємо запит до Monobank
    amount_kopecks = int(total_price * 100)  # Монобанк приймає суму ТІЛЬКИ в копійках
    domain = request.build_absolute_uri('/')[:-1]  # Динамічно визначаємо ваш домен

    headers = {
        'X-Token': getattr(settings, 'MONOBANK_TOKEN', ''),
        'Content-Type': 'application/json'
    }

    payload = {
        "amount": amount_kopecks,
        "ccy": 980,  # Код гривні UAH
        "reference": str(order.id),
        "redirectUrl": f"{domain}/cabinet/",  # Куди повернути учня після оплати
        "webHookUrl": f"{domain}/mono/webhook/",  # Куди Моно надішле приховану відповідь
    }

    try:
        # Відправляємо запит
        response = requests.post("https://api.monobank.ua/api/merchant/invoice/create", json=payload, headers=headers)
        data = response.json()

        if 'pageUrl' in data:
            order.mono_invoice_id = data['invoiceId']
            order.save()
            return redirect(data['pageUrl'])  # Перекидаємо на чорну сторінку Monopay
        else:
            messages.error(request, "Помилка платіжної системи. Спробуйте пізніше або спишіть з балансу.")
            return redirect('cart_detail')

    except Exception as e:
        messages.error(request, "Помилка з'єднання з Monobank.")
        return redirect('cart_detail')


@csrf_exempt
def mono_webhook(request):
    """Приймає сповіщення від Monobank про успішну оплату (Вебхук)"""
    # csrf_exempt потрібен, бо запит приходить не від користувача, а від сервера Monobank
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            invoice_id = data.get('invoiceId')
            status = data.get('status')  # 'success', 'failure', 'created'

            if status == 'success':
                # Знаходимо замовлення за інвойсом
                order = Order.objects.get(mono_invoice_id=invoice_id)

                # Щоб не видати матеріали двічі, перевіряємо чи статус ще "pending"
                if order.status != 'paid':
                    order.status = 'paid'
                    order.save()

                    # Надаємо доступ учню
                    for item in order.items.all():
                        order.user.purchased_materials.add(item.material)

                    # Очищаємо його кошик
                    cart = Cart.objects.filter(user=order.user).first()
                    if cart:
                        cart.items.all().delete()

            return HttpResponse("OK", status=200)  # Обов'язково відповідаємо "OK", щоб Моно заспокоївся
        except Exception:
            return HttpResponse("Error", status=400)

    return HttpResponse("Method not allowed", status=405)