import random
import time
import requests

from config import X_BEARER_TOKEN
from brain.post_generator import generate_post_intent
from brain.caulde_writer import write
from outputs.drafts import add_reply_draft
from outputs.stream_log import log_stream

# --- CONFIGURATION ---
# AGGRESSIVE MODE: Checks 3 random accounts every 20 seconds.
OBSERVER_INTERVAL = 20  
ACCOUNTS_PER_BATCH = 3

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
            # If 429, we are being rate limited.
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
            params={"max_results": 5}
        )
        if r.status_code != 200:
            return []

        return r.json().get("data", [])
        
    except Exception as e:
        log_stream(f"⚠️ Observer API Error: {e}")
        return []

def observer_loop():
    log_stream("👀 OBSERVER: AGGRESSIVE MODE (20s Interval)")

    while True:
        try:
            # Pick random targets
            targets = random.sample(WATCH_ACCOUNTS, ACCOUNTS_PER_BATCH)
            
            for account in targets:
                tweets = fetch_recent_tweets(account)

                if not tweets:
                    continue

                # Pick one tweet
                tweet = random.choice(tweets)
                
                # REMOVED PROBABILITY CHECK - ALWAYS DRAFTS
                log_stream(f"🚨 FOUND TWEET by @{account}: '{tweet['text'][:30]}...'")
                
                intent = generate_post_intent()
                
                # Generate reply
                output = write(
                    intent=intent,
                    context_text=tweet["text"] # Feed the tweet content to the Brain
                )

                if output:
                    add_reply_draft(
                        text=output,
                        reply_to_id=tweet["id"],
                        context=f"@{account}: {tweet['text']}"
                    )
                    log_stream(f"✅ DRAFTED REPLY to @{account}")

            # Short sleep
            time.sleep(OBSERVER_INTERVAL)

        except Exception as e:
            log_stream(f"❌ OBSERVER CRASH: {e}")
            time.sleep(60)