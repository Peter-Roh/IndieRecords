"""
define url that starts with /music
"""
from django.urls import path
from musics import views


app_name = "music"


urlpatterns = [
    path("", views.main, name="main"),
]
