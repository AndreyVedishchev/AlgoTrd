import requests

def make_request(endpoint, params=None):
    base_url = "https://fapi.binance.com"
    response = requests.get(base_url + endpoint, params=params)
    result = response.json()
    return result

# Найти в документации API Binance ендпоинт тикеров за 24 часа .
# Получить данные для списка из 10 фьючерсных пар на ваш произвольный выбор.
# Далее из полученной информации выберите пару, которая больше всего выросла и ту,
# которая больше всего упала за произвольный период.
if __name__ == '__main__':

    symbols = ['BTCUSDT','ETHUSDT','CAKEUSDT','SUIUSDT','COWUSDT','WIFUSDT','UMAUSDT','KAVAUSDT','SUNUSDT','TRBUSDT']
    endpoint_ticker_24 = "/fapi/v1/ticker/24hr"

    max_heigh = 0
    max_drop = 0
    dict_max_heigh = None
    dict_max_drop = None

    for smb in symbols:
        params = {
            'symbol': smb
        }
        ticker = make_request(endpoint_ticker_24, params)
        print("Ticker_24 >>", ticker)

        if float(ticker['priceChangePercent']) > max_heigh:
            max_heigh = float(ticker['priceChangePercent'])
            dict_max_heigh = {
                ticker['symbol']: max_heigh
            }

        if float(ticker['priceChangePercent']) < max_drop:
            max_drop = float(ticker['priceChangePercent'])
            dict_max_drop = {
                ticker['symbol']: max_drop
            }

    if dict_max_heigh is None:
        print("для роста нет данных для анализа")
    else:
        print("максимальный рост в процентах >>", dict_max_heigh)

    if dict_max_drop is None:
        print("для падения нет данных для анализа")
    else:
        print("максимальное падение в процентах >>", dict_max_drop)