from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView, DeleteView

from .forms import RegisterForm


class UserListView(ListView):
    model = User
    template_name = 'users.html'


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'deletion_confirmation.html'
    extra_context = {
        'entity': gettext_lazy('user'),
        'cancel_url': reverse_lazy('users'),
    }
    success_url = reverse_lazy('users')
    success_message = gettext_lazy('User successfully deleted')


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = 'index'
    success_message = gettext_lazy('You are logged in')


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, gettext('You have been logged out'))
        return redirect('login')


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = gettext_lazy('The user has been successfully registered')


class UserUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'update_entity.html'
    extra_context = {
        'entity': gettext_lazy('user'),
    }
    fields = ('first_name', 'last_name', 'username')
    success_url = reverse_lazy('users')
    success_message = gettext_lazy('User successfully modified')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, gettext('You do not have permission to make changes.'))
        return redirect('users')
