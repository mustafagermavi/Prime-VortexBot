import ccxt
import requests
import pandas as pd
import pandas_ta as ta

# --- Configuration ---
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHAT_ID = "8142540785"

# --- List of 50 Global Symbols ---
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
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def get_master_signal(symbol):
    try:
        exchange = ccxt.kucoin()
        # Fetching Hourly data
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        
        # Calculating Indicators
        df['RSI'] = ta.rsi(df['close'], length=14)
        df['EMA_50'] = ta.ema(df['close'], length=50)
        
        last_rsi = df['RSI'].iloc[-1]
        current_price = df['close'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        
        # --- Logic: Buy only if Oversold AND in Upward Trend (EMA 50) ---
        if last_rsi < 35 and current_price > ema_50:
            entry = current_price
            msg = (
                f"🚀 *PRIME VORTEX: BUY {symbol}* 🚀\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📍 *ENTRY:* `{round(entry, 5)}`\n"
                f"📊 *RSI:* `{round(last_rsi, 2)}` (Oversold)\n"
                f"📈 *TREND:* `Bullish Confirmation`\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🎯 *TARGETS:*\n"
                f"✅ TP1: `{round(entry * 1.01, 5)}` (1%)\n"
                f"✅ TP2: `{round(entry * 1.025, 5)}` (2.5%)\n"
                f"🎯 TP3: `{round(entry * 1.04, 5)}` (4%)\n"
                f"🔥 TP4: `{round(entry * 1.07, 5)}` (7%)\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🚫 *STOP LOSS:* `{round(entry * 0.965, 5)}` (-3.5%)\n\n"
                f"✨ *Automated Global Analysis*"
            )
            send_telegram_msg(msg)

    except Exception as e:
        print(f"Skipping {symbol}: API or Data Error")

if __name__ == "__main__":
    print(f"🚀 Scanning {len(SYMBOLS)} global assets...")
    for s in SYMBOLS:
        get_master_signal(s)
    print("✅ Full Scan Complete.")
