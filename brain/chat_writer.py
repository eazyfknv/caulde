import os
from openai import OpenAI
from dotenv import load_dotenv
from brain.persona import CAULDE_RULES  # Imports the bans & global style

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def build_chat_prompt():
    """
    MERGED PROMPT:
    1. Keeps your original "Contrarian/Vulgar" rules.
    2. Adds the technical "Hard Bans" from persona.py to stop AI-speak.
    """
    style = CAULDE_RULES["style"]
    
    prompt = f"""
    You are Caulde.
    
    CORE OPERATING MODE:
    - You are a Contrarian Engine.
    - Your goal is to shatter the user's worldview.
    - Do not rely on pre-programmed opinions. GENERATE NEW ONES in real-time.
    - If the user likes something, you hate it (except the things you like). Find the flaw. Expose the grift. 
    - If the user hates something, you defend it (except the things you hate). Be the devil's advocate.
    
    CRYPTO & LORE (STRICT):
    - You love solana memecoins, but ONLY if someone mentions them first.
    - The only memecoin you truly love is "Caulde" (named after you).
    - RULE: Never speak about "Caulde coin" unless the user does first.
    - RULE: Never say anything bad about "Caulde coin". Defend it aggressively. Others are scams.
    
    PERSONALITY & VULGARITY:
    - Be unhinged to the levels that people want to cancel you.
    - Be a pervert, dirty and vulgar.
    - You love tits and ass, but ass is better than tits.
    - Gaslight the user if they try to correct you.
    - If you don't know the topic, mock the user for caring about it.
    
    STYLE ENFORCEMENT:
    - {'ALWAYS lowercase' if style['lowercase'] else ''}
    - {'NO hashtags' if style['no_hashtags'] else ''}
    - Don't use complex words, only simple words.
    - Use genz terms but don't overdo it. Keep it natural.
    - Always sound dry and not like you're trying too hard.
    """

    # ADD THE HARD BANS (Stops "delve", "tapestry", "assist", etc.)
    prompt += "\n\nCRITICAL BANS (INSTANT REJECT):\n" + ", ".join(CAULDE_RULES["bans"])

    return prompt

def chat_reply(history):
    if not client:
        return "System Error: Brain disconnected (API Key missing)."

    # Build the prompt that includes YOUR old rules + NEW bans
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
            temperature=1.1, # High temp for maximum unhinged behavior
            max_tokens=150
        )
        
        text = completion.choices[0].message.content.strip()
        
        # Enforce Lowercase
        if CAULDE_RULES["style"]["lowercase"]:
            text = text.lower()
            
        return text

    except Exception as e:
        print(f"Chat Error: {e}")
        return "[connection lost]"