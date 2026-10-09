import hashlib
from functools import wraps

from django.core.cache import cache
from django.http import HttpResponse

ADMIN_LOGIN_MAX_FAILURES = 10
ADMIN_LOGIN_WINDOW = 15 * 60  # секунд


def _failures_key(username):
    return 'admin-login-failures:' + hashlib.sha256(username.strip().lower().encode()).hexdigest()


def rate_limited_admin_login(login_view):
    """Обмежує підбір пароля на сторінці входу в адмінку.

    Рахуємо невдалі спроби для кожного email (а не IP: за проксі Render IP ненадійний,
    і ліміт за IP міг би заблокувати вхід усім одразу)."""
    @wraps(login_view)
    def wrapper(request, extra_context=None):
        if request.method != 'POST':
            return login_view(request, extra_context)

        key = _failures_key(request.POST.get('username', ''))
        if cache.get(key, 0) >= ADMIN_LOGIN_MAX_FAILURES:
            return HttpResponse(
                "Забагато невдалих спроб входу. Спробуйте через 15 хвилин.",
                status=429, content_type='text/plain; charset=utf-8')

        response = login_view(request, extra_context)
        if request.user.is_authenticated and request.user.is_staff:
            cache.delete(key)
        else:
            cache.add(key, 0, ADMIN_LOGIN_WINDOW)
            try:
                cache.incr(key)
            except ValueError:  # ключ щойно протух
                cache.set(key, 1, ADMIN_LOGIN_WINDOW)
        return response
    return wrapper
