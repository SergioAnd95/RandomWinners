from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .forms import CandidateForm
from .models import Candidate


class NameCreateView(CreateView):
    """
    CBV fo create new names
    """
    form_class = CandidateForm
    success_url = '/'
    template_name = 'index.html'

    def form_valid(self, form):
        form.instance.group = self.request.group_candidates

        # Handle ajax request
        if self.request.is_ajax():
            try:
                form.save()
            except IntegrityError:
                msg = _('Кандидат с таким именем уже добавлен')
                return HttpResponse(msg, status=500)
            return render(self.request, '_table_data.html', {})

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(data=form.errors, status=404)
        return super().form_invalid(form)


@require_POST
def get_winners(request):
    """
    View for get winners in group of candidate
    :param request: HttpRequest
    :return: HttpResponse
    """
    try:
        request.group_candidates.get_winners()
    except ValueError:
        msg = _('Что определить победителей нужно что б пользователей было более %d' % settings.COUNT_OF_WINNERS)
        return HttpResponse(msg, status=500)

    # Handle ajax request
    if request.is_ajax():
        return render(request, '_table_data.html', {})
    return redirect('/')


@require_POST
def refresh_winners(request):
    """
    View for refresh winners
    :param request: HttpRequest
    :return: HttpResponse
    """
    try:
        request.group_candidates.refresh_winners()
    except:
        msg = _('Что определить победителей нужно что б пользователей было более %d' % settings.COUNT_OF_WINNERS)
        return HttpResponse(msg, status=500)

    # Handle ajax request
    if request.is_ajax():
        return render(request, '_table_data.html', {})
    return redirect('/')


@require_POST
def remove_candidate(request, pk):
    name = get_object_or_404(Candidate, pk=pk, group=request.group_candidates)
    name.delete()

    # Handle ajax request
    if request.is_ajax():
        return HttpResponse('ok')
    return redirect('/')