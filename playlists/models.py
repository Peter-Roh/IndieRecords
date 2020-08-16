"""
define models related to playlist
"""
from django.db import models
from core import models as core_models


class Playlist(core_models.TimestampedModel):

    """ Playlist Model Definition """

    name = models.CharField(max_length=100)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    musics = models.ManyToManyField("musics.Music", blank=True)

    def __str__(self):
        return f"{self.user.username}\'s playlist: {self.name}"
