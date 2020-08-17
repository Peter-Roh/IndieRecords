"""
define forms related to users
"""
import datetime
from django import forms
from django.forms.widgets import PasswordInput
from users.models import User


class SignupForm(forms.Form):

    """ sign up form definition """

    this_year = datetime.datetime.today().year
    YEARS = [x for x in range(1940, this_year + 1)]

    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES)
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS),
        initial=datetime.date.today
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username = username)
            raise forms.ValidationError("That username is already taken. ")
        except User.DoesNotExist:
            return username

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match. ")
        else:
            return password

    def save(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        gender = self.cleaned_data.get("gender")
        birth = self.cleaned_data.get("birthday")
        user = User.objects.create_user(username, password)
        user.email = email
        user.gender = gender
        user.birth = birth
        user.set_password(password)
        user.save()
