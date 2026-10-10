from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class TermsAcceptanceMiddleware:
    """Хто ще не погодився з поточною редакцією оферти (вхід через Google, акаунти, створені
    до появи запису згоди, або після зміни TERMS_VERSION), спершу потрапляє на /accept-terms/.

    Перехоплюються лише переходи між сторінками (GET): форми й запити зі сторінок, які вже відкрито,
    не ламаються. Викладач/адміністратор, сторінки входу-виходу, самі документи, вебхуки й
    сторінка результату оплати — без перевірки. Уже придбане (читалка, практика, презентації занять)
    відкривається й без нової згоди: так обіцяє оферта (п. 23.3), а посилання на ці сторінки
    є на /accept-terms/.
    """

    EXEMPT_PREFIXES = (
        '/accept-terms/', '/login/', '/logout/', '/register/', '/accounts/',
        '/offer/', '/privacy/', '/do-kvadratu-secret-control/',
        '/bot/', '/mono/', '/api/', '/payment/result/', '/parents/',
        '/download/', '/practice/', '/lesson/', '/attempt/',
        '/robots.txt', '/sitemap.xml', '/favicon.ico',
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt = self.EXEMPT_PREFIXES + tuple(
            p for p in (settings.STATIC_URL, settings.MEDIA_URL) if p and p.startswith('/'))

    def __call__(self, request):
        if request.method == 'GET' and not request.path.startswith(self.exempt):
            user = getattr(request, 'user', None)
            if (user is not None and user.is_authenticated and not (user.is_staff or user.is_superuser)
                    and not user.has_accepted_current_terms):
                return redirect(f"{reverse('accept_terms')}?{urlencode({'next': request.get_full_path()})}")
        return self.get_response(request)
