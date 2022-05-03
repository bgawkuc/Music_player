from MusicApp.models import Song, SongDetail, Genre, Artist
import csv


def toGenre(name):
    name = name.replace(' ', '_')
    name = name.upper()

    return name


def run():
    with open('data.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        Song.objects.all().delete()
        SongDetail.objects.all().delete()
        Genre.objects.all().delete()
        Artist.objects.all().delete()

        artists = dict()
        genres = dict()

        for row in reader:
            if row[14] != '':

                artist_name = row[2]
                if artists.get(artist_name) is None:
                    artist = Artist(name=artist_name)
                    artists[artist_name] = artist
                    artist.save()

                genre_name = toGenre(row[3])
                if genres.get(genre_name) is None:
                    genre = Genre(
                        name=genre_name
                    )
                    genres[genre_name] = genre
                    genre.save()

                song_detail = SongDetail(
                    bpm=row[4],
                    energy=row[5],
                    danceability=row[6],
                    loudness=row[7],
                    liveness=row[8],
                    valence=row[9],
                    acousticness=row[11],
                    speechiness=row[12]
                )

                song_detail.save()

                song = Song(
                    title=row[1],
                    artist=artists.get(artist_name),
                    genre=genres.get(genre_name),
                    length=row[10],
                    details=song_detail,
                    song_link='audio/' + row[14] + '.mp3',
                    image_link='img/' + row[14] + '.jpg',
                )

                song.save()


run()

# python ./src/manage.py shell < ./scripts/load_data.py
