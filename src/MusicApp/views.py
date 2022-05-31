from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from .bestSong import songsGenerator, findBestSong
from .forms import PlaylistForm, SearchQueryForm
from .models import Song, Favourite, Playlist, PlaylistSong, Genre, Artist, PlaylistFollow
from .player import getSongsJson
from .playlists import createPlaylist, deletePlaylist, deleteSong, addSong, changePrivacy, followPlaylist, \
    unfollowPlaylist


def music(request):
    songs = Song.objects.all().order_by('title')

    if request.user.is_authenticated:
        songs = list(list(zip(*songsGenerator(request.user)))[1])
        print(songs)

    variables = getSongsJson(songs)
    context = {'songs': songs, 'variables': variables}
    return render(request, 'MusicApp/index.html', context=context)


@login_required(login_url='sign_in')
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
                playlists = Playlist.objects.filter(name__icontains=query, is_private=False)

    if request.method == "POST":
        if 'follow-playlist' in request.POST:
            p_id = request.POST['follow-playlist']
            playlist = Playlist.objects.get(id=p_id)
            followPlaylist(playlist, request.user)
            return HttpResponseRedirect('/playlists/' + p_id)

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
            addSong(playlist, song)
            return HttpResponseRedirect('/song_details/' + str(song.id))

        elif 'remove-playlist' in request.POST:
            playlist_id = request.POST['remove-playlist']
            playlist = Playlist.objects.get(id=playlist_id)
            deleteSong(playlist, song)
            return HttpResponseRedirect('/song_details/' + str(song.id))

    context = {'song': song, 'is_favourite': is_favourite, 'playlists': playlists, 'dict': dict}
    return render(request, 'MusicApp/song_details.html', context=context)


@login_required(login_url='sign_in')
def playlists(request):
    playlists = Playlist.objects.filter(owner=request.user)
    followed = PlaylistFollow.objects.filter(user=request.user).values('playlist')
    followed_ids = followed.values_list('playlist', flat=True)
    followed = list(Playlist.objects.filter(id__in=followed_ids).distinct().filter(~Q(owner=request.user)))
    print(followed)

    if request.method == "POST":
        if 'create-playlist' in request.POST:
            form = PlaylistForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                is_private = True if form.cleaned_data['is_private'] else False
                createPlaylist(name, request.user, is_private)
        elif 'delete-playlist' in request.POST:
            p_id = request.POST['delete-playlist']
            deletePlaylist(p_id)
        elif 'public-playlist' in request.POST:
            p_id = request.POST['public-playlist']
            playlist = Playlist.objects.get(id=p_id)
            changePrivacy(playlist, False)
        elif 'private-playlist' in request.POST:
            p_id = request.POST['private-playlist']
            playlist = Playlist.objects.get(id=p_id)
            changePrivacy(playlist, True)
        elif 'unfollow-playlist' in request.POST:
            p_id = request.POST['unfollow-playlist']
            playlist = Playlist.objects.get(id=p_id)
            unfollowPlaylist(playlist, request.user)

    context = {'playlists': playlists, 'followed': followed}
    return render(request, 'MusicApp/playlists.html', context=context)


@login_required(login_url='sign_in')
def playlist_song(request, pk):
    found_playlist = Playlist.objects.get(id=pk)

    if found_playlist.is_private and found_playlist.owner != request.user:
        return HttpResponseRedirect('/')

    p_songs = PlaylistSong.objects.filter(playlist=found_playlist).values('song')
    songs_ids = p_songs.values_list('song', flat=True)
    songs = list(Song.objects.filter(id__in=songs_ids).distinct())

    print(songs_ids, songs)

    variables = getSongsJson(songs)

    print(variables)
    # song deletion
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        song = Song.objects.get(id=song_id)
        deleteSong(found_playlist, song)
        return HttpResponseRedirect('/playlists/' + str(found_playlist.id))

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
    context = {'results': findBestSong(request.user)}

    return render(request, 'MusicApp/song_generator.html', context=context)
