from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import register_view
from django.contrib.auth.views import LoginView, LogoutView
from materials.views import AboutView
# ВИПРАВЛЕНО: Додано MaterialDetailView та замінено cabinet_view на CabinetView
from materials.views import (
    MaterialListView,
    MaterialDetailView,
    buy_material_view,
    api_materials_list,
    CabinetView,
    download_material_view,
    api_bot_user_library,
    HomeView,
    cart_detail,
    add_to_cart,
    remove_from_cart,
    pay_from_balance,
    pay_with_mono,
    mono_webhook,
    topup_balance_view,
    diagnostic_test_view
)

urlpatterns = [
    # ХОВАЄМО АДМІНКУ: змінено стандартну адресу 'admin/' на унікальну
    path('do-kvadratu-secret-control/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('materials/', MaterialListView.as_view(), name='materials_list'),
    path('buy/<int:material_id>/', buy_material_view, name='buy_action'),

    # ВИПРАВЛЕНО: прибрано приставку views., оскільки функції імпортовано напряму
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:material_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

    # ДОДАНО name='register'
    path('register/', register_view, name='register'),

    path('api/materials/', api_materials_list),
    path('cabinet/', CabinetView.as_view(), name='cabinet'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # ВИПРАВЛЕНО: Додано name='download_material'
    path('download/<int:material_id>/', download_material_view, name='download_material'),

    path('api/bot/library/<str:telegram_id>/', api_bot_user_library),
    path('material/<int:pk>/', MaterialDetailView.as_view(), name='material_detail'),
    path('accounts/', include('allauth.urls')),
    path('about/', AboutView.as_view(), name='about'),
    path('cart/pay/balance/', pay_from_balance, name='pay_from_balance'),
    path('cart/pay/mono/', pay_with_mono, name='pay_with_mono'),
    path('mono/webhook/', mono_webhook, name='mono_webhook'),
    path('cabinet/topup/', topup_balance_view, name='topup_balance'),
    # 1. Сторінка введення email для скидання
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
         name="reset_password"),

    # 2. Повідомлення "Лист відправлено"
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),
         name="password_reset_done"),

    # 3. Сторінка введення НОВОГО пароля (сюди веде посилання з листа)
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"),
         name="password_reset_confirm"),

    # 4. Повідомлення "Пароль успішно змінено"
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),

    path('diagnostic/', diagnostic_test_view, name='diagnostic_test'),
    path('offer/', TemplateView.as_view(template_name="offer.html"), name='offer'),
    path('privacy/', TemplateView.as_view(template_name="privacy.html"), name='privacy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)