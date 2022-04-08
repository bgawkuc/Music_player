import json

from django.shortcuts import render
from django.views.generic import DetailView

from .models import Song


class SongDetails(DetailView):
    model = Song
    context_object_name = 'song'
    # nadaje nazwe dla tego route
    template_name = 'MusicApp/song_details.html'


def music(request):
    songs = Song.objects.all().order_by('title')
    songs_json = []
    for song in songs:
        minutes = str(song.length // 60)
        seconds = song.length % 60
        if seconds < 10:
            seconds *= 10
        seconds = str(seconds)

        ent = {
            'name':          song.title,
            'artist':        song.artist,
            'url':           'static/' + song.song_link,
            'cover_art_url': 'static/' + song.image_link,
            'duration':      minutes + ':' + seconds,
            'genre':         song.genre.name,
            'id':            song.id
        }

        songs_json.append(ent)

    variables = {
        'title':      'Music',
        'songs_json': json.dumps(songs_json)
    }

    return render(request, 'index.html', variables)
