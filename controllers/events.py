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

def getComments():
    rows = db(db.comments.id_comment_belongs_to == request.vars.id).select()
    return response.json(dict(rows = rows))

def add_comment():
    sp_oauth = getauth()
    access_token = login()
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        q = (db.spotify_user.username == results["id"])
        spotify_user = db(q).select().first()
        db.comments.insert(comment_type = request.vars.id, commentText = request.vars.commentText, id_comment_belongs_to = request.vars.id, pictureOfCommenter = spotify_user.image, nameOfCommenter = results['display_name'], idOfCommenter = spotify_user.username)
        return response.json(dict(message = "ok", spotify_user = spotify_user))
    else:
        return response.json(dict(message = "nok"))

def get_current_user_info():
    sp_oauth = getauth()
    access_token = login()
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return response.json(dict(results = results))
    else:
        return response.json(dict(results = None))

def get_current_user_events():
    rows = db(db.eventMembers.member_id == request.vars.id).select()
    return response.json(dict(rows = rows))

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
        numberOfComments = db(db.comments.id_comment_belongs_to == r.id).count()
        if i < end_idx - start_idx:
            t = dict(
                id = r.id,
                GIF=r.GIF,
                name_of_event=r.name_of_event,
                organizer_id=r.organizer_id,
                organizer_name=r.organizer_name,
                datetime = r.datetime,
                Area=r.Area,
                description=r.description,
                numberOfCommentsInFeed = numberOfComments
            )
            events.append(t)
        else:
            pass
    return response.json(dict(
        events = events
    ))

def add_member():
    sp_oauth = getauth()
    access_token = login()
    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        q = (db.spotify_user.username == results["id"])
        spotify_user = db(q).select().first()
        q = db((db.eventMembers.member_id == results["id"]) & (db.eventMembers.member_name == results["display_name"]) & (db.eventMembers.name_of_event == request.vars.name) & (db.eventMembers.id_of_event == request.vars.id) & (db.eventMembers.is_organizer_of_event_id == False)).select().first()
        if q is None:
            number = db.eventMembers.insert(member_id = results["id"], member_name = results["display_name"], name_of_event = request.vars.name, id_of_event = request.vars.id, is_organizer_of_event_id = False, profilePicture = spotify_user.image)
            row = db(db.eventMembers.id == number).select().first()
            return response.json(dict(row = row))
        else:
            db(db.eventMembers.id == q.id).delete()
            row = db().select(db.eventMembers.ALL)
            return response.json(dict(row = row))
    else:
        return response.json(dict(row = none))

def getauth():
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
    SCOPE = 'user-library-read user-modify-playback-state streaming user-read-birthdate user-read-email user-read-private'
    CACHE = '.spotipyoauthcache'
    sp_oauth = oauth2.SpotifyOAuth(
        SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)
    return sp_oauth

def get_event_members():
    rows = db(db.eventMembers.id_of_event == request.vars.id).select()
    return response.json(dict(rows = rows))

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
        try:
            q = (db.spotify_user.username == results["id"])
            spotify_user = db(q).select().first()
            if results["email"] is not None and len(results["images"]) != 0:
                row = db(db.eventDetails.name_of_event == form.vars.name_of_event).select().first().update_record(GIF = form.vars.GIF, name_of_event = form.vars.name_of_event, organizer_id = results["id"], organizer_name = results["display_name"], datetime = form.vars.datetime, Area = form.vars.Area, description = form.vars.description)
                db.feed_info.insert(feed_type="EVENT", user_id_active=results["id"], user_name_active=results["display_name"],title = form.vars.name_of_event,song=None, song_picture=None, profilePicture = spotify_user.image)
                db.eventMembers.insert(member_id = results["id"], member_name = results["display_name"], name_of_event = form.vars.name_of_event, id_of_event = row.id, is_organizer_of_event_id = True, profilePicture = spotify_user.image)
            else:
                pass
        except:
            return dict(form = form, error = "")
        redirect(URL('events', index))
        return dict(form = form, error = None)
	return dict(form = form,  error = None)

def update():
    q = db(db.eventDetails.id == request.vars.id).select().first().update_record(GIF = request.vars.GIFurl, name_of_event = request.vars.title,datetime = request.vars.datetime, Area = request.vars.locationOfEvent, description = request.vars.description)
    return response.json(dict(q = q))

def delete_member():
    q = db((db.eventMembers.member_id == request.vars.user) & (db.eventMembers.id_of_event == request.vars.id)).delete()
    a = db().select(db.eventMembers.ALL);
    return response.json(dict(a=a));

#Method for debugging
def delete():
    q = (db.eventDetails.GIF == "https://media.giphy.com/media/2xDc7OxVp7nYfPcDuC/giphy.gif")
    events = db(q).delete()
    return response.json(dict(events = events))

def delete_memo():
    q = (db.eventDetails.id == request.vars.id)
    events = db(q).delete()
    return response.json(dict(events = events))
