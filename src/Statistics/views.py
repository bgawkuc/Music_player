import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

from django.http import HttpResponse, FileResponse
from django.shortcuts import render

from MusicApp.models import Song
from Statistics.models import StatSinglePlay, StatDurationPlay
from fpdf import FPDF

matplotlib.use("Agg")


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
    fiveBestSongs = findBestFiveSongs(findMostPopularUserSongs(user))
    fiveBestArtists = findBestFiveSongs(findMostPopularUserArtists(user))
    fiveBestGenres = findBestFiveSongs(findMostPopularUserGenres(user))

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


def createPDF():
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 20)

    return pdf


def addToPDF(pdf, data, title, tableTitlesData, tableContentData):
    pdf.set_font('courier', 'B', 20)
    pdf.cell(297, 10, title, ln=1, align='C')
    pdf.cell(297, 10, '', ln=1)
    pdf.set_font('courier', 'B', 14)

    if len(tableTitlesData) == 5:
        pdf.cell(297, 14, f" {tableTitlesData[0].ljust(tableTitlesData[1])} {tableTitlesData[2].ljust(tableTitlesData[3])} {tableTitlesData[4]}", ln=1)
    elif len(tableTitlesData) == 7:
        pdf.cell(297, 14, f"{tableTitlesData[0].ljust(tableTitlesData[1])} {tableTitlesData[2].ljust(tableTitlesData[3])} "
                          f"{tableTitlesData[4].ljust(tableTitlesData[5])}  {tableTitlesData[6]}", ln=1)

    pdf.line(10, 40, 287, 40)
    pdf.set_font('courier', '', 12)
    data1, data2, data3 = [], [], []
    idx = 1

    if len(tableTitlesData) == 5:
        for el1, el2 in data:
            pdf.cell(297, 7, str(idx).ljust(tableContentData[0]) + str(el1).ljust(tableContentData[1]) + str(el2).rjust(tableContentData[2]), ln=1)
            data1.append(el1)
            data2.append(el2)
            idx += 1

    elif len(tableTitlesData) == 7:
        for el1, el2, el3 in data:
            pdf.cell(297, 7, str(idx).ljust(tableContentData[0]) + str(el1).ljust(tableContentData[1]) +
                     str(el2).ljust(tableContentData[2]) + str(el3).rjust(tableContentData[3]), ln=1)
            data1.append(el1)
            data2.append(el2)
            data3.append(el3)
            idx += 1

    return data1, data2, data3, pdf


def addContentToMyReport(pdf, data, tableContentData, title, tableTitlesData, xLabel, yLabel, id_):
    data1, data2, data3, pdf = addToPDF(pdf, data, title, tableTitlesData, tableContentData)
    x = [str(i) for i in range(1, len(data1) + 1)]

    if len(tableTitlesData) == 5:
        createBarPlot(x, data2, title, xLabel, yLabel, id_)
    elif len(tableTitlesData) == 7:
        createBarPlot(x, data3, title, xLabel, yLabel, id_)

    pdf.image('image' + str(id_) + '.jpg', x=23.5, w=250, h=176)


def createPiePlot(title, data, counts, id_):
    maxi = max(counts)
    idx = counts.index(maxi)
    values = np.array(counts)

    explode = [0 for _ in range(len(counts))]
    explode[idx] = 0.1
    colors = findNDifferentColors(len(counts))

    plt.pie(values, colors=colors, explode=explode, shadow=False, startangle=140)
    plt.title(title)
    plt.axis('equal')

    labels = ['id:' f'{l} - {(s / sum(counts) * 100):0.2f}%' for l, s in zip(data, counts)]
    plt.legend(bbox_to_anchor=(0.8, 0), loc='lower left', labels=labels)
    plt.savefig("image" + str(id_) + ".jpg", dpi=300)
    plt.close()
    plt.clf()


def createBarPlot(xValues, yValues, title, xLabel, yLabel, id_):
    plt.bar(xValues, yValues, color='#21a25b', width=0.6)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    for i in range(len(xValues)):
        plt.text(i, yValues[i], yValues[i], ha='center')

    plt.savefig("image" + str(id_) + ".jpg", dpi=300)
    plt.close()
    plt.clf()


# create different reports


def myReport(request):
    user = request.user
    fiveBestSongs = findBestFiveSongs(findMostPopularUserSongs(user))
    fiveBestArtists = findBestFiveSongs(findMostPopularUserArtists(user))
    fiveBestGenres = findBestFiveSongs(findMostPopularUserGenres(user))

    pdf = createPDF()

    tableTitlesData = ['Id', 7, 'Title', 50, 'Artist', 25, 'Count']
    tableContentData = [10, 60, 26, 10]
    addContentToMyReport(pdf, fiveBestSongs, tableContentData, 'Number of plays of my 5 best songs', tableTitlesData, 'Song ID', 'Number', 5)

    tableTitlesData = ['Id', 7, 'Artist', 75, 'Count']
    tableContentData = [10, 92, 0]
    addContentToMyReport(pdf, fiveBestArtists, tableContentData, 'Number of plays of my best 5 artist\'s song', tableTitlesData, 'Artist', 'Number', 6)

    tableTitlesData = ['Id', 7, 'Genre', 75, 'Count']
    tableContentData = [10, 92, 0]
    addContentToMyReport(pdf, fiveBestGenres, tableContentData, 'Number of plays of my best 5 genres',
                         tableTitlesData, 'Genre', 'Number', 7)

    pdf.output('myReport.pdf', 'F')

    return FileResponse(open('myReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def songsReport(request):
    all_ = findMostPopularSongs()
    tableTitlesData = ['Id', 7, 'Title', 50, 'Artist', 25, 'Count']
    tableContentData = [10, 60, 26, 10]

    _, _, counts, pdf = addToPDF(createPDF(), all_, 'The most listened songs', tableTitlesData, tableContentData)

    x = [str(i) for i in range(1, len(all_)+1)]
    createBarPlot(x, counts, 'The most listened songs', 'Song ID', 'Number', "")

    pdf.image('image.jpg', x=23.5, w=250, h=176)
    pdf.output('songsReport.pdf', 'F')

    return FileResponse(open('songsReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def artistsReport(request):
    all_ = findMostPopularArtist()
    tableTitlesData = ['Id', 7, 'Artist', 75, 'Count']
    tableContentData = [10, 92, 0]

    _, counts, _,  pdf = addToPDF(createPDF(), all_, 'The most listened artists', tableTitlesData, tableContentData)

    x = [str(i) for i in range(1, len(all_)+1)]
    createPiePlot('The most listened artists', x, counts, 2)

    pdf.image('image2.jpg', x=-5, w=250, h=176)
    pdf.output('artistsReport.pdf', 'F')

    return FileResponse(open('artistsReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def genresReport(request):
    all_ = findMostPopularGenres()
    tableTitlesData = ['Id', 7, 'Genre', 75, 'Count']
    tableContentData = [10, 92, 0]

    _, counts, _,  pdf = addToPDF(createPDF(),all_, 'The most listened music genres', tableTitlesData, tableContentData)

    x = [str(i) for i in range(1, len(all_)+1)]
    createPiePlot('The most listened music genres', x, counts, 3)

    pdf.image('image3.jpg', x=-5, w=250, h=176)
    pdf.output('genresReport.pdf', 'F')

    return FileResponse(open('genresReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


def usersReport(request):
    all_ = usersActivity()
    tableTitlesData = ['Id', 7, 'User', 60, 'Number of played songs']
    tableContentData = [10, 92, 0]

    users, counts, _, pdf = addToPDF(createPDF(), all_, 'Users activity', tableTitlesData, tableContentData)

    createBarPlot(users, counts, 'Users activity', 'User name', 'Number', 4)

    pdf.image('image4.jpg', x=23.5, w=250, h=176)
    pdf.output('usersReport.pdf', 'F')

    return FileResponse(open('usersReport.pdf', 'rb'), as_attachment=False, content_type='application/pdf')


# select songs by most different categories


def findBestFiveSongs(songs):
    # if there are less than 5 different played songs
    if len(songs) < 5:
        return songs[:len(songs)]
    return songs[:5]


def helpFindMostPopularSongs(stat, last, result):
    if last == -1 or last != stat.song.id:
        last = stat.song.id
        result.append([stat.song.title, stat.song.artist.name, stat.count])
    else:
        result[-1][2] += stat.count

    return last


def findMostPopularSongs():
    stats = StatSinglePlay.objects.all().order_by('song_id')
    result = []
    last = -1

    for stat in stats:
        last = helpFindMostPopularSongs(stat, last, result)

    result.sort(key=lambda x: x[2], reverse=True)

    return result


def findMostPopularUserSongs(user):
    stats = StatSinglePlay.objects.all().order_by('song_id')
    result = []
    last = -1

    for stat in stats:
        if stat.user.id == user.id:
            last = helpFindMostPopularSongs(stat, last, result)

    result.sort(key=lambda x: x[2], reverse=True)

    return result


def helpFindMostPopularArtists(stat, artists, result):
    if stat.song.artist not in artists:
        result.append([stat.song.artist.name, stat.count])
        artists.append(stat.song.artist)
    else:
        idx = artists.index(stat.song.artist)
        result[idx][1] += stat.count


def findMostPopularArtist():
    stats = StatSinglePlay.objects.all()
    result, artists = [], []

    for stat in stats:
        helpFindMostPopularArtists(stat, artists, result)

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def findMostPopularUserArtists(user):
    stats = StatSinglePlay.objects.all()
    result = []
    artists = []

    for stat in stats:
        if stat.user.id == user.id:
            helpFindMostPopularArtists(stat, artists, result)

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def helpFindMostPopularGenres(stat, genres, result):
    if stat.song.genre.name not in genres:
        result.append([stat.song.genre.name, stat.count])
        genres.append(stat.song.genre.name)
    else:
        idx = genres.index(stat.song.genre.name)
        result[idx][1] += stat.count


def findMostPopularGenres():
    stats = StatSinglePlay.objects.all()
    result, genres = [], []

    for stat in stats:
        helpFindMostPopularGenres(stat, genres, result)

    result.sort(key=lambda x: x[1], reverse=True)

    return result


def findMostPopularUserGenres(user):
    stats = StatSinglePlay.objects.all()
    result, genres = [], []

    for stat in stats:
        if user.id == stat.user_id:
            helpFindMostPopularGenres(stat, genres, result)

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
