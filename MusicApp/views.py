from django.shortcuts import render
from django.views.generic import DetailView

from .models import Song


def index(request):
    context = {"songs": Song.objects.all()}
    return render(request, "index.html", context)


class SongDetails(DetailView):
    model = Song
    context_object_name = 'song'
    #nadaje nazwe dla tego route
    template_name = 'MusicApp/song_details.html'