from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy, pgettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.mixins import ProtectedDeleteMixin

from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labeles.html'
    login_url = reverse_lazy('login')


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ('name',)
    template_name = 'create_entity.html'
    extra_context = {
        'entity': pgettext_lazy('create', 'label'),
    }
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully created')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'update_entity.html'
    extra_context = {
        'entity': pgettext_lazy('edit', 'label'),
    }
    fields = ('name',)
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully modified')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, ProtectedDeleteMixin, DeleteView):
    model = Label
    template_name = 'deletion_confirmation.html'
    extra_context = {
        'entity': gettext_lazy('label'),
        'cancel_url': reverse_lazy('labels'),
    }
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully deleted')
    protected_message = gettext_lazy('The label cannot be deleted because it is in use')
