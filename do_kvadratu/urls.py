from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ІМПОРТ ALLAUTH ДЛЯ БЕЗПЕЧНОЇ АВТОРИЗАЦІЇ
from allauth.account import views as allauth_views

from .admin_security import rate_limited_admin_login

# Вхід в адмінку з лімітом невдалих спроб (захист від підбору пароля)
admin.site.login = rate_limited_admin_login(admin.site.login)

# ІМПОРТ З MATERIALS
from materials.views import (
    MaterialListView,
    MaterialDetailView,
    api_materials_list,
    CabinetView,
    download_material_view,
    api_bot_user_library,
    HomeView,
    AboutView,
    cart_detail,
    add_to_cart,
    remove_from_cart,
    pay_from_balance,
    pay_with_mono,
    mono_webhook,
    payment_result,
    topup_balance_view,
    diagnostic_test_view,
    OfferView,
    PrivacyView,
    booking_view,
    practice_session_view,
    request_tutor_student_status,
    submit_review,
    view_student_presentation,
    view_attempt_details,
    report_question_error,
    parent_dashboard_view,
    add_quick_report,
    add_nmt_score,
    parent_view_presentation,
    submit_parent_review
)

urlpatterns = [
    # ХОВАЄМО АДМІНКУ
    path('do-kvadratu-secret-control/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('materials/', MaterialListView.as_view(), name='materials_list'),

    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:material_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

    # ==========================================
    # БЕЗПЕЧНА АВТОРИЗАЦІЯ (ALLAUTH)
    # ==========================================
    path('register/', allauth_views.signup, name='register'),
    path('login/', allauth_views.login, name='login'),
    path('logout/', allauth_views.logout, name='logout'),
    path('accounts/', include('allauth.urls')),  # Залишаємо для внутрішньої логіки Google та Allauth

    path('api/materials/', api_materials_list),
    path('cabinet/', CabinetView.as_view(), name='cabinet'),

    path('download/<int:material_id>/', download_material_view, name='download_material'),
    path('practice/<int:material_id>/', practice_session_view, name='practice_session'),
    path('api/bot/library/<str:telegram_id>/', api_bot_user_library),
    path('material/<int:pk>/', MaterialDetailView.as_view(), name='material_detail'),
    path('about/', AboutView.as_view(), name='about'),

    path('cart/pay/balance/', pay_from_balance, name='pay_from_balance'),
    path('cart/pay/mono/', pay_with_mono, name='pay_with_mono'),
    path('mono/webhook/', mono_webhook, name='mono_webhook'),
    path('payment/result/<int:order_id>/', payment_result, name='payment_result'),
    path('cabinet/topup/', topup_balance_view, name='topup_balance'),

    # Відновлення пароля — через allauth (/accounts/password/reset/): з лімітами
    # і для акаунтів, створених через Google. Стара адреса лише перенаправляє.
    path('reset_password/', RedirectView.as_view(pattern_name='account_reset_password'), name="reset_password"),
    # Посилання з листів, надісланих ще старою формою (діють 3 дні); можна прибрати після 20.10.2026
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),

    # Діагностичний тест
    path('diagnostic/', diagnostic_test_view, name='diagnostic_test'),

    # Юридичні документи
    path('offer/', OfferView.as_view(), name='offer'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('bot/', include('telegram_bot.urls')),

    # Календар запису
    path('booking/', booking_view, name='booking'),
    path('request-student/', request_tutor_student_status, name='request_student_status'),
    path('submit-review/', submit_review, name='submit_review'),
    path('lesson/<int:presentation_id>/', view_student_presentation, name='view_student_presentation'),
    path('attempt/<int:attempt_id>/', view_attempt_details, name='view_attempt_details'),
    path('api/report-error/', report_question_error, name='report_question_error'),

    # ФАЙЛ ДЛЯ ПОШУКОВИХ БОТІВ GOOGLE
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    # Діагностичний тест
    path('diagnostic/', diagnostic_test_view, name='diagnostic_test'),

    # Дашборд для батьків
    path('parents/<uuid:parent_token>/', parent_dashboard_view, name='parent_dashboard'),
    path('cabinet/add-report/', add_quick_report, name='add_quick_report'),
    path('cabinet/add-nmt-score/', add_nmt_score, name='add_nmt_score'),
    path('parents/<uuid:parent_token>/lesson/<int:presentation_id>/', parent_view_presentation, name='parent_view_presentation'),
    path('parents/<uuid:parent_token>/review/', submit_parent_review, name='submit_parent_review'),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)