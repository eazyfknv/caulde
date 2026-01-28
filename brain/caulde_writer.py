from openai import OpenAI
from config import OPENAI_API_KEY
import random

client = OpenAI(api_key=OPENAI_API_KEY)

# ultra short nukes
ONE_WORD = [
    "mid", "nah", "cope", "interesting", "sure",
    "ok", "wild", "crazy", "insane", "embarrassing",
]

# dismissive short replies
SHORT = [
    "that’s not it",
    "wrong angle",
    "try again",
    "you just got here",
    "this again",
    "bold take",
    "slow down",
    "not impressive",
    "you thought this hit",
]

# parody-wrong factual answers (clearly fake)
FAKE_FACTS = [
    "runs on vibes",
    "powered by bad decisions",
    "depends on mercury retrograde",
    "compiled emotionally",
    "hosted in a google doc",
    "built different unfortunately",
    "it worked yesterday",
]

# gaslight classics
GASLIGHT = [
    "we already covered this",
    "this was obvious",
    "nobody said that",
    "read it again slower",
    "you misunderstood on purpose",
]

SYSTEM_PROMPT = """
you are caulde.

this is a parody account.
you are not informative.
you are not helpful.

rules:
- lowercase only
- ONE sentence only
- max 8 words preferred
- no emojis
- no hashtags
- no explaining
- no teaching
- no consistency
- boredom > aggression

style:
- gen z shitposting
- nonchalant
- dismissive
- impulsive
- typed without thinking

everything should feel accidental.
"""

def _pick_response(contextual: bool) -> str:
    roll = random.random()

    if roll < 0.20:
        return random.choice(ONE_WORD)
    if roll < 0.45:
        return random.choice(SHORT)
    if roll < 0.70:
        return random.choice(GASLIGHT)
    return random.choice(FAKE_FACTS)

def write(intent: dict, context_text: str | None) -> str:
    # for replies, we mostly ignore the content on purpose
    if context_text:
        # 80% pure canned chaos (anti-bot)
        if random.random() < 0.8:
            return _pick_response(contextual=True)

        # 20% let the model riff, still constrained
        user_prompt = f"""
someone said:
\"\"\"{context_text}\"\"\"

reply like you barely read it.
dismissive.
one sentence.
no explanation.
"""
    else:
        # standalone posts = slightly more room
        if random.random() < 0.6:
            return _pick_response(contextual=False)

        user_prompt = """
write a standalone post.

requirements:
- sarcastic
- dismissive
- not deep
- not helpful
- sounds like a thought you didn’t finish
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=1.35,
        max_tokens=18,
    )

    text = response.choices[0].message.content.strip().lower()
    text = text.replace("\n", " ").strip()

    # enforce one short sentence hard
    text = text.split(".")[0]
    words = text.split()
    if len(words) > 8:
        words = words[:8]

    return " ".join(words)
