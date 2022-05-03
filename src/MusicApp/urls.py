from django.urls import path
from . import views
from .views import UserProfile

urlpatterns = [
    path('', views.music, name='index'),
    path('song_details/<int:pk>', views.songDetails, name='song_details'),
    path('user_profile/', UserProfile.as_view(), name='user_profile'),
    path('user_profile/favourites/', views.favourites, name='favourites'),
    path('user_profile/playlists/', views.playlists, name='playlists'),
    path('user_profile/playlists/<int:pk>', views.playlist_song, name='playlist_songs'),
    path('search/', views.search, name='search')
]