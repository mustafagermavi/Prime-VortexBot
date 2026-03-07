import ccxt
import requests

# زانیاریێن بوتێ تلگرامی
TOKEN = "ل ڤێرە تالۆکێ خۆ یێ تلگرامی دانە"
CHAT_ID = "ل ڤێرە ئایدییا چاتێ خۆ دانە"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    requests.get(url)

# پشکنینا بازارێ
exchange = ccxt.binance()
symbol = 'BTC/USDT'
ticker = exchange.fetch_ticker(symbol)
price = ticker['last']

# سیگناڵەکێ سادە
message = f"📢 پشکنینا ئۆتۆماتیکی:\nبهایێ {symbol} نوکە {price}$ یە."
send_message(message)
