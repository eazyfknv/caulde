import threading
import time
import os

# --- CRITICAL: Ensure these files don't import 'config' ---
from inputs.twitter_reader import fetch_new_mentions
from brain.thinker import think
from brain.idle_thinker import idle_think_loop
from brain.observer import observer_loop
from outputs.stream_log import log_stream

POLL_INTERVAL = 20

def mention_loop():
    log_stream("mention loop started")
    while True:
        try:
            events = fetch_new_mentions()
            for event in events:
                think(event)
        except Exception as e:
            log_stream(f"mention error: {e}")
        time.sleep(POLL_INTERVAL)

# --- NEW FUNCTION: Call this from app.py ---
def start_brain():
    log_stream("🧠 BRAIN STARTING UP...")
    threading.Thread(target=mention_loop, daemon=True).start()
    threading.Thread(target=idle_think_loop, daemon=True).start()
    threading.Thread(target=observer_loop, daemon=True).start()

if __name__ == "__main__":
    # This block only runs if you type 'python main.py' locally
    start_brain()
    while True:
        time.sleep(60)