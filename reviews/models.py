"""
define models related to reviews
"""
from django.db import models
from core import models as core_models


class Review(core_models.TimestampedModel):

    """ Review Model Definition """

    review = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    music = models.ForeignKey("musics.Music", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review} - {self.music}'
