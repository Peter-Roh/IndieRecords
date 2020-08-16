"""
configure admin panel related to music models
"""
from django.contrib import admin
from musics import models


@admin.register(models.MusicType)
class MusicTypeAdmin(admin.ModelAdmin):

    """ Music type admin """

    pass


@admin.register(models.Music)
class MusicAdmin(admin.ModelAdmin):

    """ Music admin """

    fieldsets = (
        (
            "Music Info",
            {
                "fields":
                (
                    "file",
                    "title",
                    "coverImage",
                    "genre",
                    "lyrics",
                    "description",
                    "artist",
                    "lyricist",
                    "composer",
                )
            }
        ),
    )

    list_display = (
        "title",
        "artist",
        "get_genre",
        "created",
    )

    list_filter = (
        "artist",
        "genre",
    )

    search_fields = (
        "title",
        "artist__username"
    )

    # filter many to many fields
    filter_horizontal = (
        "genre",
    )

    raw_id_fields = (
        "artist",
    )

    def get_genre(self, obj):

        ''' show genres of a song in admin panel '''

        genre = []
        for item in obj.genre.all():
            genre.append(item.genre)
        return ",".join(genre)

    get_genre.short_description = "Genre"
