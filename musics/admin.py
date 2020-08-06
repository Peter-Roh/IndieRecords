from django.contrib import admin
from . import models


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
