import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import string


def get_random_id(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


CLIENT_ID = ''
CLIENT_SECRET = ''


class Spotify:
    def __init__(self):
        client_id = CLIENT_ID
        client_secret = CLIENT_SECRET
        spotify_scopes = ['playlist-read-collaborative', 'playlist-read-private']
        redirect_url = "https://spoty-tube-api.herokuapp.com/callback/"
        self.request = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                                 client_secret=client_secret,
                                                                 redirect_uri=redirect_url,
                                                                 scope=','.join((spotify_scopes))))

    ## grabs users playlist
    def get_user_playlists_list(self):
        playlists = []
        response = self.request.current_user_playlists()
        for item in response['items']:
            playlists.append(Playlist(item['name'], item['id']).__repr__())
        return playlists

    ##retrievs songs from playlist
    def get_tracks_from_playlists(self, playlists):
        tracks = []
        for playlist in playlists:
            tracks_from_playlist = self.request.playlist_items(
                playlist['playlist_id'])  ## grabs tracks from playlist id
            for item in tracks_from_playlist['items']:
                track = item['track']
                artist = track['artists'][0]['name']
                track_name = track['name']
                tracks.append(Track(artist, track_name).__repr__())
            playlist.update({'tracks': tracks})
            tracks = []
        return playlists  ##return playlists dict with 'tracks' keys


class Playlist:
    def __init__(self, playlist_name, playlist_id):
        self.playlist_name = playlist_name
        self.playlist_id = playlist_id

    def __repr__(self):
        return {'playlist_name': self.playlist_name, 'playlist_id': self.playlist_id}


class Track:
    def __init__(self, track_artist, track_name):
        self.track_artist = track_artist
        self.track_name = track_name
        self.id = get_random_id()

    def __repr__(self):
        return {'track_name': self.track_artist + " " + self.track_name, 'track_id': self.id, 'isSelected': False}
