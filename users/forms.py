"""
define forms related to users
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import PasswordInput
from users.models import User


class SignupForm(forms.Form):

    """ sign up form definition """

    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput)
    password1 = forms.CharField(widget=PasswordInput, label="Confirm Password")

    def clean_username(self):
        '''  check username '''
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("That username is already taken. ")
        except User.DoesNotExist:
            return username

    def clean_password1(self):
        ''' check password '''
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match. ")
        else:
            return password

    def save(self):
        ''' sign up user '''
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = User.objects.create_user(username, password)
        user.email = email
        user.set_password(password)
        user.save()


class CustomUserChangeForm(UserChangeForm):

    """ custom user change form """

    class Meta:
        model = get_user_model()
        fields = ("email", "avatar")
