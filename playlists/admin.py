"""
configure admin panel related to playlist
"""
from django.contrib import admin
from playlists import models


@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):

    """ Playlist Admin Definition """

    list_display = (
        "__str__",
        "count_musics"
    )

    filter_horizontal = (
        "musics",
    )

    raw_id_fields = (
        "user",
    )

    def count_musics(self, obj):

        ''' return how many musics are in the playlist '''

        return obj.musics.count()

    count_musics.short_description = "Number of Musics"
