from outputs.stream_log import log_stream
from outputs.drafts import add_reply_draft

from brain.reply_writer import reply_to_mention


def think(event: dict):
    """
    Handles incoming events (mentions).
    This file is ONLY for replies.
    """

    if event.get("type") != "mention":
        return

    text = event.get("text", "").strip()
    source_id = event.get("source_id")

    if not text or not source_id:
        return

    log_stream("reply intent detected")

    try:
        reply = reply_to_mention(text)

        if reply:
            add_reply_draft(
                text=reply,
                reply_to_id=source_id,
                context=text
            )
            log_stream("reply draft created")

    except Exception as e:
        log_stream(f"reply error: {e}")
