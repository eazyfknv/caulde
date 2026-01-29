from fastapi import FastAPI, Body, Header, Request
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
from typing import Optional, Dict, List

# --- IMPORTS ---
from brain.caulde_writer import write
from brain.post_generator import generate_post_intent
# IMPORTED discard_all
from outputs.drafts import get_drafts, approve_and_post, discard, discard_all
from outputs.stream_log import read_stream, log_stream
from brain.chat_writer import chat_reply

app = FastAPI()

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"

# --- IN-MEMORY SESSION STORAGE ---
SESSIONS: Dict[str, List[dict]] = {}

# --- UI ROUTES ---
@app.get("/", response_class=HTMLResponse)
def home():
    return (TEMPLATES_DIR / "stream.html").read_text(encoding="utf-8")

@app.get("/admin", response_class=HTMLResponse)
def admin():
    return (TEMPLATES_DIR / "drafts.html").read_text(encoding="utf-8")

# --- CHAT API ---

@app.get("/chat/messages")
def get_chat_history(x_session_id: Optional[str] = Header(None, alias="X-Session-ID")):
    if not x_session_id:
        return []
    return SESSIONS.get(x_session_id, [])

@app.post("/chat")
async def chat(
    payload: dict = Body(...), 
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID") 
):
    if not x_session_id:
        session_id = "default"
    else:
        session_id = x_session_id

    if session_id not in SESSIONS:
        SESSIONS[session_id] = []

    user_text = payload.get("message", "").strip()
    
    if user_text:
        SESSIONS[session_id].append({"author": "user", "text": user_text})
        response_text = chat_reply(SESSIONS[session_id])
        if response_text:
            SESSIONS[session_id].append({"author": "assistant", "text": response_text})
    else:
        response_text = "..."

    return JSONResponse({"role": "assistant", "content": response_text})

# --- DRAFTS & POSTING API ---

@app.post("/prompt")
async def prompt_post(payload: dict = Body(...)):
    prompt = payload.get("prompt", "").strip()
    text = write(intent=None, context_text=prompt)
    if text:
        from outputs.drafts import add_post_draft
        add_post_draft(text)
    return JSONResponse({"status": "ok", "text": text})

@app.post("/generate_post")
async def generate_random_post():
    intent = generate_post_intent()
    text = write(intent=intent, context_text=None)
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

@app.get("/drafts")
def list_drafts():
    return get_drafts()

@app.post("/approve/{draft_id}")
def approve(draft_id: int):
    approve_and_post(draft_id)
    return {"status": "ok"}

@app.post("/discard/{draft_id}")
def discard_post(draft_id: int):
    discard(draft_id)
    return {"status": "ok"}

# --- CLEAR ALL ROUTE ---
@app.post("/discard_all")
def clear_all_drafts():
    discard_all()
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    print("🚀 SERVER STARTING...")
    try:
        from main import start_brain
        start_brain()
        print("✅ BRAIN ONLINE")
    except Exception as e:
        print(f"❌ BRAIN ERROR: {e}")