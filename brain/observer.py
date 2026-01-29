import random
import time
import requests

from config import X_BEARER_TOKEN
from brain.post_generator import generate_post_intent
from brain.caulde_writer import write
from outputs.drafts import add_reply_draft
from outputs.stream_log import log_stream

# --- CONFIGURATION ---
OBSERVER_INTERVAL = 20  # Check every 20 seconds
ACCOUNTS_PER_BATCH = 3  # How many accounts to check per cycle

# Memory to prevent replying to the same tweet twice
SEEN_TWEETS = set()

WATCH_ACCOUNTS = [
    "cz_binance", "elonmusk", "VitalikButerin", "balajis", "coinbase",
    "StarPlatinum", "MetaGorgonite", "finnbags", "_Shadow36", "trading_axe",
    "0x_Broly", "riostoriches", "cobie", "cryptofergani", "Jayyakamii",
    "gudmansachs", "Dior100x", "AlexFinn", "0xSweep", "OrangeSBS",
    "barneyxbt", "cyrilXBT", "CryptoZin", "GordonGekko", "straightozero",
    "czyxx_i", "Ga__ke", "alexL_E_I", "EHuanglu", "dnasty_sol",
    "PicturesFoIder", "bubblemaps", "joeroganhq", "litteralyme0",
    "SolanaSensei", "waddles_eth", "Cupseyy", "scufffd", "Nijol71",
    "ZssBecker", "purpdevvv", "kirawontmiss", "BRICSinfo", "Kadotttt",
    "WhiteHouse", "json1444", "imperooterxbt", "UziCryptoo", "assasin_eth",
    "goyimpnl", "CryptoZin", "dxrnell", "litteralyme0", "novabyyte",
    "WeatherMonitors"
]

def fetch_recent_tweets(username: str):
    """
    Fetches the last 5 tweets from a user.
    """
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}

    try:
        # 1. Get User ID
        r = requests.get(
            f"https://api.twitter.com/2/users/by/username/{username}",
            headers=headers
        )
        if r.status_code != 200:
            if r.status_code == 429:
                log_stream(f"⚠️ RATE LIMIT HIT (429). Slowing down...")
            return []

        user_data = r.json().get("data")
        if not user_data:
            return []
            
        user_id = user_data["id"]

        # 2. Get Tweets
        r = requests.get(
            f"https://api.twitter.com/2/users/{user_id}/tweets",
            headers=headers,
            params={"max_results": 5} # Checks the 5 most recent
        )
        if r.status_code != 200:
            return []

        return r.json().get("data", [])
        
    except Exception as e:
        log_stream(f"⚠️ Observer API Error: {e}")
        return []

def observer_loop():
    log_stream("👀 OBSERVER: AGGRESSIVE MODE (20s). Deduplication Active.")

    while True:
        try:
            # Pick random targets
            targets = random.sample(WATCH_ACCOUNTS, ACCOUNTS_PER_BATCH)
            
            for account in targets:
                tweets = fetch_recent_tweets(account)

                if not tweets:
                    continue

                for tweet in tweets:
                    t_id = tweet["id"]
                    t_text = tweet["text"]

                    # THE FIX: Check if we already saw this specific tweet
                    if t_id in SEEN_TWEETS:
                        continue

                    # If new, process it immediately (100% chance)
                    log_stream(f"🚨 NEW TWEET by @{account}: '{t_text[:30]}...'")
                    
                    intent = generate_post_intent()
                    output = write(
                        intent=intent,
                        context_text=t_text
                    )

                    if output:
                        add_reply_draft(
                            text=output,
                            reply_to_id=t_id,
                            context=f"@{account}: {t_text}"
                        )
                        log_stream(f"✅ DRAFTED REPLY to @{account}")
                    
                    # Mark as seen so we don't spam it next loop
                    SEEN_TWEETS.add(t_id)

            # Sleep 20s
            time.sleep(OBSERVER_INTERVAL)

        except Exception as e:
            log_stream(f"❌ OBSERVER CRASH: {e}")
            time.sleep(60)