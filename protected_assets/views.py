from __future__ import unicode_literals

import os
import urllib

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import is_safe_url
from django.views.static import serve

from filebrowser_safe.settings import DIRECTORY as FILEBROWSER_DIRECTORY
from mezzanine.conf import settings

from .forms import AgreementForm
from .models import Agreement, SignedAgreement


@login_required
def protected_download(request, path):
    """Check for a signed download agreement before delivering the asset."""
    settings.use_editable()
    agreement = SignedAgreement.objects.filter(
        user=request.user, agreement__version=settings.DOWNLOAD_AGREEMENT_VERSION)
    if not agreement.exists():
        params = {'next': request.path}
        previous = request.META.get('HTTP_REFERER', None) or None
        if previous is not None:
            params['next'] = previous
            request.session['waiting_download'] = request.path
        agreement_url = '%s?%s' % (
            reverse('protected_assets.sign_agreement'),
            urllib.urlencode(params))
        return redirect(agreement_url)
    if settings.DEBUG:
        response = serve(request, path, document_root=os.path.join(settings.MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'protected'))
    else:
        response = HttpResponse()
        response['X-Accel-Redirect'] = '/__protected__/%s' % path
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(path)
    if request.path == request.session.get('waiting_download'):
         del request.session['waiting_download']
    if request.path == request.session.get('ready_download'):
         del request.session['ready_download']
    return response


@login_required
def sign_agreement(request):
    """Display the user agreement and allow the user to sign it."""
    settings.use_editable()

    form = AgreementForm()
    agreement = get_object_or_404(Agreement, version=settings.DOWNLOAD_AGREEMENT_VERSION)

    if request.method == "POST":
        form = AgreementForm(request.POST)
        if form.is_valid():
            ip = (request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
                  or request.META.get('REMOTE_ADDR'))
            SignedAgreement.objects.create(
                user=request.user,
                ip=ip,
                agreement=agreement,
            )
            redirect_field_name = 'next'
            default_next = '/'
            next_page = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name))
            next_page = next_page or default_next
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = default_next
            if 'waiting_download' in request.session:
                request.session['ready_download'] = request.session['waiting_download']
                del request.session['waiting_download']
            return redirect(next_page)

    return render(request, 'protected_assets/download-agreement.html', {
        'form': form,
        'agreement': agreement,
    })
