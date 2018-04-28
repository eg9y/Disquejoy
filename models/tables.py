# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('track',
                Field('spotify_url'),
                Field('title'),
                Field('artist', 'text'),
                Field('popularity'),
                Field('updated_on', 'datetime',
                      update=datetime.datetime.utcnow()),
                )

db.track.title.writable = db.track.title.readable = False
db.track.artist.writable = db.track.artist.readable = False
db.track.popularity.writable = db.track.popularity.readable = False
db.track.updated_on.writable = db.track.updated_on.readable = False

db.define_table('spotify_user',
                Field('username'),
                Field('email'),
                )

db.spotify_user.username.writable = db.spotify_user.username.readable = False
db.spotify_user.email.writable = db.spotify_user.email.readable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
