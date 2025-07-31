# utils.py

import os
import time
from datetime import datetime, timezone
from telethon.tl.functions.messages import GetHistoryRequest

# === LOGGING ===
def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

# === LOAD FALLBACK ===
def load_fallback_messages(path):
    if not os.path.exists(path):
        log(f"⚠️ File fallback tidak ditemukan: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# === IDLE CHECKING ===
async def get_last_message_time(client, group):
    try:
        result = await client(GetHistoryRequest(
            peer=group,
            limit=1,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        if result.messages:
            return result.messages[0].date.replace(tzinfo=timezone.utc).timestamp()
    except Exception as e:
        log(f"❌ Error mengambil pesan terakhir dari {group}: {e}")
    return 0

def should_send_idle_prompt(last_time, timeout_seconds):
    now = time.time()
    return (now - last_time) >= timeout_seconds

# === RATE LIMITER ===
_user_last_replies = {}

def rate_limiter(user_id, limit_per_minute):
    now = time.time()
    window_start = now - 60
    _user_last_replies.setdefault(user_id, [])
    # Hapus yang sudah lewat 60 detik
    _user_last_replies[user_id] = [ts for ts in _user_last_replies[user_id] if ts >= window_start]

    if len(_user_last_replies[user_id]) < limit_per_minute:
        _user_last_replies[user_id].append(now)
        return True
    return False
