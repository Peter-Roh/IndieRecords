"""
configure admin panel related to reviews
"""
from django.contrib import admin
from reviews import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    list_display = (
        "user",
        "music",
        "review",
    )

    search_fields = (
        "user__username",
    )

    list_filter = (
        "user",
        "music",
    )

    raw_id_fields = (
        "user",
    )
