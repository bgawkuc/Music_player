import datetime
import matplotlib.pyplot as plt
import numpy as np
import random

from django.http import HttpResponse, FileResponse
from django.shortcuts import render

from MusicApp.models import Song
from Statistics.models import StatSinglePlay, StatDurationPlay
from fpdf import FPDF


# pip install fpdf2
# pip install pillow
from six import StringIO


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

    if stat is not None:
        stat.increaseCount()
        stat.save()
    else:
        stat = StatSinglePlay(user=user, song=song)

        stat.increaseCount()
        stat.save()

    print("SinglePlay")
    print(song_id, user.id, date)
    print(stat.song.id, stat.user.id, stat.date, stat.count)
    return HttpResponse()


def durationPlay(request):
    user = request.user
    song_id = request.POST['song']
    song = Song.objects.filter(id=song_id).first()
    time_units = request.POST['time_units']

    stat = StatDurationPlay(user=user, song=song, time_units=time_units)
    stat.save()

    print("DurationPlay")
    print(song_id, user.id)
    print(stat.song.id, stat.user.id, stat.date, stat.time_units)
    return HttpResponse()


def userStats(request):
    stats = StatSinglePlay.objects.all()
    user = request.user
    fiveBestSongs = findFiveMostPopularUserSongs(user)
    fiveBestArtists = findFiveMostPopularUserArtists(user)
    fiveBestGenres = findFiveMostPopularGenres(user)

    context = {'stats': stats, 'fiveBestSongs': fiveBestSongs, 'fiveBestArtists': fiveBestArtists, 'fiveBestGenres': fiveBestGenres}
    return render(request, 'Statistics/user_stats.html', context=context)


def adminStats(request):
    return render(request, 'Statistics/admin_stats.html', context={})


def findNDifferentColors(n):
    colors = []
    while len(colors) < n:
        color = "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
        if color not in colors:
            colors.append(color)
    return colors


def songsReport(request):
    all_ = findMostPopularSongs()

    # create pdf
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 20)

    pdf.cell(297, 10, 'Number of each songs played', ln=1, align='C')
    pdf.cell(297, 10, '', ln=1)

    pdf.set_font('courier', 'B', 14)
    pdf.cell(297, 14, f" {'Id'.ljust(7)} {'Title'.ljust(50)} {'Artist'.ljust(20)} {'Count'}", ln=1)
    pdf.line(10, 40, 287, 40)

    pdf.set_font('courier', '', 12)
    idx = 1
    counts = []

    for title, artist, count in all_:
        pdf.cell(297, 7, str(idx).ljust(10) + str(title).ljust(60) + str(artist).ljust(26) + str(count), ln=1)
        idx += 1
        counts.append(count)

    x = [str(i) for i in range(1, len(all_)+1)]
    plt.bar(x, counts, color='#21a25b', width=0.6)
    plt.title('Number of each songs played')
    plt.xlabel('Song ID')
    plt.ylabel('Number of plays')
    plt.show()

    pdf.output('songsReport.pdf', 'F')

    return FileResponse(open('songsReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def artistsReport(request):
    all_ = findMostPopularArtist()

    # create pdf
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 20)

    pdf.cell(297, 10, 'Number of plays of each artist\'s songs', ln=1, align='C')
    pdf.cell(297, 10, '', ln=1)

    pdf.set_font('courier', 'B', 14)
    pdf.cell(297, 14, f"{'Artist'.ljust(85)} {'Count'.ljust(50)}",ln=1)
    pdf.line(10, 40, 287, 40)

    pdf.set_font('courier', '', 12)
    artists, counts = [], []

    for artist, count in all_:
        pdf.cell(297, 7, str(artist).ljust(95) + str(count).rjust(10),ln=1)
        artists.append(artist)
        counts.append(count)

    maxi = max(counts)
    idx = counts.index(maxi)

    values = np.array(counts)
    explode = [0 for _ in range(len(counts))]
    explode[idx] = 0.2
    colors = findNDifferentColors(len(counts))

    plt.pie(values, startangle=90, colors=colors, explode=explode, shadow=True)
    plt.title('Percentage of plays of each artist\'s songs')
    plt.axis('equal')

    labels = [f'{l}, {(s/sum(counts) * 100):0.2f}%' for l, s in zip(artists, counts)]
    plt.legend(bbox_to_anchor=(0.7, 0), loc='lower left', labels=labels)
    plt.show()

    # jakoś na wątkach to trzeba zrobić, by zapisac wykres do pliku, próbowałam kilka h, ale bez efektów

    pdf.output('artistsReport.pdf', 'F')

    return FileResponse(open('artistsReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def genresReport(request):
    all_ = findMostPopularGenres()

    # create pdf
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 20)

    pdf.cell(297, 10, 'The most listened music genres', ln=1, align='C')
    pdf.cell(297, 10, '', ln=1)

    pdf.set_font('courier', 'B', 14)
    pdf.cell(297, 14, f"{'Genre'.ljust(85)} {'Count'.ljust(50)}", ln=1)
    pdf.line(10, 40, 287, 40)
    pdf.set_font('courier', '', 12)
    genres, counts = [], []

    for genre, count in all_:
        pdf.cell(297, 7, str(genre).ljust(95) + str(count).rjust(10), ln=1)
        genres.append(genre)
        counts.append(count)

    pdf.output('genresReport.pdf', 'F')

    # plot
    maxi = max(counts)
    idx = counts.index(maxi)

    values = np.array(counts)
    explode = [0 for _ in range(len(counts))]
    explode[idx] = 0.2
    colors = findNDifferentColors(len(counts))

    plt.pie(values, startangle=90, colors=colors, explode=explode, shadow=True)
    plt.title('The most listened music genres')
    plt.axis('equal')

    labels = [f'{l}, {(s / sum(counts) * 100):0.2f}%' for l, s in zip(genres, counts)]
    plt.legend(bbox_to_anchor=(0.7, 0), loc='lower left', labels=labels)
    plt.show()

    return FileResponse(open('genresReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def usersReport(request):
    all_ = usersActivity()

    # create pdf
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 20)

    pdf.cell(297, 10, 'Users activity', ln=1, align='C')
    pdf.cell(297, 10, '', ln=1)

    pdf.set_font('courier', 'B', 14)
    pdf.cell(297, 14, f"{'User'.ljust(50)} {'Number of played songs'.ljust(50)}", ln=1)
    pdf.line(10, 40, 287, 40)
    pdf.set_font('courier', '', 12)
    users = []
    counts = []

    for user, count in all_:
        pdf.cell(297, 7, str(user).ljust(95) + str(count).rjust(10), ln=1)
        users.append(user)
        counts.append(count)

    pdf.output('usersReport.pdf', 'F')

    plt.bar(users, counts, color='#21a25b', width=0.6)
    plt.title('Number of played songs')
    plt.xlabel('User name')
    plt.ylabel('Number')
    plt.show()

    return FileResponse(open('usersReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def findMostPopularSongs():
    stats = StatSinglePlay.objects.all().order_by('song_id')
    result = []
    last = -1

    for stat in stats:
        if last == -1 or last != stat.song.id:
            last = stat.song.id
            result.append([stat.song.title, stat.song.artist.name, stat.count])
        else:
            result[-1][2] += stat.count

    result.sort(key=lambda x: x[2], reverse=True)

    return result


def findMostPopularUserSongs(user):
    stats = StatSinglePlay.objects.all().order_by('song_id')
    result = []
    last = -1

    for stat in stats:
        if stat.user.id == user.id:
            if last == -1 or last != stat.song.id:
                last = stat.song.id
                result.append([stat.song.title, stat.song.artist.name, stat.count])
            else:
                result[-1][2] += stat.count

    result.sort(key=lambda x: x[2], reverse=True)

    return result


def findFiveMostPopularUserSongs(user):
    result = findMostPopularUserSongs(user)

    # if there are less than 5 different played songs
    if len(result) < 5:
        return result[:len(result)]
    return result[:5]


def findMostPopularArtist():
    stats = StatSinglePlay.objects.all()
    result, artists = [], []

    for stat in stats:
        if stat.song.artist.name not in artists:
            result.append([stat.song.artist.name, stat.count])
            artists.append(stat.song.artist.name)
        else:
            idx = artists.index(stat.song.artist.name)
            result[idx][1] += stat.count

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def findMostPopularUserArtists(user):
    stats = StatSinglePlay.objects.all()
    result = []
    artists = []

    for stat in stats:
        if stat.user.id == user.id:
            if stat.song.artist not in artists:
                result.append([stat.song.artist.name, stat.count])
                artists.append(stat.song.artist)
            else:
                idx = artists.index(stat.song.artist)
                result[idx][1] += stat.count

    # print(result)
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def findFiveMostPopularUserArtists(user):
    result = findMostPopularUserArtists(user)

    # if there are less than 5 different played songs
    if len(result) < 5:
        return result[:len(result)]
    return result[:5]


def findMostPopularUserGenres(user):
    stats = StatSinglePlay.objects.all()
    result, genres = [], []

    for stat in stats:
        if user.id == stat.user_id:
            if stat.song.genre.name not in genres:
                result.append([stat.song.genre.name, stat.count])
                genres.append(stat.song.genre.name)
            else:
                idx = genres.index(stat.song.genre.name)
                result[idx][1] += stat.count

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def findFiveMostPopularGenres(user):
    result = findMostPopularUserGenres(user)

    if len(result) < 5:
        return result[:len(result)]
    return result[:5]


def findMostPopularGenres():
    stats = StatSinglePlay.objects.all()
    result, genres = [], []

    for stat in stats:
        if stat.song.genre.name not in genres:
            result.append([stat.song.genre.name, stat.count])
            genres.append(stat.song.genre.name)
        else:
            idx = genres.index(stat.song.genre.name)
            result[idx][1] += stat.count

    result.sort(key=lambda x: x[1], reverse=True)

    return result


def usersActivity():
    stats = StatSinglePlay.objects.all().order_by('user')
    result = []
    last = ""

    for stat in stats:
        if last == "" or last != stat.user.username:
            result.append([stat.user.username, stat.count])
            last = stat.user.username
        else:
            result[-1][1] += stat.count

    result.sort(key=lambda x: x[1], reverse=True)

    return result