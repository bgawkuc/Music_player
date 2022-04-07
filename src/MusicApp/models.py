from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from MusicPlayer import settings

static_url = settings.STATIC_URL


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    song_link = models.CharField(max_length=255)
    image_link = models.CharField(max_length=255)
    genre = models.ForeignKey('Genre', on_delete=models.DO_NOTHING)
    length = models.IntegerField(validators=[MinValueValidator(0)])
    details = models.ForeignKey('SongDetail', on_delete=models.CASCADE)  # if song removed then songdetail also


class SongDetail(models.Model):
    id = models.AutoField(primary_key=True)
    bpm = models.IntegerField(validators=[MinValueValidator(0)])
    energy = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    danceability = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    loudness = models.IntegerField(validators=[MaxValueValidator(0)])
    liveness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    valence = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    acousticness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    speechiness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
