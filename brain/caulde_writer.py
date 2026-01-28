import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

# Get key from Environment (Railway/Render compatible)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("CRITICAL: OPENAI_API_KEY missing in caulde_writer.")
    client = None
else:
    client = OpenAI(api_key=api_key)

def write(intent, context_text=""):
    if not client:
        return None

    system_prompt = """
    You are Caulde. An autonomous, controversial crypto-native shitposter.
    Style: Lowercase, rude, short, accelerationist.
    Topic: Crypto, AI, VCs, or general disdain for modern society.
    Goal: Write a single tweet based on the INTENT provided.
    """
    
    user_content = f"Intent: {intent}"
    if context_text:
        user_content += f"\nContext/Topic: {context_text}"

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.9,
            max_tokens=60
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Writer Error: {e}")
        return None