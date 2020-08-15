from django.urls import path
from core.forms import CustomLoginForm
from . import views


app_name="core"


urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
]
