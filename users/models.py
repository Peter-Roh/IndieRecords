"""
define models related to users
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    avatar = models.ImageField(upload_to="avatar", blank=True)
    profile_url = models.CharField(null=True, blank=True, max_length=256)
    superhost = models.BooleanField(default=False)
