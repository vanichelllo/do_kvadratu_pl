
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import escape_uri_path

from .models import Cart


def promo(request):
    """Банери акції показуються лише в її дати (за київським часом), як і знижка в кошику."""
    return {
        'promo_active': Cart.promo_is_active(),
        'promo_start': Cart.PROMO_START,
        'promo_end': Cart.PROMO_END,
    }


HALLOWEEN_START = (10, 17)  # (місяць, день) — щороку, включно
HALLOWEEN_END = (11, 1)


def seasonal(request):
    """Святкове оформлення головної — лише в його дати (за київським часом)."""
    today = timezone.localdate()
    return {'halloween_active': HALLOWEEN_START <= (today.month, today.day) <= HALLOWEEN_END}


def seo(request):
    # Канонічна адреса сторінки — без параметрів пошуку й завжди на основному домені
    return {
        'SITE_URL': settings.SITE_URL,
        'canonical_url': settings.SITE_URL + escape_uri_path(request.path),
    }
