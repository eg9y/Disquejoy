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
                Field('uploader', 'text'),
                Field('title'),
                Field('artist', 'text'),
                Field('popularity'),
                Field('upvotes','integer', default=0), #notice we are forcing age to be a int
                Field('updated_on', 'datetime',
                      update=datetime.datetime.utcnow()),
                )



db.track.uploader.writable = db.track.uploader.readable = False
db.track.title.writable = db.track.title.readable = False
db.track.artist.writable = db.track.artist.readable = False
db.track.popularity.writable = db.track.popularity.readable = False
db.track.updated_on.writable = db.track.updated_on.readable = False
db.track.upvotes.writable = False
db.track.upvotes.readable = False
db.define_table('spotify_user',
                Field('username'),
                Field('email'),
                )

db.define_table(
    'artist', #we are creating a table call artist
    Field('name'), # first field is call name, so thats why we use to grab data employees.name
    Field('upvotes','integer') #notice we are forcing age to be a int
    )


db.spotify_user.username.writable = db.spotify_user.username.readable = False
db.spotify_user.email.writable = db.spotify_user.email.readable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
