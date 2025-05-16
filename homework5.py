import hashlib
import hmac
import time
import requests
import json
from config import BYBIT_API_KEY, BYBIT_SECRET_KEY

# Получить текущую цену фьючерса ADAUSDT и выставить на нем 2 лимитных ордера объемом X на покупку ниже текущей цены на
# 1 % и 2% соответственно, и 1 лимитный ордер на продажу выше текущей цены на 2% объемом 2X.

# Данная функция будет создавать сигнатуру из отправленных в нее params (в формате словаря)
def gen_signature(params, timestamp):
    param_str = timestamp + BYBIT_API_KEY + '5000' + json.dumps(params)
    signature = hmac.new(bytes(BYBIT_SECRET_KEY, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
    return signature

def get_current_price(symbol):
    params = {
        "symbol": symbol,
        "category": "linear"
    }
    response = requests.get(url="https://api.bybit.com/v5/market/tickers", params=params).json()
    # print(response)
    if response and 'result' in response:
        result = response['result']
        if result and 'list' in result:
            return float(result['list'][0]['markPrice'])

def get_new_order(symbol, side, percent, qty):

    price = str(get_current_price(symbol) * (1 + (percent / 100)))

    # 1 Базовая ссылка + ендпоинт:
    url = "https://api.bybit.com/v5/order/create"

    # 2 Заголовки:
    header = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-RECV-WINDOW": "5000",
        # "X-BAPI-TIMESTAMP": timestamp,
        # "X-BAPI-SIGN": signature,
    }

    # 3 Параметры:
    timestamp = str(int(time.time() * 1000))

    params = {
        "category": "linear",
        "symbol": symbol,
        "side": side,
        "orderType": "Limit",
        "qty": str(qty),		# В сравнении с Binance, Bybit ожидает строковые данные...
        "price": price,		# аналогично
    }

    # 4 Сигнатура + timestamp:
    header["X-BAPI-SIGN"] = gen_signature(params, timestamp)
    header["X-BAPI-TIMESTAMP"] = timestamp

    # 5 Отправка запроса:
    new_order = requests.post(url=url, headers=header, data=json.dumps(params)).json()
    print(new_order)


symbol = "ADAUSDT"
qty = 7  #минимальный объем эквивалент 5 USDT
# percent указывается от текущей цены
get_new_order(symbol=symbol, side="Buy", percent=-1, qty=qty)
get_new_order(symbol=symbol, side="Buy", percent=-2, qty=qty)
get_new_order(symbol=symbol, side="Sell", percent=2, qty=qty*2)
