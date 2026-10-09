from .models import Cart


def promo(request):
    """Банери акції показуються лише в її дати (за київським часом), як і знижка в кошику."""
    return {
        'promo_active': Cart.promo_is_active(),
        'promo_start': Cart.PROMO_START,
        'promo_end': Cart.PROMO_END,
    }
