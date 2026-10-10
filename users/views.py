from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


@login_required
def accept_terms_view(request):
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    # Лише шлях на нашому сайті: інакше redirect() сприйняв би, наприклад, «logout» як назву сторінки
    if not next_url.startswith('/') or not url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = reverse('cabinet')

    if request.user.has_accepted_current_terms:
        return redirect(next_url)

    error = None
    if request.method == 'POST':
        if request.POST.get('terms'):
            request.user.accept_terms()
            return redirect(next_url)
        error = "Поставте галочку, щоб продовжити."

    return render(request, 'account/accept_terms.html', {
        'next': next_url,
        'error': error,
        # Уже придбане лишається доступним і без нової згоди (оферта, п. 23.3)
        'owned_materials': request.user.purchased_materials.only('id', 'title').order_by('title'),
        'personal_presentations': request.user.personal_presentations.only('id', 'title').order_by('-id'),
    })


def terms_required(next_url):
    """Оплата лише після згоди з чинною редакцією оферти (сторінку могли відкрити до зміни редакції)."""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and not (user.is_staff or user.is_superuser) \
                    and not user.has_accepted_current_terms:
                return redirect(f"{reverse('accept_terms')}?next={next_url}")
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
