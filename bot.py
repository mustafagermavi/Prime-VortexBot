import ccxt
import requests
import pandas as pd
import pandas_ta as ta
import time

# --- Config ---
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHANNEL_ID = "@PrimeVortexsignals"

# List of 50 assets
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT', 'DOT/USDT', 'LINK/USDT', 'MATIC/USDT', 'PEPE/USDT', 'DOGE/USDT', 'SHIB/USDT']

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def scan():
    ex = ccxt.kucoin()
    for s in SYMBOLS:
        try:
            bars = ex.fetch_ohlcv(s, timeframe='15m', limit=100)
            df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
            df['RSI'] = ta.rsi(df['c'], length=14)
            rsi = df['RSI'].iloc[-1]
            price = df['c'].iloc[-1]

            if rsi < 38:
                msg = f"🚀 *AUTOMATIC SIGNAL: {s}*\n📍 Price: `{price}`\n📊 RSI: `{round(rsi, 2)}`"
                send_msg(msg)
            time.sleep(0.2) # بۆ هندێ سێرڤەر نەیێ قەپاتکرن
        except: pass

if __name__ == "__main__":
    print("Auto Scan Started...")
    scan()
    print("Auto Scan Finished.")
