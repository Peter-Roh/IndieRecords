"""
define music related models
"""
from django.db import models
from core import models as core_models
from users import models as user_models


class MusicType(core_models.TimestampedModel):

    """ music type model """

    genre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.genre)


class Music(core_models.TimestampedModel):

    """ Music Model Definition """

    file = models.FileField(upload_to="music")
    title = models.CharField(max_length=150)
    coverImage = models.ImageField(upload_to="coverimage", blank=True)
    genre = models.ManyToManyField(MusicType)
    lyrics = models.TextField(blank=True)
    description = models.TextField(blank=True)
    artist = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    lyricist = models.CharField(max_length=30, blank=True)
    composer = models.CharField(max_length=30, blank=True)

    def __str__(self):
        # 곡 제목 by 음악가
        return self.title + " by " + str(self.artist)
