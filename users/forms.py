import datetime
from django import forms
from django.forms.widgets import PasswordInput
from . import models


class SignupForm(forms.Form):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    this_year = datetime.datetime.today().year
    YEARS = [x for x in range(1940, this_year + 1)]

    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=YEARS), initial=datetime.date.today)
