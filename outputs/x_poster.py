import requests
from requests_oauthlib import OAuth1

from config import (
    X_API_KEY,
    X_API_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_SECRET,
)

auth = OAuth1(
    X_API_KEY,
    X_API_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_SECRET
)


def post_reply(text: str, reply_to_id: str):
    url = "https://api.twitter.com/2/tweets"

    payload = {
        "text": text,
        "reply": {
            "in_reply_to_tweet_id": reply_to_id
        }
    }

    r = requests.post(url, json=payload, auth=auth)

    if r.status_code in (200, 201):
        return r.json()

    if r.status_code == 403 and "duplicate content" in r.text.lower():
        return {"status": "duplicate"}

    raise Exception(f"post failed: {r.status_code} {r.text}")


def post_tweet(text: str):
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}
    r = requests.post(url, json=payload, auth=auth)
    if r.status_code != 201:
        raise Exception(r.text)

