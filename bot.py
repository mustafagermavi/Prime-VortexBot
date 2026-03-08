import ccxt
import requests
import pandas as pd
import pandas_ta as ta
import time

# --- Config ---
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHANNEL_ID = "@PrimeVortexsignals"

SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT', 'PEPE/USDT', 'DOGE/USDT']

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})
    except: pass

def run_bot():
    ex = ccxt.kucoin()
    send_msg("🤖 *Prime Vortex:* Bot is now LIVE on Render and scanning...")
    
    while True: # ئەوەی وادەکات ئۆتۆماتیکی بێت ئەمەیە
        print("Scanning market...")
        for s in SYMBOLS:
            try:
                bars = ex.fetch_ohlcv(s, timeframe='15m', limit=100)
                df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
                df['RSI'] = ta.rsi(df['c'], length=14)
                rsi = df['RSI'].iloc[-1]
                price = df['c'].iloc[-1]

                if rsi < 38:
                    msg = f"🚀 *SIGNAL: {s}*\n📍 Price: `{price}`\n📊 RSI: `{round(rsi, 2)}`"
                    send_msg(msg)
                time.sleep(1) # بۆ ئەوەی سێرڤەرەکەمان باند نەکرێت
            except: pass
        
        print("Scan finished. Waiting 15 minutes...")
        time.sleep(900) # ٩٠٠ چرکە واتا ١٥ خولەک چاوەڕێ دەکات و دووبارە دەستپێدەکاتەوە

if __name__ == "__main__":
    run_bot()
