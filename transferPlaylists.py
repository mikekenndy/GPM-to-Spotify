import spotipy
from spotipy.oauth2 import SpotifyOAuth

from gmusicapi import Mobileclient

CLIENT_ID = 'GET CLIENT_ID FROM SPOTIFY DEV PORTAL'
CLIENT_SECRET = 'GET CLIENT_SECRET FROM SPOTIFY DEV PORTAL'
REDIRECT_URI = 'http://localhost:8888/callback/'  # Required for spotify auth
SPOTIFY_USERNAME = "YOUR SPOTIFY USERNAME"

GPM_USERNAME = "YOUR GOOGLE PLAY MUSIC USERNAME"
GPM_APP_PW = "GET TEMPORARY APP PASSWORD FROM GOOGLE"


def getGPMPlaylists():
    api = Mobileclient()

    api.login(GPM_USERNAME, GPM_APP_PW, api.FROM_MAC_ADDRESS)

    return api.get_all_user_playlist_contents()


def addPlaylistToSpotify(spotify, playlist):

    # Create playlist
    playlist_name = playlist['name'].strip()
    print('Beginning "{0}" transfer'.format(playlist_name), end='')
    playlist_created = spotify.user_playlist_create(SPOTIFY_USERNAME, playlist_name)

    tracks_to_add = []
    for track in playlist['tracks']:
        if 'track' in track:
            search_results = spotify.search(q='artist:{0} track:{1}'.format(track['track']['artist'], track['track']['title']), type='track', limit=1)
            if search_results['tracks']['items']:
                tracks_to_add.append("spotify:track:" + search_results['tracks']['items'][0]['id'])

    if len(tracks_to_add) > 100:
        chunks = [tracks_to_add[x:x + 50] for x in range(0, len(tracks_to_add), 50)]
        for chunk in chunks:
            spotify.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_created['id'], chunk)
    else:
        spotify.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_created['id'], tracks_to_add)

    print(' - Success')


# MAIN
allPlaylists = getGPMPlaylists()

spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope='playlist-modify-public', username=SPOTIFY_USERNAME, client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  redirect_uri=REDIRECT_URI))

for playlist in allPlaylists:
    addPlaylistToSpotify(spotify, playlist)