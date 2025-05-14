import hashlib
import hmac
import json
import time
import requests
from config import API_KEY, SECRET_KEY

# Получить текущую цену фьючерса AXSUSDT и выставить на нем лимитный ордер на покупку ниже текущей цены на 1%
# и лимитный ордер на продажу выше текущей цены на 1%. Сделать принт ID выставленных ордеров.

# Данная функция будет создавать сигнатуру из отправленных в нее params (в формате словаря)
def gen_signature(params):
    param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
    signature = hmac.new(bytes(SECRET_KEY, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
    return signature

def get_current_price(symbol):
    params = {
        "symbol": symbol
    }
    response = requests.get(url="https://fapi.binance.com/fapi/v1/premiumIndex", params=params).json()
    if response:
        print(response['markPrice'])
        return float(response['markPrice'])

def get_new_order(symbol, side):

    price = get_current_price(symbol) * 0.99 if side == "BUY" else get_current_price(symbol) * 1.01

    # 1 Базовая ссылка + ендпоинт:
    url = "https://fapi.binance.com/fapi/v1/order"

    # 2 Заголовки:
    header = {
        "X-MBX-APIKEY": API_KEY
    }

    # 3 Параметры:
    timestamp = int(time.time() * 1000)

    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": 2,
        "price": round(price, 3),
        "timestamp": timestamp,
    }

    # 4 Сигнатура:
    params['signature'] = gen_signature(params)
    print(params)

    # 5 Отправка запроса:
    new_order = requests.post(url=url, params=params, headers=header).json()
    if new_order and 'orderId' in new_order:
        return new_order['orderId']


buyId = get_new_order(symbol="AXSUSDT", side="BUY")
sellId = get_new_order(symbol="AXSUSDT", side="SELL")

print('orderId для ордера на покупку -> ', buyId)
print('orderId для ордера на продажу -> ', sellId)



