import ccxt
import requests
import pandas as pd
import pandas_ta as ta

# --- Config ---
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

def get_master_signal(symbol):
    try:
        exchange = ccxt.kucoin()
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        
        df['RSI'] = ta.rsi(df['close'], length=14)
        df['EMA_50'] = ta.ema(df['close'], length=50)
        
        last_rsi = df['RSI'].iloc[-1]
        current_price = df['close'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        
        # --- NEW LOGIC: Trigger if RSI < 40 (More signals) ---
        if last_rsi < 40:
            entry = current_price
            msg = (
                f"🚀 *PRIME VORTEX: BUY {symbol}* 🚀\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📍 *ENTRY:* `{round(entry, 5)}`\n"
                f"📊 *RSI:* `{round(last_rsi, 2)}` (Potential Dip)\n"
                f"📈 *TREND:* {'Bullish' if current_price > ema_50 else 'Recovery Mode'}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"✅ TP1: `{round(entry * 1.01, 5)}` (1%)\n"
                f"✅ TP2: `{round(entry * 1.025, 5)}` (2.5%)\n"
                f"🚫 SL: `{round(entry * 0.96, 5)}` (-4%)\n"
            )
            send_telegram_msg(msg)
            return True # Signal found
    except:
        return False

if __name__ == "__main__":
    # 1. Send "Bot is Active" message to be sure
    send_telegram_msg("🔍 *Scanner Started:* Checking 50 global assets...")
    
    signals_count = 0
    for s in SYMBOLS:
        if get_master_signal(s):
            signals_count += 1
    
    # 2. Final Report
    send_telegram_msg(f"✅ *Scan Complete:* Found `{signals_count}` potential signals.")
