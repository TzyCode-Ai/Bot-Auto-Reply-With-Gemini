# 🤖 Telegram Auto-Reply Bot with Gemini AI

This is a fully-featured Telegram bot that can automatically reply to messages in group chats using Gemini AI. It's built using Telethon and supports multiple accounts, multilingual fallback responses, idle message prompts, and anti-spam controls.

## ✨ Features

- ✅ Multi-account support (via session files)
- ✅ Multi-group support per account
- ✅ Auto-reply with Gemini AI or local fallback
- ✅ Language options: English / Indonesian
- ✅ Idle group detection with prompt messages
- ✅ Anti-spam: limit replies per user per minute
- ✅ Max reply limit per group until new user chats
- ✅ Easy session reuse (skips login if `.session` file exists)

## 📁 Folder Structure

.
├── main.py
├── reply.py
├── utils.py
├── config.py
├── sessions/ # Session files will be stored here
├── pesan/daftar-pesan-list/ # (optional) Message templates
├── balasan/ # fallback-en.txt / fallback-id.txt
├── .env # For storing API keys
├── .gitignore
└── README.md

## 🚀 Getting Started

### 1. Clone this repo

git clone https://github.com/your-username/telegram-auto-reply-bot.git
cd telegram-auto-reply-bot
2. Install dependencies
pip install -r requirements.txt
If you encounter issues with aiohttp, try:

pip install aiohttp --upgrade
3. Setup environment
Create a .env file:

API_ID=your_api_id
API_HASH=your_api_hash
GOOGLE_API_KEYS=key1,key2,key3
You can get your API_ID and API_HASH from https://my.telegram.org.

Note: If you're not using Gemini AI, fallback responses will be used.

4. Prepare fallback files
Place your fallback responses in:

balasan/fallback-en.txt
balasan/fallback-id.txt
One message per line.

5. Run the bot
python main.py
You will be prompted for:

Number of Telegram accounts

List of groups to monitor

Language (id / en)

Max replies per group before pausing

📌 Example Usage
If no messages are sent in a group for a while, the bot sends a random idle message like "Hi guys" or "Halo semuanya".

If a user sends a message, the bot replies intelligently (via Gemini or fallback).

Replies are rate-limited per user and per group to avoid spam.

📄 License
MIT License. Feel free to modify and contribute!

✉️ Contact
Built with ❤️ by AimTzy - Donate me : 0x0E6557CbA04Bc8213b1FB03b40E5dE851A7CE137(eth)