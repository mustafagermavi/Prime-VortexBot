import ccxt
import requests
import pandas as pd
import pandas_ta as ta

# زانیاریێن تە
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHAT_ID = "8142540785"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def get_crypto_signal():
    exchange = ccxt.kucoin()
    symbol = 'BTC/USDT'
    
    # وەرگرتنا داتایێن بهایێ (Candlestick data)
    bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
    df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
    
    # حسابکرنا RSI
    df['RSI'] = ta.rsi(df['close'], length=14)
    last_rsi = df['RSI'].iloc[-1]
    current_price = df['close'].iloc[-1]
    
    # مەرجێن سیگناڵێ
    if last_rsi < 35:
        msg = f"🟢 *سیگناڵا کڕینێ (BUY)*\n\n💎 دراڤ: {symbol}\n💰 بها: ${current_price}\n📈 ئاستێ RSI: {round(last_rsi, 2)}\n\n⚠️ تێبینی: بها یێ زۆر دابەزیی و دەلیڤەکا باشە!"
        send_telegram_msg(msg)
    
    elif last_rsi > 65:
        msg = f"🔴 *سیگناڵا فرۆتنێ (SELL)*\n\n💎 دراڤ: {symbol}\n💰 بها: ${current_price}\n📉 ئاستێ RSI: {round(last_rsi, 2)}\n\n⚠️ تێبینی: بها یێ زۆر بلند بوویی، ئاگەهدار بە!"
    
    else:
        # ئەگەر چ سیگناڵ نەبوو، تەنێ داتایێ سادە بفرێشە دا بزانی بوت یێ کار دکەت
        msg = f"⌛ *بازار یێ سەقامگیرە*\n\n💎 دراڤ: {symbol}\n💰 بها: ${current_price}\n📊 ئاستێ RSI: {round(last_rsi, 2)}\n✅ چ سیگناڵ نینن نوکە."
        send_telegram_msg(msg)

if __name__ == "__main__":
    get_crypto_signal()
