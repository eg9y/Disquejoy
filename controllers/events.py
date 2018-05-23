import spotipy
from spotipy import oauth2
import json
import re

# all sensitive info are stored in .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

def index():
    sp_oauth = getauth()
    access_token = login()
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return dict(results = results)
    else:
        return dict()

def get_events():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    events = []
    eventsDB = db().select(db.eventDetails.ALL)
    if eventsDB is None:
        return response.json(dict(
            events = events
        ))
    for i, r in enumerate(eventsDB):
        if i < end_idx - start_idx:
            t = dict(
                id = r.id,
                GIF=r.GIF,
                name_of_event=r.name_of_event,
                organizer_id=r.organizer_id,
                organizer_name=r.organizer_name,
                Area=r.Area,
                description=r.description
            )
            events.append(t)
        else:
            pass
    return response.json(dict(
        events = events
    ))

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

def upload():
	form = SQLFORM(db.eventDetails, deletable = True)
	error = None
	access_token = login()
	if access_token is None:
		redirect(URL('default', index))
	if form.process().accepted:
		sp = spotipy.Spotify(access_token)
		results = sp.current_user()
		q = db(db.eventDetails.name_of_event == form.vars.name_of_event).select().first()
		try:
			db(db.eventDetails.name_of_event == form.vars.name_of_event).select().first().update_record(GIF = form.vars.GIF, name_of_event = form.vars.name_of_event, organizer_id = results["id"], organizer_name = results["display_name"], Area = form.vars.Area, description = form.vars.description)
		except:
			error = 'URL is invalid'
			return dict(form = form, error = error)
		return dict(form = form,  error = None)
	return dict(form = form,  error = None)

#Method for debugging
def delete():
    q = (db.eventDetails.GIF == "https://media.giphy.com/media/2xDc7OxVp7nYfPcDuC/giphy.gif")
    events = db(q).delete()
    return response.json(dict(events = events))

def delete_memo():
    q = (db.eventDetails.id == request.vars.id)
    events = db(q).delete()
    return response.json(dict(events = events))