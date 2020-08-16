"""
define url that starts with /
"""
from django.urls import path
from core import views


app_name = "core"


urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
]
