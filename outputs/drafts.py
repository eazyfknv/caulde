import json
from pathlib import Path
from typing import List, Dict

from outputs.stream_log import log_stream
from outputs.x_poster import post_reply, post_tweet

DRAFTS_FILE = Path("shared/drafts.json")


# -------------------------
# FILE HELPERS
# -------------------------

def _read() -> List[Dict]:
    if not DRAFTS_FILE.exists():
        return []
    try:
        return json.loads(DRAFTS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _write(drafts: List[Dict]):
    DRAFTS_FILE.parent.mkdir(exist_ok=True)
    DRAFTS_FILE.write_text(
        json.dumps(drafts, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def _new_id(drafts: List[Dict]) -> int:
    # simple, stable, no collisions
    return max([d["id"] for d in drafts], default=0) + 1


# -------------------------
# CREATE
# -------------------------

def add_post_draft(text: str):
    drafts = _read()
    drafts.append({
        "id": _new_id(drafts),
        "kind": "post",
        "text": text,
        "posted": False,
        "source": None,
    })
    _write(drafts)
    log_stream("post draft created")


def add_reply_draft(text: str, reply_to_id: str, context: str):
    drafts = _read()
    drafts.append({
        "id": _new_id(drafts),
        "kind": "reply",
        "text": text,
        "posted": False,
        "source": reply_to_id,
        "context": context,   # 👈 store the question
    })
    _write(drafts)



# -------------------------
# READ
# -------------------------

def get_drafts() -> List[Dict]:
    return _read()


# -------------------------
# ACTIONS
# -------------------------

def approve_and_post(draft_id: int):
    drafts = _read()

    for d in drafts:
        if d["id"] == draft_id and not d["posted"]:
            if d["kind"] == "reply":
                post_reply(d["text"], d["source"])
            else:
                post_tweet(d["text"])

            d["posted"] = True
            log_stream("draft approved and posted")
            break

    _write(drafts)


def discard(draft_id: int):
    drafts = _read()

    for d in drafts:
        if d["id"] == draft_id and not d["posted"]:
            d["posted"] = True
            log_stream("draft discarded")
            break

    _write(drafts)
