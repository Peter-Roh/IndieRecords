"""
define models related to users
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LOGIN_DEFAULT = "default"
    LOGIN_GOOGLE = "google"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_DEFAULT, "Default"),
        (LOGIN_GOOGLE, "Google"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatar", blank=True)
    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=7, blank=True)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_DEFAULT)
    superhost = models.BooleanField(default=False)
