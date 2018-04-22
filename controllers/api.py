import spotipy
from spotipy import oauth2    
import json

#all sensitive info are stored in .env
from dotenv import load_dotenv
load_dotenv()
import os

def login():
    SPOTIPY_CLIENT_ID=os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")
    SCOPE = 'user-library-read'
    CACHE = '.spotipyoauthcache'
    sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )
    access_token = ""
    token_info = sp_oauth.get_cached_token()

    access_token = None
    if token_info:
        access_token = token_info['access_token']
    else:
        code = request.vars.code
        if code:
            print "Found Spotify auth code in Request URL! Trying to get valid access token..."
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token'] 
    return access_token

def index():         
    access_token = login()
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        response.flash = "Fetched access token!"    
        return dict(auth_url=None, results=results, access_token=access_token)
    else:
        auth_url = sp_oauth.get_authorize_url()
        htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
        return dict(auth_url=auth_url, results=None, access_token=None)

def show_tracks(results):
    all_songs = []
    for i, item in enumerate(results['items']):
        track = item['track']
        all_songs.append({
            "_id": i,
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "popularity": track['popularity']
        })
    return all_songs

# Needs to define username
def get_playlists():
    access_token = login()
    sp = spotipy.Spotify(access_token)
    username = request.args(0)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            results = sp.user_playlist(username, playlist['id'],
                                        fields="tracks,next")
            tracks = results['tracks']
            every_tracks = []
            
            every_tracks.append(show_tracks(tracks))
            while tracks['next']:
                tracks = sp.next(tracks)
                every_tracks.append(show_tracks(tracks))
    return dict(every_tracks=every_tracks)    
