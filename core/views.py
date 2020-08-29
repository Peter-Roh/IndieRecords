"""
define login view
"""
import datetime
import os
import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views.generic import FormView
from users import mixins
from users.models import User
from core import forms


class LoginView(mixins.LoggedOutOnlyView, FormView):

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


class GoogleException(Exception):
    pass


def google_login(request):
    client_id = os.environ.get("GOOGLE_ID")
    redirect_uri = "http://localhost:8000/login/google/callback/"
    scope="email profile openid https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read"
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}")


def google_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GOOGLE_ID")
        client_secret = os.environ.get("GOOGLE_SECRET")
        redirect_uri = "http://localhost:8000/login/google/callback/"
        if code is not None:
            request = requests.post(
                f"https://www.googleapis.com/oauth2/v4/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}",
                headers={
                    "Accept": "application/json"
                }
            )
            result_json = request.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GoogleException()
            else:
                access_token = result_json.get("access_token")
                personFields = "birthdays,genders"
                profile_request = requests.get(
                    f"https://www.googleapis.com/oauth2/v1/userinfo",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json"
                    },
                )

                detail_request = requests.get(
                    f"https://people.googleapis.com/v1/people/me?personFields={personFields}",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json"
                    },
                )
                profile_json = profile_request.json()
                detail_json = detail_request.json()
                email = profile_json.get("email")
                if email is not None:
                    name = profile_json.get("name")
                    picture = profile_json.get("picture")
                    family_name = profile_json.get("family_name")
                    given_name = profile_json.get("given_name")
                    gender = detail_json.get("genders")[0]['value']
                    date = detail_json.get("birthdays")[0]['date']
                    try:
                        user = User.objects.get(username=name)
                        #user already exists
                        if user.login_method != User.LOGIN_GOOGLE:
                            raise GoogleException()
                    except User.DoesNotExist:
                        user = User.objects.create(
                            username=name,
                            email=email,
                            first_name=given_name,
                            last_name=family_name,
                            gender=gender,
                            login_method=User.LOGIN_GOOGLE,
                            profile_url=picture,
                            birth=datetime.datetime(date['year'], date['month'], date['day'])
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("musics:main"))
                else:
                    raise GoogleException()
        else:
            raise GoogleException()
    except GoogleException:
        return redirect(reverse("core:login"))
