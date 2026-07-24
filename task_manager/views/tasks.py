from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy, pgettext_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..forms import TaskFilterForm
from ..models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        qs = Task.objects.all()

        self.form = TaskFilterForm(self.request.GET or None)

        if self.form.is_valid():
            data = self.form.cleaned_data
            if data['status']:
                qs = qs.filter(status=data['status'])

            if data['assignee']:
                qs = qs.filter(assignee=data['assignee'])

            if data['own_tasks']:
                qs = qs.filter(author=self.request.user)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task.html'
    login_url = reverse_lazy('login')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ('name', 'description', 'status', 'assignee')
    template_name = 'create_entity.html'
    extra_context = {
        'entity': pgettext_lazy('create', 'task'),
    }
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks')
    success_message = gettext_lazy('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'update_entity.html'
    extra_context = {
        'entity': pgettext_lazy('edit', 'task'),
    }
    fields = ('name', 'description', 'status', 'assignee')
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks')
    success_message = gettext_lazy('Task successfully modified')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'deletion_confirmation.html'
    extra_context = {
        'entity': pgettext_lazy('delete', 'task'),
        'cancel_url': reverse_lazy('tasks'),
    }
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks')
    success_message = gettext_lazy('Task successfully deleted')

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, gettext('A task can only be deleted by its author'))
        return redirect('tasks')
