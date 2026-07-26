from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        password_form = SetPasswordForm(self.instance)

        self.fields.update(password_form.fields)

        self.fields['new_password1'].label = gettext('Password')
        self.fields['new_password2'].label = gettext('Password confirmation')

    def clean(self):
        cleaned_data = super().clean()

        password_form = SetPasswordForm(
            self.instance,
            {
                'new_password1': cleaned_data.get('new_password1'),
                'new_password2': cleaned_data.get('new_password2'),
            },
        )

        if not password_form.is_valid():
            for field, errors in password_form.errors.items():
                for error in errors:
                    self.add_error(field, error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('new_password1')
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
