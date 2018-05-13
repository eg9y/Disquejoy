import spotipy
from spotipy import oauth2
import json
import re

# all sensitive info are stored in .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os


def login(sp_oauth):
    access_token = ""
    token_info = sp_oauth.get_cached_token()

    access_token = None
    if token_info:
        access_token = token_info['access_token']
    else:
        code = request.vars.code
        if code:
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
    return access_token


def getAuth():
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
    SCOPE = 'user-library-read'
    CACHE = '.spotipyoauthcache'
    sp_oauth = oauth2.SpotifyOAuth(
        SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)
    return sp_oauth


def index():
    sp_oauth = getAuth()
    access_token = login(sp_oauth)
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        q = (db.spotify_user.username == results["id"])
        spotify_user = db(q).select().first()
        if spotify_user is None:
            if hasattr(results, 'email'):
                db.spotify_user.insert(
                    username=results["id"], email=results["email"])
            else:
                db.spotify_user.insert(
                    username=results["id"], email=None)
        else:
            session.flash = "Exists"
        return dict(auth_url=None, results=results, access_token=access_token)
    else:
        auth_url = sp_oauth.get_authorize_url()
        htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
        return dict(auth_url=auth_url, results=None, access_token=None)


def logout():
    os.remove(".spotipyoauthcache")
    redirect(URL('disquejoy', 'api', 'index'))


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

# TODO: Avoid track by popular artist
def upload():
    form = SQLFORM(db.track, deletable=True)
    if form.process().accepted:
        error = None
        sp_oauth = getAuth()
        access_token = login(sp_oauth)
        sp = spotipy.Spotify(access_token)
        q = (db.track.spotify_url == form.vars.spotify_url)        
        try:
            realURL = re.search(r'[0-9][^?]+', form.vars.spotify_url).group(0)
            track = sp.track(realURL)
        except:
            error = 'Please enter correct URL'
            db(q).delete()
            return dict(form=form, error=error)
        if track["popularity"] > 20:
            error = 'This track is too popular (Higher than 20). "' + \
                track["album"]["name"] + \
                    '"-'+ track["album"]["artists"][0]["name"]+ " has a popularity of " + str(track["popularity"])
            db(q).delete()
            return dict(form=form, error=error)
        checkSame = (db.track.artist == track["album"]["artists"][0]["name"])
        if db(checkSame).select().first() is not None:
            logger.info("Tests")
            error = '"'+track["album"]["name"] + \
                '"-' + track["album"]["artists"][0]["name"] +' has already been uploaded.'
            db(checkSame).delete()
            return dict(form=form, error=error)
        else:
            # track_details = sp.audio_features([realURL])
            track_row = db(q).select().first()
            track_row.update_record(
                artist=track["album"]["artists"][0]["name"], title=track["album"]["name"], popularity=track["popularity"])
            redirect(URL('default', 'index'))
    return dict(form=form, error=None)

def get_playlists():
    sp_oauth = getAuth()
    access_token = login(sp_oauth)
    sp = spotipy.Spotify(access_token)
    username = request.args(0)
    playlists = sp.user_playlists(username)
    every_tracks = []
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
