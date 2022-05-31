from typing import Optional

from django.contrib.auth.models import User
from django.db.models import Q

from MusicApp.models import Playlist, Song, PlaylistSong, PlaylistFollow


def createPlaylist(name: str, user: User, privacy_setting: bool) -> bool:
    playlist = Playlist(name=name, owner=user, is_private=privacy_setting)
    playlist.save()

    followPlaylist(playlist, user)

    return True


def deletePlaylist(id: int) -> bool:
    playlist = Playlist.objects.get(id=id)

    if playlist is None:
        print("Playlist does not exist.")
        return False

    playlist.delete()

    return True


def changePrivacy(playlist: Playlist, privacy_setting: bool) -> bool:
    playlist.is_private = privacy_setting
    playlist.save()

    if privacy_setting is False:
        playlist_follows = PlaylistFollow.objects.filter(~Q(user=playlist.owner), playlist=playlist).all()
        playlist_follows.delete()

    return True


def followPlaylist(playlist: Playlist, user: User) -> bool:
    if PlaylistFollow.objects.filter(playlist=playlist, user=user).first() is not None:
        print("User is currently following this playlist.")
        return False

    playlist_follow = PlaylistFollow(playlist=playlist, user=user)
    playlist_follow.save()

    return True


def unfollowPlaylist(playlist: Playlist, user: User) -> bool:
    if playlist.owner == user:
        # if the playlist is deleted so is the follow (cascade)
        print("The playlist owner cannot unfollow their playlist.")
        return False

    playlist_follow = PlaylistFollow.objects.get(playlist=playlist, user=user)
    if playlist is None:
        print("User is not following this playlist.")
        return False

    playlist_follow.delete()

    return True


def addSong(playlist: Playlist, song: Song) -> bool:
    if PlaylistSong.objects.filter(song=song).first() is not None:
        print("Song exists in playlist")
        return False

    playlist_song = PlaylistSong(playlist=playlist, song=song)
    playlist_song.save()

    return True


def deleteSong(playlist: Playlist, song: Song) -> bool:
    songs = PlaylistSong.objects.get(playlist=playlist, song=song)
    if songs is None:
        print("Song does not exist in this playlist.")
        return False

    songs.delete()

    return True
