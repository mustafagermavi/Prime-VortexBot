import ccxt
import requests
import pandas as pd
import pandas_ta as ta
import time
import sys

# --- Settings ---
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHANNEL_ID = "@PrimeVortexsignals"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    print("Bot starting...")
    send_msg("🚀 *Prime Vortex System:* Online & Scanning...")
    
    # لێرەدا پشکنینەکان دەست پێ دەکەن (وەک ئەو کۆدانەی پێشتر)
    # من تەنها ئەم پەیامەم داناوە بۆ ئەوەی دڵنیا بین کە ئیرۆرەکە نەماوە
