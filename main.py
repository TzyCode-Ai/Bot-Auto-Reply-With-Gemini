# main.py

import os
import asyncio
import random
from telethon import TelegramClient, events
from config import API_ID, API_HASH
from reply import generate_reply
from utils import log, load_fallback_messages, get_last_message_time, should_send_idle_prompt, rate_limiter

SESSIONS_FOLDER = "sessions"
PESAN_FOLDER = "pesan/daftar-pesan-list"
FALLBACK_FOLDER = "balasan"

IDLE_TIMEOUT = 60  # detik
IDLE_MESSAGES_ID = [
    "Halo semuanya", "busyeh dah sepii amat", "Ada yang online?", "sibuk keknya nih", "apa nih poker tah?"
]
IDLE_MESSAGES_EN = [
    "Hi guys", "Anyone online?", "Let’s activate the group", "Coffee break", "Say something"
]

user_reply_counter = {}
group_reply_state = {}  # per group reply control


def get_account_count():
    try:
        return int(input("🔢 Masukkan jumlah akun Telegram yang ingin digunakan: "))
    except ValueError:
        return 1

def get_target_groups():
    return input("📌 Masukkan username grup yang ingin dipantau (pisahkan dengan koma): ").split(',')

def get_language():
    lang = input("🌐 Pilih bahasa (id/en): ").strip().lower()
    return "en" if lang not in ["id", "en"] else lang

def get_reply_limit():
    try:
        return int(input("🔁 Masukkan maksimal jumlah balasan berturut-turut per grup (default 2): ") or 2)
    except ValueError:
        return 2


async def start_bot(account_index, api_id, api_hash, groups, lang, reply_limit):
    session_name = os.path.join(SESSIONS_FOLDER, f"account{account_index+1}")
    session_file = session_name + ".session"

    client = TelegramClient(session_name, api_id, api_hash)

    if os.path.exists(session_file):
        await client.connect()
        if not await client.is_user_authorized():
            log(f"⚠️ Session ditemukan tapi tidak terautentikasi untuk akun {account_index+1}, login ulang.")
            await client.start()
        else:
            log(f"✅ Menggunakan session yang sudah ada untuk akun {account_index+1}")
    else:
        await client.start()
        log(f"✅ Akun {account_index+1} berhasil login sebagai {await client.get_me()}")

    fallback_path = os.path.join(FALLBACK_FOLDER, f"fallback-{lang}.txt")
    fallback_messages = load_fallback_messages(fallback_path)

    idle_messages = IDLE_MESSAGES_EN if lang == "en" else IDLE_MESSAGES_ID

    for group in groups:
        group = group.strip()

        @client.on(events.NewMessage(chats=group))
        async def handler(event):
            if event.out or not event.message.text:
                return

            group_id = str(event.chat_id)
            sender_id = event.sender_id

            if group_id not in group_reply_state:
                group_reply_state[group_id] = {"count": 0, "last_user": None}

            if group_reply_state[group_id]["last_user"] != sender_id:
                group_reply_state[group_id]["count"] = 0
                group_reply_state[group_id]["last_user"] = sender_id

            if group_reply_state[group_id]["count"] >= reply_limit:
                log(f"⏳ Grup {group_id} melebihi limit {reply_limit} balasan berturut-turut, menunggu user lain.")
                return

            if not rate_limiter(sender_id, 3):
                log(f"⏳ Melebihi limit balasan per menit untuk user {sender_id}, skip.")
                return

            prompt = event.message.text
            reply_text = await generate_reply(prompt, lang=lang, fallback_messages=fallback_messages)
            try:
                await event.reply(reply_text)
                log(f"💬 Balas ke {sender_id} di {group_id} => {reply_text}")
                group_reply_state[group_id]["count"] += 1
            except Exception as e:
                log(f"❌ Gagal membalas: {e}")

    async def idle_checker():
        while True:
            for group in groups:
                try:
                    last_time = await get_last_message_time(client, group.strip())
                    if should_send_idle_prompt(last_time, IDLE_TIMEOUT):
                        msg = random.choice(idle_messages)
                        await client.send_message(group.strip(), msg)
                        log(f"🕒 Grup sepi, kirim pesan pemancing ke {group.strip()}: {msg}")
                except Exception as e:
                    log(f"⚠️ Idle check error untuk {group.strip()}: {e}")
            await asyncio.sleep(IDLE_TIMEOUT)

    await asyncio.gather(client.run_until_disconnected(), idle_checker())


async def main():
    os.makedirs(SESSIONS_FOLDER, exist_ok=True)
    account_count = get_account_count()
    groups = get_target_groups()
    lang = get_language()
    reply_limit = get_reply_limit()

    tasks = [start_bot(i, API_ID, API_HASH, groups, lang, reply_limit) for i in range(account_count)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
