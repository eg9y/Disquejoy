import spotipy
from spotipy import oauth2
import json
import re

# all sensitive info are stored in .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os


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
        return dict(auth_url=None, results=results, access_token=access_token, spotify_user = spotify_user)
    else:
        redirect(URL('api', 'index', vars=dict(msg='You must login to view your profiles!')))


def login():
    sp_oauth = getauth()
    access_token = ""
    if session.userinfo:
        print "IM IN BITCH"
        print session
        access_token = session.userinfo
    else:
        code = request.vars.code
        if code:
            access_token = sp_oauth.get_access_token(code)['access_token']
            session.userinfo = access_token
    return access_token


def profileInfo():
    sp_oauth = getAuth()
    access_token = login(sp_oauth)
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        q = (db.spotify_user.username == results["id"])
        spotify_user = db(q).select().first()
        return response.json(dict(spotify_user = spotify_user))
    else:
        return response.json(dict(spotify_user = None))

def getAuth():
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
    SCOPE = 'user-library-read'
    CACHE = '.spotipyoauthcache'
    sp_oauth = oauth2.SpotifyOAuth(
        SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)
    return sp_oauth


def get_token_client():
    access_token = login()
    return response.json(dict(access_token=access_token))

def discoverData():
    q = (db.spotify_user.username == request.vars.id)
    spotify_user = db(q).select().first()
    return response.json(spotify_user)


def retrieveTotalLikes():
    sp_oauth = getAuth()
    access_token = login(sp_oauth)
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        q = (db.track.uploader == results["id"])
        tracksUserUploaded = db(q).select()
        return response.json(dict(tracksUserUploaded = tracksUserUploaded))
    else:
        pass

#def deleteData():
#    q = (db.upvotes.songName == "None")
#    q2 = (db.upvotes.songName == "None").select()
#    db(q).delete()
#    return response.json(dict(q = q))

def retrieveTotalLikesGiven():
    sp_oauth = getAuth()
    access_token = login(sp_oauth)
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        q = (db.spotify_user.username == results["id"])
        spotify_user = db(q).select().first()
        q2 = (db.upvotes.upvoter == spotify_user.username)
        retrieveTotalLikesGiven = db(q2).select()
        return response.json(dict(retrieveTotalLikesGiven = retrieveTotalLikesGiven))
    else:
        pass

def retrieveTotalLikesReceived():
    sp_oauth = getAuth()
    access_token = login(sp_oauth)
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        q = (db.spotify_user.username == results["id"])
        spotify_user = db(q).select().first()
        q2 = (db.upvotes.uploaderOfSong == spotify_user.username)
        retrieveTotalLikesReceived = db(q2).select()
        return response.json(dict(retrieveTotalLikesReceived = retrieveTotalLikesReceived))
    else:
        pass
