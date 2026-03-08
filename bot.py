import ccxt
import requests
import pandas as pd
import pandas_ta as ta
import time

# --- Settings ---
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHANNEL_ID = "@PrimeVortexsignals"

SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT', 'DOT/USDT',
    'LINK/USDT', 'MATIC/USDT', 'LTC/USDT', 'NEAR/USDT', 'ATOM/USDT', 'UNI/USDT', 'ALGO/USDT', 'ICP/USDT',
    'BCH/USDT', 'FIL/USDT', 'VET/USDT', 'HBAR/USDT', 'GRT/USDT', 'AAVE/USDT', 'EGLD/USDT', 'QNT/USDT',
    'FTM/USDT', 'THETA/USDT', 'SAND/USDT', 'MANA/USDT', 'AXS/USDT', 'CHZ/USDT', 'RNDR/USDT', 'INJ/USDT',
    'OP/USDT', 'ARB/USDT', 'TIA/USDT', 'SUI/USDT', 'SEI/USDT', 'IMX/USDT', 'KAS/USDT', 'STX/USDT',
    'ORDI/USDT', 'FET/USDT', 'AGIX/USDT', 'LDO/USDT', 'PEPE/USDT', 'SHIB/USDT', 'DOGE/USDT', 'BONK/USDT', 
    'WIF/USDT', 'JUP/USDT'
]

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": message, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except: pass

def get_signals(symbol, tf):
    try:
        ex = ccxt.kucoin()
        bars = ex.fetch_ohlcv(symbol, timeframe=tf, limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['RSI'] = ta.rsi(df['c'], length=14)
        df['EMA'] = ta.ema(df['c'], length=50)
        
        rsi, price, ema = df['RSI'].iloc[-1], df['c'].iloc[-1], df['EMA'].iloc[-1]

        if rsi < 38: # Buy Condition
            tp1, tp2, sl = price * 1.01, price * 1.025, price * 0.965
            msg = (
                f"🌟 *SIGNAL: {symbol}* ({tf})\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📍 *ENTRY:* `{round(price, 5)}` | RSI: `{round(rsi, 2)}`\n"
                f"📈 *TREND:* {'🔥 BULLISH' if price > ema else '🔄 RECOVERY'}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🎯 TP1: `{round(tp1, 5)}` | TP2: `{round(tp2, 5)}` \n"
                f"🚫 STOP LOSS: `{round(sl, 5)}` (-3.5%)\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📢 Channel: @PrimeVortexsignals"
            )
            send_telegram_msg(msg)
            return True
    except: return False

if __name__ == "__main__":
    send_telegram_msg("🕵️ *Prime Vortex Scan:* Checking 50 assets (15m/1h)...")
    found = 0
    for tf in ['15m', '1h']:
        for s in SYMBOLS:
            if get_signals(s, tf): found += 1
            time.sleep(0.1)
    if found == 0: send_telegram_msg("😴 No clear entries found right now.")
