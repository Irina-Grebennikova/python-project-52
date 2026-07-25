from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy

from .models import Label, Status


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        label=gettext_lazy('Status'), queryset=Status.objects.all(), required=False
    )
    assignee = forms.ModelChoiceField(
        label=gettext_lazy('Assignee'), queryset=User.objects.all(), required=False
    )
    label = forms.ModelChoiceField(
        label=gettext_lazy('Label'), queryset=Label.objects.all(), required=False
    )
    own_tasks = forms.BooleanField(label=gettext_lazy('Only own tasks'), required=False)
