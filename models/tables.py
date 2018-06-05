# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

def get_user_email():
    return auth.user.email if auth.user is not None else None

db.define_table('track',
                Field('spotify_url'),
                Field('spotify_uri'),
                Field('image'),
                Field('uploader', 'text'),
                Field('title'),
                Field('artist', 'text'),
                Field('popularity'),
                Field('upvotes','integer', default=0), #notice we are forcing age to be a int
                Field('updated_on', 'datetime',
                      update=datetime.datetime.utcnow()),
                )

db.define_table('upvotes',
                Field('upvoter', 'text'),
                Field('song', 'text'),
                Field('songName', 'text', default = None),
                Field('uploaderOfSong', 'text'),
                Field('upvoterName', 'text', default = None),
                )

db.track.uploader.writable = db.track.uploader.readable = False
db.track.title.writable = db.track.title.readable = False
db.track.artist.writable = db.track.artist.readable = False
db.track.popularity.writable = db.track.popularity.readable = False
db.track.updated_on.writable = db.track.updated_on.readable = False
db.track.image.writable = db.track.image.readable = False
db.track.spotify_uri.writable = db.track.spotify_uri.readable = False
db.track.upvotes.writable = False
db.track.upvotes.readable = False
db.define_table('spotify_user',
    Field('image', default = None),
                Field('username'),
                Field('email')
                )

db.define_table(
    'artist', #we are creating a table call artist
    Field('name'), # first field is call name, so thats why we use to grab data employees.name
    Field('upvotes','integer') #notice we are forcing age to be a int
    )


db.spotify_user.username.writable = db.spotify_user.username.readable = False
db.spotify_user.email.writable = db.spotify_user.email.readable = False

db.define_table('eventDetails',
                Field('GIF'),
                Field('name_of_event'),
                Field('organizer_id'),
                Field('organizer_name'),
                Field('datetime'),
                Field('Area'),
                Field('description'))

db.define_table('eventMembers',
                Field('member_id'),
                Field('member_name'),
                Field('name_of_event'),
                Field('id_of_event'),
                Field('is_organizer_of_event_id')
                )

db.eventMembers.member_id.writable = db.eventMembers.member_id.readable = False
db.eventMembers.member_name.writable = db.eventMembers.member_name.readable = False
db.eventMembers.id_of_event.writable = db.eventMembers.id_of_event.readable = False
db.eventMembers.name_of_event.writable = db.eventMembers.name_of_event.readable = False
db.eventMembers.is_organizer_of_event_id.writable = db.eventMembers.is_organizer_of_event_id.readable = False

db.spotify_user.username.writable = db.spotify_user.username.readable = False
db.spotify_user.email.writable = db.spotify_user.email.readable = False

db.define_table('feed_info',
                Field('feed_type'),
                Field('user_id_active'),
                Field('user_name_active'),
                Field('user_id_passive', default = None),
                Field('user_name_passive', default = None),
                Field('song'),
                Field('song_picture')
                )

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
