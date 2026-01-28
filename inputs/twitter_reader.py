import requests
from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env locally (Railway ignores .env, but this is safe)
load_dotenv()

# ===== ENV VARS =====
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

USERNAME = "cauldesol"  # must match @handle exactly
STATE_FILE = Path("shared/last_seen_id.txt")

_user_id = None
_last_seen_id = None


# ===== STATE HELPERS =====
def load_last_seen():
    if STATE_FILE.exists():
        return STATE_FILE.read_text().strip()
    return None


def save_last_seen(tweet_id: str):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(str(tweet_id))


_last_seen_id = load_last_seen()


# ===== MAIN LOGIC =====
def fetch_new_mentions():
    global _last_seen_id, _user_id

    if not X_BEARER_TOKEN:
        print("ERROR: X_BEARER_TOKEN not set")
        return []

    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}"
    }

    # Resolve user ID once
    if not _user_id:
        user_url = f"https://api.twitter.com/2/users/by/username/{USERNAME}"
        r = requests.get(user_url, headers=headers)

        if r.status_code != 200:
            print("User lookup failed:", r.status_code, r.text)
            return []

        _user_id = r.json()["data"]["id"]

    # Fetch mentions
    mentions_url = f"https://api.twitter.com/2/users/{_user_id}/mentions"
    params = {
        "max_results": 5,
        "tweet.fields": "id,text,created_at",
    }

    if _last_seen_id:
        params["since_id"] = _last_seen_id

    r = requests.get(mentions_url, headers=headers, params=params)

    if r.status_code != 200:
        print("Mentions fetch failed:", r.status_code, r.text)
        return []

    data = r.json()
    tweets = data.get("data", [])

    events = []

    for tweet in reversed(tweets):
        _last_seen_id = tweet["id"]
        save_last_seen(_last_seen_id)

        events.append({
            "type": "mention",
            "text": tweet["text"],
            "source_id": tweet["id"],
        })

    return events
