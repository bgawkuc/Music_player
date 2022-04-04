from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from MusicPlayer import settings

static_url = settings.STATIC_URL


class Song(models.Model):
    class Genre(models.TextChoices):
        ATL_HIP_HOP = 'ATL_HIP_HOP', _('Atlanta hip hop')
        AUSTRALIAN_POP = 'AUSTRALIAN_POP', _('Australian pop')
        BIG_ROOM = 'BIG_ROOM', _('Big room')
        BOY_BAND = 'BOY_BAND', _('Boy band')
        BROSTEP = 'BROSTEP', _('Brostep')
        CANADIAN_HIP_HOP = 'CANADIAN_HIP_HOP', _('Canadian hip hop')
        CANADIAN_POP = 'CANADIAN_POP', _('Canadian pop')
        COUNTRY_RAP = 'COUNTRY_RAP', _('Country rap')
        DANCE_POP = 'DANCE_POP', _('Dancepop')
        DFW_RAP = 'DFW_RAP', _('DFW rap')
        EDM = 'EDM', _('EDM')
        ELECTROPOP = 'ELECTROPOP', _('Electropop')
        ESCAPE_ROOM = 'ESCAPE_ROOM', _('Escape room')
        LATIN = 'LATIN', _('Latin')
        PANAMANIAN_POP = 'PANAMANIAN_POP', _('Panamanian pop')
        POP = 'POP', _('Pop')
        POP_HOUSE = 'POP_HOUSE', _('Pop house')
        R_AND_B_ES = 'R_AND_B_ES', _('R&B en espanol')
        REGGAETON = 'REGGAETON', _('Reggaeton')
        REGGAETON_FLOW = 'REGGAETON_FLOW', _('Reggaeton flow')
        TRAP_MUSIC = 'TRAP_MUSIC', _('Trap music')

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    song_link = models.CharField(max_length=255)
    image_link = models.CharField(max_length=255)
    genre = models.CharField(max_length=50, choices=Genre.choices, null=True)
    length = models.IntegerField(validators=[MinValueValidator(0)])
    details = models.ForeignKey('SongDetail', on_delete=models.SET_NULL, null=True)


class SongDetail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    bpm = models.IntegerField(validators=[MinValueValidator(0)])
    energy = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    danceability = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    loudness = models.IntegerField(validators=[MaxValueValidator(0)])
    liveness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    valence = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    acousticness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    speechiness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
