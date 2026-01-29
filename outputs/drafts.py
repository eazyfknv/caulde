# Simple in-memory storage for drafts
DRAFTS = []
next_id = 1

def get_drafts():
    return DRAFTS

def add_post_draft(text):
    global next_id
    DRAFTS.insert(0, {
        "id": next_id,
        "kind": "post",
        "text": text,
        "posted": False
    })
    next_id += 1

def add_reply_draft(text, reply_to_id, context):
    global next_id
    DRAFTS.insert(0, {
        "id": next_id,
        "kind": "reply",
        "text": text,
        "reply_to_id": reply_to_id,
        "context": context, # The tweet we are replying to
        "posted": False
    })
    next_id += 1

def discard(draft_id):
    global DRAFTS
    DRAFTS = [d for d in DRAFTS if d["id"] != draft_id]

def discard_all():
    """
    Wipes all drafts immediately.
    """
    global DRAFTS
    DRAFTS.clear()

def approve_and_post(draft_id):
    # Find the draft
    draft = next((d for d in DRAFTS if d["id"] == draft_id), None)
    if not draft:
        return False
    
    # In a real bot, here is where you call twitter_api.post_tweet(draft['text'])
    print(f"✅ POSTING TO TWITTER: {draft['text']}")
    
    # Mark as posted (or remove)
    draft["posted"] = True
    # Optional: Remove immediately after posting
    discard(draft_id)
    return True