import json

def getSongsJson(songs):

    songs_json = []
    for song in songs:
        minutes = str(song.length // 60)
        seconds = song.length % 60
        if seconds < 10:
            seconds *= 10
        seconds = str(seconds)

        ent = {
            'name':          song.title,
            'artist':        song.artist.name,
            'url':           '/static/' + song.song_link,
            'cover_art_url': '/static/' + song.image_link,
            'duration':      minutes + ':' + seconds,
            'genre':         song.genre.name,
            'id':            song.id
        }

        songs_json.append(ent)

    variables = {
        'title':      'Music',
        'songs_json': json.dumps(songs_json)
    }

    return variables
