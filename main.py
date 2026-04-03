import RPi.GPIO as GPIO
import time
from collections import deque
from config import ROW_PINS, COL_PINS
from tracks import get_track, increment_play_count
from spotify import play_track, current_track

GPIO.setmode(GPIO.BCM)
ROWS = "ABCDE"

# setup pins
for pin in ROW_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in COL_PINS:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

queue = deque()
currently_playing = None

def scan_buttons():
    for col_idx, col_pin in enumerate(COL_PINS):
        GPIO.output(col_pin, GPIO.LOW)
        for row_idx, row_pin in enumerate(ROW_PINS):
            if GPIO.input(row_pin) == GPIO.LOW:
                button_id = f"{ROWS[row_idx]}{col_idx + 1}"
                GPIO.output(col_pin, GPIO.HIGH)
                return button_id
        GPIO.output(col_pin, GPIO.HIGH)
    return None

def handle_queue():
    """If nothing is playing and queue has tracks, play next"""
    global currently_playing
    now = current_track()
    if not now and queue:
        next_track = queue.popleft()
        print(f"Playing: {next_track['title']} by {next_track['artist']}")
        play_track(next_track["uri"])
        increment_play_count(next_track["button"])
        currently_playing = next_track

try:
    print("Jukebox ready...")
    while True:
        button = scan_buttons()
        if button:
            track = get_track(button)
            if track:
                track["button"] = button
                queue.append(track)
                print(f"Queued: {track['title']} by {track['artist']} ({len(queue)} in queue)")
            else:
                print(f"No track assigned to {button}")
            time.sleep(0.5)  # debounce

        handle_queue()
        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()