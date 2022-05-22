from itertools import chain

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

import Statistics.models
from .forms import PlaylistForm, SearchQueryForm
from .models import Song, Favourite, Playlist, PlaylistSong, Genre, Artist
from .player import getSongsJson


def music(request):
    songs = Song.objects.all().order_by('title')

    variables = getSongsJson(songs)
    context = {'songs': songs, 'variables': variables}
    return render(request, 'MusicApp/index.html', context=context)


def search(request):
    songs = []
    artists = []
    genres = []
    playlists = []

    if request.method == "GET":
        if "query" in request.GET:
            form = SearchQueryForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                print(query)
                songs = Song.objects.filter(title__icontains=query)
                artists = Artist.objects.filter(name__icontains=query)
                genres = Genre.objects.filter(name__icontains=query)
                playlists = Playlist.objects.filter(owner=request.user, name__icontains=query)

    context = {'songs': songs, 'artists': artists, 'genres': genres, 'playlists': playlists}
    return render(request, 'MusicApp/search.html', context=context)


class UserProfile(TemplateView):
    context_object_name = 'user_profile'
    template_name = 'MusicApp/user_profile.html'


@login_required(login_url='sign_in')
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
    song = Song.objects.get(id=pk)
    is_favourite = Favourite.objects.filter(user=request.user, song=pk).values('is_fav')
    playlists = Playlist.objects.filter(owner=request.user)
    dict = {}
    isIn = False

    for el in playlists:
        p_songs = PlaylistSong.objects.filter(playlist=el).values('song')
        songs_ids = p_songs.values_list('song', flat=True)
        songs = list(Song.objects.filter(id__in=songs_ids).distinct())
        for s in songs:
            if s.id == song.id:
                isIn = True
        dict[el] = isIn
        isIn = False

    if request.method == "POST":
        if 'add-favourite' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=song, is_fav=is_fav)
            # print(f'query: {query}')
            query.save()

        elif 'remove-favourite' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=song, is_fav=is_fav)
            # print(f'user: {request.user}')
            # print(f'song: {song.id} - {song}')
            # print(f'query: {query}')
            query.delete()

        elif 'add-playlist' in request.POST:
            playlist_id = request.POST['add-playlist']
            playlist = Playlist.objects.get(id=playlist_id)
            # print(f'playlist: {playlist.name}')
            # print(f'song: {song.title}')
            p_song = PlaylistSong(playlist=playlist, song=song)
            p_song.save()
            return HttpResponseRedirect('/song_details/' + str(song.id))

        elif 'remove-playlist' in request.POST:
            playlist_id = request.POST['remove-playlist']
            playlist = Playlist.objects.get(id=playlist_id)
            p_song = PlaylistSong.objects.filter(playlist=playlist, song__id=song.id)
            p_song.delete()
            return HttpResponseRedirect('/song_details/' + str(song.id))

    context = {'song': song, 'is_favourite': is_favourite, 'playlists': playlists, 'dict': dict}
    return render(request, 'MusicApp/song_details.html', context=context)


@login_required(login_url='sign_in')
def playlists(request):
    playlists = Playlist.objects.filter(owner=request.user)

    if request.method == "POST":
        if 'create-playlist' in request.POST:
            form = PlaylistForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                p = Playlist(name=name, owner=request.user)
                p.save()
        elif 'delete-playlist' in request.POST:
            print(request.POST)
            p_id = request.POST['delete-playlist']
            p = Playlist.objects.get(id=p_id)
            p.delete()

    context = {'playlists': playlists}
    return render(request, 'MusicApp/playlists.html', context=context)


@login_required(login_url='sign_in')
def playlist_song(request, pk):
    found_playlist = Playlist.objects.get(owner=request.user, id=pk)
    p_songs = PlaylistSong.objects.filter(playlist=found_playlist).values('song')
    songs_ids = p_songs.values_list('song', flat=True)
    songs = list(Song.objects.filter(id__in=songs_ids).distinct())

    print(songs_ids, songs)

    variables = getSongsJson(songs)

    print(variables)
    # song deletion
    if request.method == "POST":

        song_id = list(request.POST.keys())[1]
        p_song = PlaylistSong.objects.filter(playlist=found_playlist, song__id=song_id)
        p_song.delete()
        return HttpResponseRedirect('/user_profile/playlists/' + str(found_playlist.id))

    context = {'playlist': found_playlist, 'variables': variables, 'songs': songs}
    return render(request, 'MusicApp/playlist_song.html', context=context)


def song(request, pk):
    songs = list(Song.objects.filter(id=pk))
    variables = getSongsJson(songs)

    context = {'variables': variables, 'song': songs[0], 'songs': songs}
    return render(request, 'MusicApp/song.html', context=context)


def artist(request, pk):
    songs = list(Song.objects.filter(artist_id=pk))
    variables = getSongsJson(songs)

    context = {'variables': variables, 'songs': songs}
    return render(request, 'MusicApp/artist.html', context=context)


def genre(request, pk):
    genre = Genre.objects.filter(id=pk).first()
    songs = list(Song.objects.filter(genre=genre))
    variables = getSongsJson(songs)

    context = {'variables': variables, 'genre': genre, 'songs': songs}
    return render(request, 'MusicApp/genre.html', context=context)


@login_required(login_url='sign_in')
def songGenerator(request):
    allListenedSongs = Statistics.models.StatDurationPlay.objects.all()
    songsObjects, songsTitles, songsTimeUnits = [], [], []

    for listenedSong in allListenedSongs:
        if listenedSong.user.username == request.user.username:
            if listenedSong.song.title in songsTitles:
                idx = songsTitles.index(listenedSong.song.title)
                songsTimeUnits[idx] += listenedSong.time_units
            else:
                songsTitles.append(listenedSong.song.title)
                songsTimeUnits.append(listenedSong.time_units)
                songsObjects.append(listenedSong.song)

    allTime = sum(songsTimeUnits)
    results = [['bpm', 0], ['energy', 0], ['danceability', 0], ['liveness', 0], ['valence', 0], ['acousticness', 0], ['speechiness', 0]]

    for i in range(len(songsObjects)):
        results[0][1] += (songsObjects[i].details.bpm * songsTimeUnits[i]) / allTime
        results[1][1] += (songsObjects[i].details.energy * songsTimeUnits[i]) / allTime
        results[2][1] += (songsObjects[i].details.danceability * songsTimeUnits[i]) / allTime
        results[3][1] += (songsObjects[i].details.liveness * songsTimeUnits[i]) / allTime
        results[4][1] += (songsObjects[i].details.valence * songsTimeUnits[i]) / allTime
        results[5][1] += (songsObjects[i].details.acousticness * songsTimeUnits[i]) / allTime
        results[6][1] += (songsObjects[i].details.speechiness * songsTimeUnits[i]) / allTime
    context = {'results': results}

    return render(request, 'MusicApp/song_generator.html', context=context)
