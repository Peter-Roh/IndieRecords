"""
define login view
"""
import datetime
import os
import requests
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.files.base import ContentFile
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


class KakaoException(Exception):
    pass


def google_login(request):
    ''' use google oauth '''
    client_id = os.environ.get("GOOGLE_ID")
    redirect_uri = "http://localhost:8000/login/google/callback/"
    scope = "email profile openid https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read"
    # get code from google oauth
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&access_type=offline"
    )


def kakao_login(request):
    ''' use facebook oauth '''
    client_id = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


def google_callback(request):
    '''
    get informations from google people api
    check if the use is already joined
    create new user
    log the user in
    '''
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GOOGLE_ID")
        client_secret = os.environ.get("GOOGLE_SECRET")
        redirect_uri = "http://localhost:8000/login/google/callback/"
        if code is not None:
            # get access_token with the code
            request_api = requests.post(
                f"https://www.googleapis.com/oauth2/v4/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}",
                headers={
                    "Accept": "application/json"
                }
            )
            result_json = request_api.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GoogleException()
            else:
                access_token = result_json.get("access_token")
                personFields = "birthdays,genders"
                # use access_token to get informations from people api
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
                        "Accept": "application/json",
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
                    if gender == 'male':
                        gender = User.GENDER_MALE
                    elif gender == 'female':
                        gender = User.GENDER_FEMALE
                    else:
                        gender = User.GENDER_OTHER
                    date = detail_json.get("birthdays")[0]['date']
                    try:
                        user = User.objects.get(username=name)
                        # user already exists
                        if user.login_method != User.LOGIN_GOOGLE:
                            # the user already has account with different login method
                            # wrong login attempt
                            raise GoogleException()
                        # else the user is trying to log in. the user already signed up before
                    except User.DoesNotExist:
                        # create new user with infos
                        user = User.objects.create(
                            username=name,
                            email=email,
                            first_name=given_name,
                            last_name=family_name,
                            gender=gender,
                            login_method=User.LOGIN_GOOGLE,
                            birth=datetime.datetime(date['year'], date['month'], date['day'])
                        )
                        user.set_unusable_password()
                        user.save()
                        # get image file from the url
                        if picture is not None:
                            photo_request = requests.get(picture)
                            user.avatar.save(f"{name}_avatar", ContentFile(photo_request.content))
                    login(request, user)
                    return redirect(reverse("musics:main"))
                else:
                    # the google email does not exist
                    raise GoogleException()
        else:
            # code is None
            raise GoogleException()
    except GoogleException:
        return redirect(reverse("core:login"))


def kakao_callback(request):
    ''' sign in and log in with kakao '''
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("KAKAO_KEY")
        client_secret = os.environ.get("KAKAO_SECRET")
        redirect_uri = "http://127.0.0.1:8000/login/kakao/callback"
        if code is not None:
            # get access_token with the code
            request_api = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}",
            )
            result_json = request_api.json()
            error = result_json.get("error", None)
            if error is not None:
                raise KakaoException()
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                    },
                )
                profile_json = profile_request.json()
                kakao_id = profile_json.get("id")
                if kakao_id is not None:
                    name = profile_json.get("properties")['nickname']
                    picture = profile_json.get("properties")['profile_image']
                    email = profile_json.get("kakao_account")["email"]
                    if email is None:
                        raise KakaoException()
                    gender = profile_json.get("kakao_account")["gender"]
                    if gender == 'male':
                        gender = User.GENDER_MALE
                    elif gender == 'female':
                        gender = User.GENDER_FEMALE
                    else:
                        gender = User.GENDER_OTHER
                    try:
                        user = User.objects.get(username=name)
                        # user already exists
                        if user.login_method != User.LOGIN_KAKAO:
                            # the user already has account with different login method
                            # wrong login attempt
                            raise KakaoException()
                        # else the user is trying to log in. the user already signed up before
                    except User.DoesNotExist:
                        # create new user with infos
                        user = User.objects.create(
                            username=name,
                            email=email,
                            gender=gender,
                            login_method=User.LOGIN_KAKAO,
                        )
                        user.set_unusable_password()
                        user.save()
                        # get image file from the url
                        if picture is not None:
                            photo_request = requests.get(picture)
                            user.avatar.save(f"{name}_avatar", ContentFile(photo_request.content))
                    login(request, user)
                    return redirect(reverse("musics:main"))
                else:
                    raise KakaoException()
    except KakaoException:
        return redirect(reverse("core:login"))
