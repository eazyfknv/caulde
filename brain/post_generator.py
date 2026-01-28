import random


TOPICS = [
    "crypto",
    "technology",
    "internet culture",
    "money",
    "power",
    "status",
    "attention",
    "nothing in particular",
    "whatever people are arguing about",
]

MENTAL_STATES = [
    "dismissive",
    "bored_contempt",
    "tired_bullish",
    "calm_doom",
    "confidently_wrong",
    "detached_observer",
]

TONE_LEVELS = [
    "mild",
    "rude",
    "very rude",
]

LENGTHS = [
    "very short",
    "short",
    "medium",
]


def generate_post_intent():
    """
    Returns an abstract intent.
    This is NEVER posted directly.
    """
    return {
        "topic": random.choice(TOPICS),
        "state": random.choice(MENTAL_STATES),
        "tone": random.choice(TONE_LEVELS),
        "length": random.choice(LENGTHS),
        "wrongness": random.random(),  # 0.0–1.0 (how confidently wrong)
    }
