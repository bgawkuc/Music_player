import datetime

from django.http import HttpResponse

from MusicApp.models import Song
from Statistics.models import StatSinglePlay


def singlePlay(request):
    user = request.user
    song_id = request.POST['song']
    song = Song.objects.filter(id=song_id).first()
    date = datetime.date.today()

    stat = StatSinglePlay.objects.filter(date__year=date.year,
                                         date__month=date.month,
                                         date__day=date.day,
                                         song=song,
                                         user=user).first()
    print(stat)
    if stat is not None:
        stat.increaseCount()
        stat.save()
    else:
        stat = StatSinglePlay(user=user, song=song)

        stat.increaseCount()
        stat.save()

    print(song_id, user.id, date)
    print(stat.song.id, stat.user.id, stat.date, stat.count)
    return HttpResponse()
