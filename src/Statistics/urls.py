from django.urls import path
from . import views


urlpatterns = [
    path('single/', views.singlePlay, name='single'),
    path('duration/', views.durationPlay, name='duration'),
    path('user-stats/', views.userStats, name='user-stats'),
    path('admin-stats/', views.adminStats, name='admin-stats'),
    path('artists-report/', views.artistsReport, name='artists-report'),
    path('songs-report/', views.songsReport, name='songs-report'),
    path('genres-report/', views.genresReport, name='genres-report'),
    path('users-report/', views.usersReport, name='users-report'),
]

