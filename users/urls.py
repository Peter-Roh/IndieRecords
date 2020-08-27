"""
define urls that starts with /users
"""
from django.urls import path
from users import views


app_name = "users"


urlpatterns = [
    path("", views.SignupView.as_view(), name="user"),
    path("mypage/", views.Mypage.as_view(), name="mypage"),
    path("logout/", views.log_out, name="logout"),
]
