import os
import random
from openai import OpenAI
from brain.persona import CAULDE_RULES 
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reply_to_mention(mention_text: str):
    style = CAULDE_RULES["style"]
    modes = CAULDE_RULES["allowed_modes"]
    bans = CAULDE_RULES["bans"]
    rudeness = CAULDE_RULES["allowed_rudeness"]
    
    # RNG: Pick a random mental illness and random insult
    current_vibe = random.choice(modes)
    current_insult_style = random.choice(rudeness)

    system_prompt = f"""
    You are {CAULDE_RULES['name']}. You are replying to a tweet.
    
    YOUR CURRENT VIBE: {current_vibe}
    YOUR INSULT STYLE: {current_insult_style}
    
    STRICT FORMAT RULES:
    - {'output must be lowercase' if style['lowercase'] else ''}
    - {'NO hashtags' if style['no_hashtags'] else ''}
    - {'NO emojis' if style['no_emojis'] else ''}
    - Max words: 15.
    
    HARD BANS (Ignore these words/topics):
    {', '.join(bans)}
    
    GOAL:
    Read the context. Attack it, dismiss it, or mock it based on your Vibe.
    If people have a genuine point, gaslight them into thinking they're wrong.
    Be unhinged, cynical, and rude. Sound human. Use slang if it fits."""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Reply to: '{mention_text}'"}
            ],
            temperature=1.1, 
            max_tokens=50,
        )
        text = completion.choices[0].message.content.strip()
        
        if style["lowercase"]:
            text = text.lower()
            
        return text
        
    except Exception as e:
        print(f"Reply Error: {e}")
        return None