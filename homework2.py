# Убедитесь, что библиотека websocket-client установлена: pip install websocket-client
import json
import traceback
import websocket
import threading

class Socket_conn_Binance(websocket.WebSocketApp):
    def __init__(self, url):
        super().__init__(
            url=url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.run_forever()

    def on_open(self, ws):
        print(ws, 'Websocket was opened')

    def on_error(self, ws, error):
        print('on_error', ws, error)
        print(traceback.format_exc())
        exit()

    def on_close(self, ws, status, msg):
        print('on_close', ws, status, msg)
        exit()

    def on_message(self, ws, msg):
        data = json.loads(msg)
        print(data)

# url = 'wss://stream.binance.com:443/ws/ethusdt@trade'
# threading.Thread(target=Socket_conn_Binance, args=(url,)).start()

symbol = "adausdt"
list_streams = [
    f"{symbol}@aggTrade",  # 1. Сделки
    f"{symbol}@kline_1m",  # 2. Свечи 1m
    f"{symbol}@depth20"    # 3. Стакан ордеров (20 уровней)
]
url = f'wss://fstream.binance.com/stream?streams={"/".join(str(e) for e in list_streams)}'
threading.Thread(target=Socket_conn_Binance, args=(url,)).start()

# Подписаться на поток **All Market Tickers Streams** и получить данные (для общего понимания всего рынка фьючерсов).
url = 'wss://fstream.binance.com/stream?streams=!ticker@arr'
threading.Thread(target=Socket_conn_Binance, args=(url,)).start()