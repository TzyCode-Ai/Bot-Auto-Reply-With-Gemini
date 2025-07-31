# reply.py

import aiohttp
import random
from config import GOOGLE_API_KEYS
from utils import log

used_keys = set()
last_text = None

async def generate_reply(prompt, lang='en', fallback_messages=[]):
    global last_text
    if not prompt:
        return random.choice(fallback_messages) if fallback_messages else ""

    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}

    message = (
        f"Reply to the following in {lang.upper()} using simple human-like sentence:\n"
        f"{prompt}\n\nKeep it friendly and short."
    )

    data = {"contents": [{"parts": [{"text": message}]}]}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as resp:
                if resp.status == 429:
                    used_keys.add(key)
                    log(f"⚠️ API key limit, mencoba key lain...")
                    return await generate_reply(prompt, lang, fallback_messages)
                result = await resp.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                if text.strip() == last_text:
                    return await generate_reply(prompt, lang, fallback_messages)
                last_text = text
                return text
        except Exception as e:
            log(f"❌ Gagal generate AI reply: {e}")
            return random.choice(fallback_messages) if fallback_messages else "Sorry, I can't reply now."

def get_api_key():
    available = [k for k in GOOGLE_API_KEYS if k not in used_keys]
    if not available:
        used_keys.clear()
        return random.choice(GOOGLE_API_KEYS)
    return random.choice(available)
