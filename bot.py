import ccxt
import requests
import pandas as pd
import pandas_ta as ta
import time

# --- Config ---
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHANNEL_ID = "@PrimeVortexsignals"

SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT',
    'DOT/USDT', 'LINK/USDT', 'MATIC/USDT', 'PEPE/USDT', 'SHIB/USDT', 'DOGE/USDT'
]

def send_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def scan(symbol, tf):
    try:
        ex = ccxt.kucoin()
        bars = ex.fetch_ohlcv(symbol, timeframe=tf, limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['RSI'] = ta.rsi(df['c'], length=14)
        df['EMA'] = ta.ema(df['c'], length=50)
        
        rsi, price, ema = df['RSI'].iloc[-1], df['c'].iloc[-1], df['EMA'].iloc[-1]

        if rsi < 38:
            msg = (
                f"🌟 *SIGNAL: {symbol}* ({tf})\n"
                f"📍 ENTRY: `{round(price, 5)}` | RSI: `{round(rsi, 2)}`\n"
                f"🎯 TP1: `{round(price * 1.01, 5)}` | SL: `{round(price * 0.97, 5)}`"
            )
            send_msg(msg)
            return True
    except: return False

if __name__ == "__main__":
    send_msg("🕵️ *Prime Vortex:* Scanning 15m & 1h...")
    for tf in ['15m', '1h']:
        for s in SYMBOLS:
            scan(s, tf)
            time.sleep(0.1)
