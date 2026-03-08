import ccxt
import requests
import pandas as pd
import pandas_ta as ta

# --- Configuration ---
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHAT_ID = "8142540785"

SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT', 'DOT/USDT',
    'LINK/USDT', 'MATIC/USDT', 'LTC/USDT', 'NEAR/USDT', 'ATOM/USDT', 'UNI/USDT', 'ALGO/USDT', 'ICP/USDT',
    'BCH/USDT', 'FIL/USDT', 'VET/USDT', 'HBAR/USDT', 'GRT/USDT', 'AAVE/USDT', 'EGLD/USDT', 'QNT/USDT',
    'FTM/USDT', 'THETA/USDT', 'SAND/USDT', 'MANA/USDT', 'AXS/USDT', 'CHZ/USDT', 'RNDR/USDT', 'INJ/USDT',
    'OP/USDT', 'ARB/USDT', 'TIA/USDT', 'SUI/USDT', 'SEI/USDT', 'IMX/USDT', 'KAS/USDT', 'STX/USDT',
    'ORDI/USDT', 'FET/USDT', 'AGIX/USDT', 'OCEAN/USDT', 'LDO/USDT', 'PEPE/USDT', 'SHIB/USDT', 'DOGE/USDT',
    'BONK/USDT', 'WIF/USDT'
]

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def get_fast_signal(symbol):
    try:
        exchange = ccxt.kucoin()
        # Switching to 15-minute candles
        bars = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        
        df['RSI'] = ta.rsi(df['close'], length=14)
        df['EMA_50'] = ta.ema(df['close'], length=50)
        
        last_rsi = df['RSI'].iloc[-1]
        current_price = df['close'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        
        # --- Logic: Better chance to find signals in 15m ---
        if last_rsi < 38:
            entry = current_price
            strength = "🔥 STRONG" if current_price > ema_50 else "⚠️ RECOVERY"
            
            msg = (
                f"⚡ *15M SIGNAL: {symbol}* ⚡\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📍 *ENTRY:* `{round(entry, 5)}`\n"
                f"📊 *RSI:* `{round(last_rsi, 2)}`\n"
                f"💪 *POWER:* `{strength}`\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🎯 TP1: `{round(entry * 1.008, 5)}` (Scalp)\n"
                f"🎯 TP2: `{round(entry * 1.015, 5)}` (Standard)\n"
                f"🎯 TP3: `{round(entry * 1.03, 5)}` (Swing)\n"
                f"🚫 SL: `{round(entry * 0.97, 5)}` (-3%)\n"
            )
            send_telegram_msg(msg)
            return True
    except:
        return False

if __name__ == "__main__":
    send_telegram_msg("🕵️ *Prime Vortex:* Running 15m Scalp Scan on 50 Assets...")
    
    count = 0
    for s in SYMBOLS:
        if get_fast_signal(s):
            count += 1
    
    if count == 0:
        send_telegram_msg("😴 *Market Update:* No clear entry points found in the last 15m.")
    else:
        send_telegram_msg(f"✅ *Scan Finished:* Found `{count}` signals.")
