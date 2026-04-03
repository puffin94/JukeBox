from tinydb import TinyDB, Query
from config import DB_PATH

db = TinyDB(DB_PATH)
Track = Query()

def get_track(button_id):
    result = db.search(Track.button == button_id)
    return result[0] if result else None

def add_track(button_id, title, artist, uri):
    db.insert({
        "button": button_id,
        "title": title,
        "artist": artist,
        "uri": uri,
        "play_count": 0
    })

def increment_play_count(button_id):
    db.update(
        lambda r: r.update({"play_count": r["play_count"] + 1}),
        Track.button == button_id
    )

def list_tracks():
    return db.all()