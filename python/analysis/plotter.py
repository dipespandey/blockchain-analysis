import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Define the nice number formatter
def number_formatter(number, pos=None):
    """Convert larger number into a human readable format."""
    magnitude = 0
    while abs(number) >= 1000:
        magnitude += 1
        number /= 1000.0
    return '%.1f%s' % (number, ['', 'K', 'M', 'B', 'T', 'Q'][magnitude])

def produce_graph():
  pancake_data = json.load(open('pancakeswap/stats.json'))['data']['pancakeDayDatas'][::-1]
  uni2_data = json.load(open('uniswap/stats.json'))['data']['uniswapDayDatas'][::-1]
  uni3_data = json.load(open('uniswap/v3stats.json'))['data']['uniswapDayDatas'][::-1]
  binance_data = pd.read_csv('binance/binance24htv.csv')
  dates = [datetime.datetime.fromtimestamp(i['date']) for i in pancake_data]

  pancakeDailyVolumeUSD = [float(i['dailyVolumeUSD']) for i in pancake_data]
  uniswapDailyVolumeUSD = [float(i['dailyVolumeUSD']) for i in uni2_data]
  uniswapV3DailyVolumeUSD = [float(i['volumeUSD']) for i in uni3_data]
  binanceDailyVolumeUSD = list(binance_data.volume)

  print(dates, list(binance_data.snapped_at))
  pancaketxns = [int(i['totalTransactions']) for i in pancake_data]
  uniswaptxns = [int(i['txCount']) for i in uni2_data]
  uniswapV3txns = [int(i['txCount']) for i in uni3_data]

  pancakeTotalLiquidityUSD = [float(i['totalLiquidityUSD']) for i in pancake_data]
  uniswapTotalLiquidityUSD = [float(i['totalLiquidityUSD']) for i in uni2_data]
  uniswapV3TotalLiquidityUSD = [float(i['tvlUSD']) for i in uni3_data]

  fig, ax = plt.subplots()
  plt.plot(dates, uniswapDailyVolumeUSD)
  plt.plot(dates, pancakeDailyVolumeUSD)
  plt.plot(dates, uniswapV3DailyVolumeUSD)
  plt.plot(dates, binanceDailyVolumeUSD)
  plt.xlabel('date')
  plt.ylabel('DailyVolumeUSD')
  plt.legend(["Uniswap V2", "PancakeSwap V2", "Uniswap V3", "Binance"])
  ax.yaxis.set_major_formatter(FuncFormatter(number_formatter))
  plt.show()

  fig, ax = plt.subplots()
  plt.plot(dates, uniswaptxns)
  plt.plot(dates, pancaketxns)
  plt.plot(dates, uniswapV3txns)
  plt.xlabel('date')
  plt.ylabel('Daily Transactions')
  plt.legend(["Uniswap V2", "PancakeSwap V2", "Uniswap V3"])
  ax.yaxis.set_major_formatter(FuncFormatter(number_formatter))
  plt.show()

  fig, ax = plt.subplots()
  plt.plot(dates, uniswapTotalLiquidityUSD)
  plt.plot(dates, pancakeTotalLiquidityUSD)
  plt.plot(dates, uniswapV3TotalLiquidityUSD)
  plt.xlabel('date')
  plt.ylabel('DailyLiquidityUSD')
  plt.legend(["Uniswap V2", "PancakeSwap V2", "Uniswap V3"])
  ax.yaxis.set_major_formatter(FuncFormatter(number_formatter))
  plt.show()


produce_graph()