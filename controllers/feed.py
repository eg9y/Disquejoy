def index():
    return dict();

def retrieveFeed():
    feed = db().select(db.feed_info.ALL);
    return response.json(dict(feed=feed));
    
