from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy, pgettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses.html'
    login_url = reverse_lazy('login')


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ('name',)
    template_name = 'status_create.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully created')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'update_entity.html'
    extra_context = {
        'entity': pgettext_lazy('edit', 'status'),
    }
    fields = ('name',)
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully modified')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'deletion_confirmation.html'
    extra_context = {
        'entity': gettext_lazy('status'),
        'cancel_url': reverse_lazy('statuses'),
    }
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully deleted')
