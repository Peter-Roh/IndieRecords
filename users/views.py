"""
define views related to users
"""
from django.views.generic import FormView
from django.shortcuts import render
from django.urls import reverse_lazy
from users import forms


class SignupView(FormView):

    """ signup view definition """

    template_name = "users/user.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("musics:main")
