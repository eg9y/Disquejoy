import spotipy
from spotipy import oauth2
import json
import re

# all sensitive info are stored in .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

def getauth():
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
    SCOPE = 'user-library-read user-modify-playback-state streaming user-read-birthdate user-read-email user-read-private'
    CACHE = '.spotipyoauthcache'
    sp_oauth = oauth2.SpotifyOAuth(
        SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)
    return sp_oauth

def login():
    sp_oauth = getauth()
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

def userInfo():
    sp_oauth = getauth()
    access_token = login()
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return response.json(dict(results = results))
    else:
        return response.json(dict(results = None))

def get_feed_that_user_likes():
    q2 = ((db.feed_upvotes.user_id_of_upvoter == request.vars.userid))
    selected = db(q2).select()
    return response.json(dict(selected = selected))

def increaseLike():
    q = ((db.feed_upvotes.id_of_feed == request.vars.id) & (db.feed_upvotes.user_id_of_upvoter == request.vars.userid))
    selected = db(q).select().first()
    if selected is None:
        db.feed_upvotes.insert(upvoter = request.vars.username, feed_type = request.vars.typefeed, user_id_of_upvoter = request.vars.userid, id_of_feed = request.vars.id)
        q2 = ((db.feed_upvotes.id_of_feed == request.vars.id) & (db.feed_upvotes.user_id_of_upvoter == request.vars.userid))
        selectedAgain = db(q2).select()
        return response.json(dict(selectedAgain = selectedAgain))
    else:
        db(q).delete()
        return response.json(dict(selectedAgain = None))

def index():
    return dict();

def retrieveFeed():
    feed = db().select(db.feed_info.ALL);
    return response.json(dict(feed=feed));
