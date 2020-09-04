"""
define views related to users
"""
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.urls import reverse_lazy
from users import forms
from users.models import User
from users import mixins


class SignupView(mixins.LoggedOutOnlyView, FormView):

    """ signup view definition """

    template_name = "users/user.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("musics:main")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

def log_out(request):

    """ sign out a user """

    logout(request)
    return redirect(reverse("core:login"))


class Mypage(SuccessMessageMixin, UpdateView):

    """ mypage to update profiles """

    template_name = "users/mypage.html"
    model = User
    success_url = reverse_lazy("musics:main")
    success_message = "Profile Updated"
    fields = ("email", "avatar", "gender")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)


class UpdatePassword(SuccessMessageMixin, PasswordChangeView):

    pass
