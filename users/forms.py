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
