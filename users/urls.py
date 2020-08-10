from django.urls import path
from . import views


app_name = "users"


urlpatterns = [
    path("", views.main, name="user"),
#    path("signup", views.signup, name="signup"),
]
