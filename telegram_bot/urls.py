from django.urls import path
from .views import telegram_webhook

urlpatterns = [
    path('webhook/', telegram_webhook, name='telegram_webhook'),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
]