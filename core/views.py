"""
define login view
"""
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import reverse
from django.views.generic import FormView
from core import forms


class LoginView(FormView):

    """ login view definition """

    template_name = "core/main.html"
    form_class = forms.CustomLoginForm

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("musics:main")
