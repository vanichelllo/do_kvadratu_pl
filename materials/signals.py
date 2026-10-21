from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def apply_pending_cart(sender, request, user, **kwargs):
    """Що гість додав у кошик до входу — кладемо в кошик (безкоштовне — одразу в кабінет)"""
    from .models import Cart, CartItem, StudyMaterial
    from .views import PENDING_CART_KEY, user_owns_material

    if request is None or not hasattr(request, 'session'):
        return
    ids = request.session.pop(PENDING_CART_KEY, None)
    if not ids:
        return
    for material in StudyMaterial.objects.filter(id__in=ids, is_published=True).defer('html_content'):
        if user_owns_material(user, material):
            continue
        if material.is_free or material.price == 0:
            user.purchased_materials.add(*(material.included_materials.all() if material.is_bundle else [material]))
        else:
            cart, _ = Cart.objects.get_or_create(user=user)
            CartItem.objects.get_or_create(cart=cart, material=material)
