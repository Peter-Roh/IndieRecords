from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput
from django.forms.widgets import TextInput
from users import models


class CustomLoginForm(AuthenticationForm):

    ''' custom default authentication form '''

    username = forms.CharField(
        widget=TextInput(
            attrs={
                'class': 'validate',
                'placeholder': 'USERNAME'
                }
            ),
        label=""
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                'placeholder': 'PASSWORD'
            }
        ),
        label=""
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Please enter a correct password. "))
        except models.User.DoesNotExist:
            self.add_error("username", forms.ValidationError("User does not exist.."))
