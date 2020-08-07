from django.contrib import admin
from . import models


@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):

    """ Playlist Admin Definition """

    list_display = (
        "__str__",
        "countMusics"
    )

    filter_horizontal = (
        "musics",
    )

    raw_id_fields = (
        "user",
    )

    def countMusics(self, obj):
        return obj.musics.count()

    countMusics.short_description = "Number of Musics"
