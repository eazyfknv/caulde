import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHAT_FILE = BASE_DIR / "shared" / "chat.json"

MAX_MESSAGES = 200


def _read():
    if not CHAT_FILE.exists():
        return []
    return json.loads(CHAT_FILE.read_text(encoding="utf-8"))


def _write(messages):
    CHAT_FILE.parent.mkdir(exist_ok=True)
    CHAT_FILE.write_text(
        json.dumps(messages[-MAX_MESSAGES:], ensure_ascii=False),
        encoding="utf-8"
    )


def add_message(author: str, text: str):
    messages = _read()
    messages.append({
        "author": author,
        "text": text,
        "ts": time.time()
    })
    _write(messages)


def get_messages():
    return _read()
