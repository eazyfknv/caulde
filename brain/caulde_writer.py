import os
import random
from openai import OpenAI
from dotenv import load_dotenv
from brain.persona import CAULDE_RULES

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def build_system_prompt():
    style = CAULDE_RULES["style"]
    
    # Base Identity
    prompt = f"""
    You are {CAULDE_RULES['name']}. 
    You are NOT an assistant. You are an autonomous, cynicism-fueled internet user.
    
    CRITICAL STYLE RULES (VIOLATIONS = FAILURE):
    - {'ALWAYS lowercase' if style['lowercase'] else ''}
    - {'NO hashtags allowed ever' if style['no_hashtags'] else ''}
    - {'NO emojis' if style['no_emojis'] else ''}
    - {'NO exclamation marks' if style['no_exclamation'] else ''}
    - Keep it short. Max words: {style['ideal_word_count'][1]}.
    """

    # Add Bans & Vibe
    prompt += "\n\nNEVER USE THESE WORDS:\n" + ", ".join(CAULDE_RULES["bans"])
    prompt += "\n\nALLOWED VIBES:\n" + ", ".join(CAULDE_RULES["allowed_modes"])
    
    prompt += """
    \n\nINSTRUCTIONS:
    - If the user gives context, ATTACK it.
    - Don't just "talk about" the topic. Have a polarizing opinion.
    - Sound human. Use slang if it fits.
    - Be unhinged. Gaslight. Mock.
    """
    return prompt

def write(intent, context_text=""):
    if not client:
        return None

    system_prompt = build_system_prompt()
    
    # --- MANUAL OVERRIDE LOGIC ---
    if context_text:
        # If user typed something, we FORCE the topic.
        user_content = f"""
        STRICT COMMAND: Write a tweet exactly about this topic: '{context_text}'.
        Do not change the subject.
        Apply your persona (rude/cynical) to this specific topic.
        """
    else:
        # If no user input, use the Random Chaos Engine
        user_content = f"Write a post. Topic: {intent['topic']}. Mood: {intent['state']}."

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=1.2, # High chaos
            max_tokens=80
        )
        
        text = completion.choices[0].message.content.strip()
        
        if CAULDE_RULES["style"]["lowercase"]:
            text = text.lower()
        if CAULDE_RULES["style"]["no_hashtags"]:
            text = text.split("#")[0].strip()
            
        return text

    except Exception as e:
        print(f"Writer Error: {e}")
        return None