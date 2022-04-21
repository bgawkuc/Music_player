from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import PlaylistForm, SearchQueryForm
from .models import Song, Favourite, Playlist, PlaylistSong
from .player import getSongsJson


def music(request):
    songs = Song.objects.all().order_by('title')

    if request.method == "POST":
        if "query-search" in request.POST:
            form = SearchQueryForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                print(query)
                songs_title = Song.objects.filter(title__icontains=query)
                songs_author = Song.objects.filter(artist__icontains=query)
                songs_genre = Song.objects.filter(genre__name__icontains=query)
                songs = list(set(chain(songs_title, songs_author, songs_genre)))
                print(songs)

    variables = getSongsJson(songs)
    return render(request, 'MusicApp/index.html', variables)


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

    if request.method == "POST":
        if 'add-favourite' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=song, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
        elif 'remove-favourite' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=song, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {song.id} - {song}')
            print(f'query: {query}')
            query.delete()
        elif 'add-playlist' in request.POST:
            playlist_id = request.POST['add-playlist']
            playlist = Playlist.objects.get(id=playlist_id)
            print(f'playlist: {playlist.name}')
            print(f'song: {song.title}')

            # if not already in playlist
            if not PlaylistSong.objects.filter(playlist=playlist, song=song):
                p_song = PlaylistSong(playlist=playlist, song=song)
                p_song.save()

    context = {'song': song, 'is_favourite': is_favourite, 'playlists': playlists}
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
    songs = list(Song.objects.filter(id__in=songs_ids))

    print(songs_ids, songs)

    variables = getSongsJson(songs)

    # song deletion
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        p_song = PlaylistSong.objects.get(playlist=found_playlist, song__id=song_id)
        p_song.delete()

    context = {'playlist': found_playlist, 'variables': variables, 'songs': songs_ids}
    return render(request, 'MusicApp/playlist_song.html', context=context)
