from pathlib import Path
from datetime import datetime

LOG_FILE = Path("shared/stream.log")


def log_stream(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    LOG_FILE.parent.mkdir(exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def read_stream() -> str:
    if not LOG_FILE.exists():
        return ""
    return LOG_FILE.read_text(encoding="utf-8")
