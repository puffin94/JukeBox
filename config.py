from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_DEVICE_NAME = os.getenv("SPOTIFY_DEVICE_NAME")

# button matrix pins
ROW_PINS = [4, 17, 27, 22, 5]       # A-E
COL_PINS = [6, 13, 19, 26, 21, 20, 16, 12, 7, 8]  # 1-10

DB_PATH = "db/tracks.json"

# audio
VOLUME = 80  # 0-100