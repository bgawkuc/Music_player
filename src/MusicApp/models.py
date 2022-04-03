from django.db import models


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.TextField(max_length=50)
    image = models.ImageField(blank=True, null=True)
    song_file = models.FileField(blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    beats_per_min = models.CharField(max_length=5, blank=True, null=True)
    energy = models.CharField(max_length=5, blank=True, null=True)
    danceability = models.CharField(max_length=5, blank=True, null=True)
