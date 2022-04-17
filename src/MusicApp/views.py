import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Song, Favourite


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

    return render(request, 'MusicApp/index.html', variables)


class UserProfile(TemplateView):
    context_object_name = 'user_profile'
    template_name = 'MusicApp/user_profile.html'


def favourites(request):
    songs = Song.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()
    print(f'songs: {songs}')

    if request.method == "POST":
        pk = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(user=request.user, song__id=pk, is_fav=True)
        favourite_song.delete()
    context = {'songs': songs}
    return render(request, 'MusicApp/favourites.html', context=context)


@login_required(login_url='sign_in')
def songDetails(request, pk):
    songs = Song.objects.filter(id=pk).first()
    is_favourite = Favourite.objects.filter(user=request.user).filter(song=pk).values('is_fav')

    if request.method == "POST":
        if 'add-favourite' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=songs, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
        elif 'remove-favourite' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=songs, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {songs.id} - {songs}')
            print(f'query: {query}')
            query.delete()

    context = {'songs': songs, 'is_favourite': is_favourite}
    return render(request, 'MusicApp/song_details.html', context=context)