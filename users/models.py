"""
define models related to users
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    LOGIN_DEFAULT = "default"
    LOGIN_GOOGLE = "google"
    LOGIN_FACEBOOK = "facebook"

    LOGIN_CHOICES = (
        (LOGIN_DEFAULT, "Default"),
        (LOGIN_GOOGLE, "Google"),
        (LOGIN_FACEBOOK, "Facebook"),
    )

    avatar = models.ImageField(upload_to="avatar", blank=True)
    profile_url = models.CharField(null=True, blank=True, max_length=256)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_DEFAULT)
    superhost = models.BooleanField(default=False)
