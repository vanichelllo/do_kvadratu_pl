from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


@login_required
def accept_terms_view(request):
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()},
                                           require_https=request.is_secure()):
        next_url = reverse('cabinet')

    if request.user.has_accepted_current_terms:
        return redirect(next_url)

    error = None
    if request.method == 'POST':
        if request.POST.get('terms'):
            request.user.accept_terms()
            return redirect(next_url)
        error = "Поставте галочку, щоб продовжити."

    return render(request, 'account/accept_terms.html', {'next': next_url, 'error': error})
