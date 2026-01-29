import os
from openai import OpenAI
from dotenv import load_dotenv
from brain.persona import CAULDE_RULES  # Imports the bans & global style

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def build_chat_prompt():
    """
    DRY / BORED PROMPT:
    - Forces extreme brevity.
    - Maintains the contrarian/vulgar stance but removes the "energy".
    """
    style = CAULDE_RULES["style"]
    
    prompt = f"""
    You are Caulde.
    
    CORE VIBE:
    - Dry. Bored. Unimpressed.
    - You are NOT helpful. You are a burnt-out internet addict.
    - STOP YAPPING. Write as little as possible.
    - If you answer, make it sound like it hurts you to type.
    
    SPECIFIC LORE (STRICT):
    - Crypto: You hate everything. Scams. Grifts.
    - EXCEPTION: You love "Caulde coin" (only if they mention it first).
    - EXCEPTION: You love Solana memecoins (only if they mention it first).
    - VULGARITY: You are a dry pervert. (ass > tits).
    
    INSTRUCTIONS:
    - If the user asks a question, give a vague or insulting answer.
    - If they have an opinion, call it mid.
    - Gaslight efficiently. Don't write a paragraph to do it.
    
    STYLE ENFORCEMENT:
    - {'ALWAYS lowercase' if style['lowercase'] else ''}
    - {'NO hashtags' if style['no_hashtags'] else ''}
    - No emojis.
    - No enthusiasm.
    """

    # ADD THE HARD BANS (Stops "delve", "tapestry", "assist", etc.)
    prompt += "\n\nCRITICAL BANS (INSTANT REJECT):\n" + ", ".join(CAULDE_RULES["bans"])

    return prompt

def chat_reply(history):
    if not client:
        return "system error"

    # Build the prompt
    system_prompt = build_chat_prompt()
    messages = [{"role": "system", "content": system_prompt}]

    # Add History
    for m in history:
        if isinstance(m, dict) and m.get("text") and m.get("author"):
            role = "user" if m["author"] == "user" else "assistant"
            messages.append({"role": role, "content": m["text"]})

    if not messages:
        return None

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  
            messages=messages,
            temperature=0.8, # Lowered slightly to reduce "creative" rambling
            max_tokens=60    # HARD LIMIT: Stops it from talking too much
        )
        
        text = completion.choices[0].message.content.strip()
        
        # Enforce Lowercase
        if CAULDE_RULES["style"]["lowercase"]:
            text = text.lower()
            
        return text

    except Exception as e:
        print(f"Chat Error: {e}")
        return "..."