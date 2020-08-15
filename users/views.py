from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from . import forms


class SignupView(FormView):

    template_name = "users/user.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("musics:main")
