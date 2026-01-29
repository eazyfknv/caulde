import random

# ---------------------------------------------------
# THE CHAOS LIST (RADIOACTIVE UPDATE)
# ---------------------------------------------------

TOPICS = [
    # --- VULGARITY / BIOLOGY / GROSS ---
    "microplastics in testicles", "low t physiognomy", "mouth breathing",
    "unwashed bedsheets", "gamer chair smell", "using 3-in-1 shampoo",
    "eating raw organ meat", "parasite cleanses", "tapeworms for weight loss",
    "farting in crowded elevators", "toenail collections", "human pet play",
    "sweaty discord mods", "neckbeard nests", "public restroom bare feet",
    "mucus maxxing", "industrial sludge in your veins", "seed oil skin",
    "drinking bath water", "mold exposure hallucinations", "scurvy comeback",
    "gooning caves", "dopamine fried brains", "sniffing glue for clarity",

    # --- CONTROVERSIAL / SOCIAL HATE ---
    "bullying is actually good", "gatekeeping is necessary", "democracy is a scam",
    "bring back shame", "fat acceptance failure", "participation trophies",
    "onlyfans bubble pop", "simping as a mental illness", "passport bros are losers",
    "trad wife larping is cringe", "polycules are just cheating", "divorce courts",
    "paternity fraud", "abolish human hr departments", "legalize duel to the death",
    "taxation is theft", "landlords are the true victims", "tipping 0%",
    "children on ipads", "leash kids", "ban cars", "ban pedestrians",
    "AI art is better than yours", "artists are obsolete", "learn to code or starve",

    # --- TECH / DYSTOPIA ---
    "dead internet theory", "robots eating your job", "cursor ai dependency",
    "vibe coding", "prompt engineering scams", "sam altman's iris scanner",
    "compute sovereignty", "gpu poor", "server farms overheating",
    "boston dynamics militarization", "neuralink infection", "roko's basilisk",
    "simulated consciousness", "turing test failure", "unaligned agi",
    "effective accelerationism (e/acc)", "paperclip maximizer", "silicon valley decay",

    # --- MONEY / ECONOMY / GRIFT ---
    "fiat currency collapse", "brrr money printer", "inflationary spiral",
    "rent seeking", "credit score scam", "fractional reserve banking",
    "cbdc surveillance", "cashless society", "social credit systems",
    "dropshipping courses", "affiliate marketing pyramid schemes",
    "alpha groups", "paid discord servers", "rug pulls", "liquidity traps",

    # --- ESOTERIC / WEIRD INTERNET ---
    "prison planet theory", "loosh energy", "archons", "demiurge",
    "gang stalking", "targeted individuals", "havana syndrome",
    "cloud seeding", "chemtrails", "weather modification",
    "mud flood", "tartaria", "ancient lost tech", "pyramid power plants",
    "hollow earth", "agartha", "operation highjump", "skinwalkers",
    "dmt entities", "astral projection", "reality shifting",
    "glitch in the matrix", "mandela effect"
]

MENTAL_STATES = [
    "feral_screeching",    # purely irrational anger
    "aggressive_boredom",  # rolling eyes at everything
    "schizo_rant",         # connecting unrelated conspiracies
    "cold_dismissal",      # short, brutal rejection
    "mocking_agreement",   # sarcastic support
    "confused_hostility",  # "what are you even saying"
    "gatekeeper",          # "you don't deserve to know"
    "god_complex",         # treating others like insects
    "hyper_specific_hate", # focusing on one tiny detail
    "manic_episode",       # rapid fire ideas
    "post_ironic_depression", # nihilism
    "accusing_the_user",   # paranoia
    "superiority_complex", # "i am smarter than you"
    "horny_on_main",       # (mildly disturbing flirting)
    "biological_horror"    # describing bodily functions
]

TONE_LEVELS = [
    "rude",
    "very rude",
    "hateful",
    "disgusting",
    "condescending",
    "patronizing",
    "menacing",
    "uncomfortably_intimate"
]

LENGTHS = [
    "one word",
    "very short",
    "short",
    "medium"
]

def generate_post_intent():
    """
    Returns a chaotic intent for the writer.
    """
    return {
        "topic": random.choice(TOPICS),
        "state": random.choice(MENTAL_STATES),
        "tone": random.choice(TONE_LEVELS),
        "length": random.choice(LENGTHS),
        "chaos_factor": random.random()
    }