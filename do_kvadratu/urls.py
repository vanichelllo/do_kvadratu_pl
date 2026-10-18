from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect
from django.templatetags.static import static as static_url
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ІМПОРТ ALLAUTH ДЛЯ БЕЗПЕЧНОЇ АВТОРИЗАЦІЇ
from allauth.account import views as allauth_views

from .admin_security import rate_limited_admin_login
from materials.sitemaps import MaterialSitemap, StaticPagesSitemap
from users.views import accept_terms_view

# Вхід в адмінку з лімітом невдалих спроб (захист від підбору пароля)
admin.site.login = rate_limited_admin_login(admin.site.login)

# ІМПОРТ З MATERIALS
from materials import games
from materials.views import (
    AboutView,
    CabinetView,
    HomeView,
    MaterialDetailView,
    MaterialListView,
    OfferView,
    PrivacyView,
    add_nmt_score,
    add_quick_report,
    add_to_cart,
    api_bot_user_library,
    api_materials_list,
    booking_view,
    cart_detail,
    diagnostic_offer_view,
    diagnostic_test_view,
    download_material_view,
    math_sprint_game,
    mono_webhook,
    parent_dashboard_view,
    parent_view_material,
    parent_view_presentation,
    pay_from_balance,
    pay_with_mono,
    payment_result,
    practice_session_view,
    practice_check_view,
    homework_assign,
    homework_credit,
    attempt_manage,
    practice_start,
    join_teacher,
    ForTutorsView,
    tutor_trial,
    tutor_buy,
    remove_from_cart,
    report_question_error,
    request_tutor_student_status,
    submit_parent_review,
    submit_review,
    topup_balance_view,
    view_attempt_details,
    view_student_presentation,
    web_manifest,
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
    path('accept-terms/', accept_terms_view, name='accept_terms'),  # згода з офертою (вхід через Google тощо)

    path('api/materials/', api_materials_list),
    path('cabinet/', CabinetView.as_view(), name='cabinet'),

    path('download/<int:material_id>/', download_material_view, name='download_material'),
    path('practice/<int:material_id>/', practice_session_view, name='practice_session'),
    path('practice/start/', practice_start, name='practice_start'),
    path('join/<str:code>/', join_teacher, name='join_teacher'),
    path('for-tutors/', ForTutorsView.as_view(), name='for_tutors'),
    path('for-tutors/trial/', tutor_trial, name='tutor_trial'),
    path('for-tutors/buy/<int:plan_id>/<str:period>/', tutor_buy, name='tutor_buy'),
    path('practice/<int:material_id>/check/', practice_check_view, name='practice_check'),
    path('homework/assign/', homework_assign, name='homework_assign'),
    path('attempt/<int:attempt_id>/manage/', attempt_manage, name='attempt_manage'),
    path('homework/<int:homework_id>/credit/', homework_credit, name='homework_credit'),
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

    # Дашборд для батьків
    path('parents/<uuid:parent_token>/', parent_dashboard_view, name='parent_dashboard'),
    path('cabinet/add-report/', add_quick_report, name='add_quick_report'),
    path('cabinet/add-nmt-score/', add_nmt_score, name='add_nmt_score'),
    path('parents/<uuid:parent_token>/lesson/<int:presentation_id>/', parent_view_presentation, name='parent_view_presentation'),
    path('parents/<uuid:parent_token>/topic/<int:material_id>/', parent_view_material, name='parent_view_material'),
    path('parents/<uuid:parent_token>/review/', submit_parent_review, name='submit_parent_review'),
    # Карта сайту для Google: головні сторінки + усі опубліковані конспекти
    path('sitemap.xml', sitemap, {'sitemaps': {'pages': StaticPagesSitemap, 'materials': MaterialSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
    # Браузери за замовчуванням шукають іконку за цією адресою
    path('favicon.ico', lambda request: redirect(static_url('images/favicon.ico'))),
    # Телефони шукають велику іконку за цими адресами, навіть якщо сторінка її не вказала
    path('apple-touch-icon.png', lambda request: redirect(static_url('images/apple-touch-icon.png'))),
    path('apple-touch-icon-precomposed.png', lambda request: redirect(static_url('images/apple-touch-icon.png'))),
    path('site.webmanifest', web_manifest, name='web_manifest'),
    path('game/sprint/', math_sprint_game, name='math_sprint'),
    path('diagnostic/offer/', diagnostic_offer_view, name='diagnostic_offer'),
    path('game/', games.game_hub, name='game_hub'),
    path('game/pairs/', games.game_pairs, name='game_pairs'),
    path('game/input/', games.game_input, name='game_input'),
    path('game/mistakes/', games.game_mistakes, name='game_mistakes'),
    path('game/answer/', games.game_answer, name='game_answer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)