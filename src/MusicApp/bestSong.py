import pandas as pd

from MusicApp.models import Song
from Statistics.models import StatDurationPlay


def findBestSong(user):
    allListenedSongs = StatDurationPlay.objects.all()
    songsObjects, songsTitles, songsTimeUnits = [], [], []

    for listenedSong in allListenedSongs:
        if listenedSong.user.username == user.username:
            if listenedSong.song.title in songsTitles:
                idx = songsTitles.index(listenedSong.song.title)
                songsTimeUnits[idx] += listenedSong.time_units
            else:
                songsTitles.append(listenedSong.song.title)
                songsTimeUnits.append(listenedSong.time_units)
                songsObjects.append(listenedSong.song)

    allTime = sum(songsTimeUnits)
    results = {'bpm': 0, 'energy': 0, 'danceability': 0, 'liveness': 0, 'valence': 0, 'acousticness': 0,
               'speechiness': 0}

    for i in range(len(songsObjects)):
        results['bpm'] += (songsObjects[i].details.bpm * songsTimeUnits[i]) / allTime
        results['energy'] += (songsObjects[i].details.energy * songsTimeUnits[i]) / allTime
        results['danceability'] += (songsObjects[i].details.danceability * songsTimeUnits[i]) / allTime
        results['liveness'] += (songsObjects[i].details.liveness * songsTimeUnits[i]) / allTime
        results['valence'] += (songsObjects[i].details.valence * songsTimeUnits[i]) / allTime
        results['acousticness'] += (songsObjects[i].details.acousticness * songsTimeUnits[i]) / allTime
        results['speechiness'] += (songsObjects[i].details.speechiness * songsTimeUnits[i]) / allTime

    return results


def songsGenerator(user):
    allSongs = Song.objects.all()
    results = findBestSong(user)
    bestSongDF = pd.DataFrame([results])
    songList = []

    for songElement in allSongs:
        d = songElement.details
        df2 = pd.DataFrame([[d.bpm, d.energy, d.danceability, d.liveness, d.valence, d.acousticness, d.speechiness]], columns=results.keys())
        songList.append((abs(bestSongDF.corrwith(df2, 1)[0]), songElement))

    songList.sort(key=lambda x: x[0], reverse=True)

    # for i in range(5):
        # print(songList[i][1].title)

    return songList[:5]
