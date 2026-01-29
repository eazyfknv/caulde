import random
import time
import requests

from config import X_BEARER_TOKEN
from brain.post_generator import generate_post_intent
from brain.caulde_writer import write
from outputs.drafts import add_reply_draft
from outputs.stream_log import log_stream

OBSERVER_INTERVAL = 2700  # 45 minutes

WATCH_ACCOUNTS = [
    "cz_binance",
    "elonmusk",
    "VitalikButerin",
    "balajis",
    "coinbase",
    "StarPlatinum",
    "MetaGorgonite",
    "finnbags",
    "_Shadow36",
    "trading_axe",
    "0x_Broly",
    "riostoriches",
    "cobie",
    "cryptofergani",
    "Jayyakamii",
    "gudmansachs",
    "Dior100x",
    "AlexFinn",
    "0xSweep",
    "OrangeSBS",
    "barneyxbt",
    "cyrilXBT",
    "CryptoZin",
    "GordonGekko",
    "straightozero",
    "czyxx_i",
    "Ga__ke",
    "alexL_E_I",
    "EHuanglu",
    "dnasty_sol",
    "PicturesFoIder",
    "bubblemaps",
    "joeroganhq",
    "litteralyme0",
    "SolanaSensei",
    "waddles_eth",
    "Cupseyy",
    "scufffd",
    "Nijol71",
    "ZssBecker",
    "purpdevvv",
    "kirawontmiss",
    "BRICSinfo",
    "Kadotttt",
    "WhiteHouse",
    "json1444",
    "imperooterxbt",
    "UziCryptoo",
    "assasin_eth",
    "goyimpnl",
    "CryptoZin",
    "dxrnell",
    "litteralyme0",
    "novabyyte",
    "WeatherMonitors"
    ]



def fetch_recent_tweets(username: str):
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}

    r = requests.get(
        f"https://api.twitter.com/2/users/by/username/{username}",
        headers=headers
    )
    if r.status_code != 200:
        return []

    user_id = r.json()["data"]["id"]

    r = requests.get(
        f"https://api.twitter.com/2/users/{user_id}/tweets",
        headers=headers,
        params={"max_results": 5}
    )
    if r.status_code != 200:
        return []

    return r.json().get("data", [])


def observer_loop():
    log_stream("observer loop started")

    while True:
        try:
            if random.random() < 0.2:
                account = random.choice(WATCH_ACCOUNTS)
                tweets = fetch_recent_tweets(account)

                if not tweets:
                    time.sleep(OBSERVER_INTERVAL)
                    continue

                tweet = random.choice(tweets)

                intent = generate_post_intent()

                output = write(
                    intent=intent,
                    context_text=tweet["text"]
                )

                if output:
                    add_reply_draft(
                        text=output,
                        reply_to_id=tweet["id"],
                        context=tweet["text"]
                    )
                    log_stream("observer reply drafted")

        except Exception as e:
            log_stream(f"observer error: {e}")

        time.sleep(OBSERVER_INTERVAL)
