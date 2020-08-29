"""
configure admin panel related to users
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users import models
from musics import models as musics_model
from playlists import models as playlists_model


class MusicInline(admin.StackedInline):

    """ show music admin panel inside users """

    model = musics_model.Music


class PlaylistInline(admin.TabularInline):

    """ show playlist admin panel inside users """

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
                    "login_method",
                    "profile_url",
                    "superhost",
                )
            }
        ),
    )

    list_display = (
        "username",
        "email",
        "gender",
        "login_method",
        "superhost",
    )

    list_filter = (
        "login_method",
        "gender",
        "superhost",
    )

    inlines = (
        MusicInline,
        PlaylistInline,
    )
