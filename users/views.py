"""
define views related to users
"""
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views.generic import FormView
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.urls import reverse_lazy
from users import forms


class SignupView(FormView):

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


def Mypage(request):

    return render(request, "users/mypage.html")
