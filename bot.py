import ccxt
import requests
import pandas as pd
import pandas_ta as ta
import time

TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHANNEL_ID = "@PrimeVortexsignals"

# 50 Top Coins
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT', 'DOT/USDT', 'PEPE/USDT', 'DOGE/USDT', 'SHIB/USDT', 'NEAR/USDT', 'LINK/USDT']

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"})

def check_market(symbol, tf):
    try:
        ex = ccxt.kucoin()
        bars = ex.fetch_ohlcv(symbol, timeframe=tf, limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['RSI'] = ta.rsi(df['c'], length=14)
        rsi = df['RSI'].iloc[-1]
        price = df['c'].iloc[-1]

        if rsi < 38:
            msg = f"🚀 *SIGNAL ({tf}): {symbol}*\n📍 Entry: `{price}`\n📊 RSI: `{round(rsi, 2)}`"
            send_msg(msg)
    except: pass

if __name__ == "__main__":
    send_msg("🕵️ *Prime Vortex:* Scanning Market (15m/1h)...")
    for tf in ['15m', '1h']:
        for s in SYMBOLS:
            check_market(s, tf)
            time.sleep(0.5)
