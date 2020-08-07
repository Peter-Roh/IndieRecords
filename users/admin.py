from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from musics import models as musics_model
from playlists import models as playlists_model


class MusicInline(admin.StackedInline):

    model = musics_model.Music


class PlaylistInline(admin.TabularInline):

    model = playlists_model.Playlist


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields":
                (
                    "avatar",
                    "gender",
                    "birth",
                    "superhost",
                )
            }
        ),
    )

    list_display = (
        "username",
        "email",
        "gender",
        "superhost",
    )

    list_filter = (
        "gender",
        "superhost",
    )

    inlines = (
        MusicInline,
        PlaylistInline,
    )
