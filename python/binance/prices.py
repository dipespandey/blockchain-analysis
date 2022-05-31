import requests
import datetime

market = 'ETHUSDT'
tick_interval = '1m'
start_time = None

# [
#   [
#     1499040000000,      // Open time
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "17928899.62484339" // Ignore
#   ]
# ]

url = f'https://api.binance.com/api/v3/klines?symbol={market}&interval={tick_interval}&startTime=1621555200000'
url1 = f'https://api.binance.com/api/v3/klines?symbol={market}&interval={tick_interval}&startTime=1621585200000'
url2 = f'https://api.binance.com/api/v3/klines?symbol={market}&interval={tick_interval}&startTime=1621615200000'
data = requests.get(url).json()

with open('prices.csv', 'a') as f:
  f.write('\n')
  for i in data:
    print(i[0])
    date = datetime.datetime.fromtimestamp(i[0]/1000)
    price = i[4]
    f.write(f'\n{str(price)},{date}')