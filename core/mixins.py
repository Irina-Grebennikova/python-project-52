from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext


class ProtectedDeleteMixin:
    protected_message = gettext('Cannot delete this object')
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.success_url)
