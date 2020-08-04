from django.contrib import admin
from . import models


@admin.register(models.MusicType)
class MusicTypeAdmin(admin.ModelAdmin):

    pass


@admin.register(models.Music)
class MusicAdmin(admin.ModelAdmin):

    pass
