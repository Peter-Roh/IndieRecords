"""
define url that starts with /
"""
from django.urls import path
from core import views


app_name = "core"


urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("login/google/", views.google_login, name="google-login"),
    path("login/google/callback/", views.google_callback, name="google-callback"),
    path("login/facebook/", views.facebook_login, name="facebook-login"),
    path("login/facebook/callback/", views.facebook_callback, name="facebook-callback"),
]
