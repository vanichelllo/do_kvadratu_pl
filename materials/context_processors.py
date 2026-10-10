from django.conf import settings
from django.utils.encoding import escape_uri_path

from .models import Cart


def promo(request):
    """Банери акції показуються лише в її дати (за київським часом), як і знижка в кошику."""
    return {
        'promo_active': Cart.promo_is_active(),
        'promo_start': Cart.PROMO_START,
        'promo_end': Cart.PROMO_END,
    }


def seo(request):
    # Канонічна адреса сторінки — без параметрів пошуку й завжди на основному домені
    return {
        'SITE_URL': settings.SITE_URL,
        'canonical_url': settings.SITE_URL + escape_uri_path(request.path),
    }
