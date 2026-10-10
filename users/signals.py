from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .analytics import queue_event


@receiver(user_signed_up)
def track_sign_up(request, user, **kwargs):
    if request is not None and hasattr(request, 'session'):
        queue_event(request, 'sign_up', {'method': 'google' if kwargs.get('sociallogin') else 'email'})
