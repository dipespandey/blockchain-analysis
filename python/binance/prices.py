import requests

market = 'ETHUSDT'
tick_interval = '1m'
start_time = None

url = 'https://api.binance.com/api/v3/klines?symbol='+market+'&interval='+tick_interval
data = requests.get(url).json()

print(data)