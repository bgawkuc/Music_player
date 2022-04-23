from django.contrib import admin
from .models import Song, SongDetail, Genre

admin.site.register(Song)
admin.site.register(SongDetail)
admin.site.register(Genre)
