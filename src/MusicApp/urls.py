from django.urls import path
from . import views
from .views import SongDetails


urlpatterns = [
    path('', views.music, name='index'),
    # dla każdego utworu strona z detalami
    path('song-details/<int:pk>', SongDetails.as_view(), name='song-details'),
]