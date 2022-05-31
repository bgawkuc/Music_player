from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from MusicPlayer import settings

static_url = settings.STATIC_URL


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.ForeignKey('Artist', on_delete=models.DO_NOTHING)
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


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_private = models.BooleanField(default=True)


class PlaylistFollow(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PlaylistSong(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
