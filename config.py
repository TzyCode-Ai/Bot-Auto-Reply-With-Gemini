# config.py

import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
GOOGLE_API_KEYS = [k.strip() for k in os.getenv("GOOGLE_API_KEYS", "").split(',') if k.strip()]

if not GOOGLE_API_KEYS:
    raise ValueError("❌ GOOGLE_API_KEYS tidak ditemukan di .env")
