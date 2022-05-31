from django.urls import path
from . import views
from .views import UserProfile

urlpatterns = [
    path('', views.music, name='index'),
    path('song_details/<int:pk>', views.songDetails, name='song_details'),
    path('user_profile/', UserProfile.as_view(), name='user_profile'),
    path('user_profile/favourites/', views.favourites, name='favourites'),
    path('user_profile/playlists/', views.playlists, name='playlists'),
    path('playlists/<int:pk>', views.playlist_song, name='playlist_songs'),
    path('song/<int:pk>', views.song, name='song'),
    path('artist/<int:pk>', views.artist, name='artist'),
    path('genre/<int:pk>', views.genre, name='genre'),
    path('search/', views.search, name='search'),
    path('song_generator', views.songGenerator, name='song_generator'),
]