import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_DEVICE_NAME,
    VOLUME
)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))


def get_jukebox_device():
    """Find the librespot device, retry a few times in case it's warming up"""
    for _ in range(5):
        devices = sp.devices()
        for device in devices["devices"]:
            if device["name"] == SPOTIFY_DEVICE_NAME:
                return device["id"]
        time.sleep(1)
    return None


def play_track(uri):
    device_id = get_jukebox_device()
    if not device_id:
        print("Jukebox Spotify device not found — is librespot running?")
        return False

    sp.start_playback(device_id=device_id, uris=[uri])
    sp.volume(VOLUME, device_id=device_id)
    return True


def stop_playback():
    device_id = get_jukebox_device()
    if device_id:
        sp.pause_playback(device_id=device_id)


def current_track():
    playback = sp.current_playback()
    if playback and playback["is_playing"]:
        track = playback["item"]
        return {
            "title": track["name"],
            "artist": track["artists"][0]["name"],
            "duration_ms": track["duration_ms"],
            "progress_ms": playback["progress_ms"]
        }
    return None