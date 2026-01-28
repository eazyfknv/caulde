from fastapi import FastAPI, Body, Header
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    StreamingResponse,
)

from pathlib import Path
import time
import threading
import random
from typing import Optional

# --- IMPORTS ---
from brain.caulde_writer import write
from brain.post_generator import generate_post_intent
from outputs.drafts import get_drafts, approve_and_post, discard
from outputs.stream_log import read_stream
from brain.chat_writer import chat_reply

app = FastAPI()

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"

# IN-MEMORY STORAGE
USER_SESSIONS = {}

# --- UI ROUTES ---
@app.get("/", response_class=HTMLResponse)
def home():
    return (TEMPLATES_DIR / "stream.html").read_text(encoding="utf-8")

@app.get("/admin", response_class=HTMLResponse)
def admin():
    return (TEMPLATES_DIR / "drafts.html").read_text(encoding="utf-8")

# --- CHAT API WITH LOGS ---

@app.post("/chat")
async def chat(
    payload: dict = Body(...), 
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID") 
):
    print(f"\n📨 [HTTP] Chat Request Received.")
    
    message = payload.get("message", "").strip()
    if not message:
        print("⚠️ [HTTP] Message empty.")
        return JSONResponse({"error": "empty"}, status_code=400)
    
    if not x_session_id:
        print("⚠️ [HTTP] No Session ID provided by browser.")
        # Fallback for testing tools without headers
        x_session_id = "default_debug_session"

    print(f"👤 [HTTP] Session ID: {x_session_id}")
    print(f"💬 [HTTP] Message: {message}")

    # 1. Init Session
    if x_session_id not in USER_SESSIONS:
        USER_SESSIONS[x_session_id] = []

    # 2. Save User Msg
    USER_SESSIONS[x_session_id].append({"author": "user", "text": message})

    # 3. Spawn Thread
    def reply_later(sess_id):
        print(f"⏳ [THREAD] Thinking started for {sess_id}...")
        time.sleep(random.uniform(0.5, 1.5))
        
        # Get history
        history = USER_SESSIONS.get(sess_id, [])[-8:]
        
        try:
            print(f"🧠 [THREAD] Calling Brain...")
            reply = chat_reply(history) # Calls the debugged chat_writer
            
            if reply:
                if sess_id in USER_SESSIONS:
                    USER_SESSIONS[sess_id].append({"author": "caulde", "text": reply})
                    print(f"⚡ [THREAD] Saved reply to session.")
                else:
                    print(f"⚠️ [THREAD] Session {sess_id} disappeared!")
            else:
                print(f"⚠️ [THREAD] Brain returned None.")
                
        except Exception as e:
            print(f"❌ [THREAD] CRASH: {e}")

    threading.Thread(target=reply_later, args=(x_session_id,), daemon=True).start()

    return JSONResponse({"status": "ok"})

@app.get("/chat/messages")
def chat_messages(x_session_id: Optional[str] = Header(None, alias="X-Session-ID")):
    # Debug: Print only if ID is missing to avoid spam
    if not x_session_id:
        # print("⚠️ [POLL] No Session ID in poll request") 
        return []
    
    msgs = USER_SESSIONS.get(x_session_id, [])
    # print(f"🔍 [POLL] Returning {len(msgs)} messages for {x_session_id}")
    return msgs

# --- OTHER ENDPOINTS (UNCHANGED) ---

@app.get("/drafts")
def drafts():
    return get_drafts()

@app.post("/approve/{id}")
def approve(id: int):
    approve_and_post(id)
    return JSONResponse({"status": "posted"})

@app.post("/discard/{id}")
def discard_draft(id: int):
    discard(id)
    return JSONResponse({"status": "discarded"})

@app.post("/prompt")
async def prompt_post(payload: dict = Body(...)):
    prompt = payload.get("prompt", "").strip()
    intent = generate_post_intent()
    text = write(intent=intent, context_text=prompt)
    if text:
        from outputs.drafts import add_post_draft
        add_post_draft(text)
    return JSONResponse({"status": "ok", "text": text})

@app.get("/stream", response_class=PlainTextResponse)
def stream():
    return read_stream()

@app.get("/stream/live")
def stream_live():
    def event_generator():
        last_len = 0
        while True:
            try:
                data = read_stream()
                if len(data) > last_len:
                    chunk = data[last_len:]
                    last_len = len(data)
                    for line in chunk.split('\n'):
                        if line.strip():
                            yield f"data: {line}\n\n"
            except:
                pass
            time.sleep(0.5)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# ... (rest of your app.py code) ...

@app.on_event("startup")
async def startup_event():
    print("🚀 SERVER STARTING: Launching Brain...")
    try:
        from main import start_brain
        start_brain()
        print("✅ BRAIN LAUNCHED SUCCESSFULLY")
    except Exception as e:
        print(f"❌ BRAIN FAILED TO START: {e}")
        # This usually means a file inside main (like twitter_reader)
        # is still trying to import 'config'.