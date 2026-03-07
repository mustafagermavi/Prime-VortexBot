import ccxt
import requests

# زانیاریێن تە
TOKEN = "8652574111:AAEAtgw9G-n5489pe0CST83bImdNK3fPs_c"
CHAT_ID = "8142540785"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

def get_signal():
    # ل ڤێرە مە بۆرسە گوهۆڕی بۆ KuCoin دا کو کێشە نەمینیت
    exchange = ccxt.kucoin() 
    symbol = 'BTC/USDT'
    
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']
    
    msg = f"🚀 *سیگناڵا کریپتۆ یا ئۆتۆماتیکی*\n\n💎 دراڤ: `{symbol}`\n💰 بها ل KuCoin: `${price}`\n\n✅ نوکە پڕۆژە ل سەر سێرڤەرێن جیهانی کار دکەت!"
    send_telegram_msg(msg)

if __name__ == "__main__":
    get_signal()
