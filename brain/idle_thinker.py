import random
import time

from brain.post_generator import generate_post_intent
from brain.caulde_writer import write
from outputs.drafts import add_post_draft
from outputs.stream_log import log_stream

IDLE_INTERVAL = 600  # 30 minutes


def idle_think_loop():
    log_stream("idle thinker started")

    while True:
        try:
            if random.random() < 0.95:
                intent = generate_post_intent()

                output = write(
                    intent=intent,
                    context_text=None
                )

                if output:
                    add_post_draft(output)
                    log_stream("idle post drafted")

        except Exception as e:
            log_stream(f"idle thinker error: {e}")

        time.sleep(IDLE_INTERVAL)
