import datetime
import requests
from binance.client import Client


class BinancePricing():
    def __init__(self, coin_id):
        self.coin = coin_id
        self.client = Client()
            
    def get_price_after_timestamp(self, timestamp):
        bars = self.client.get_historical_klines(self.coin, '1d', timestamp, limit=1000)
        return [(datetime.datetime.fromtimestamp(i/1000), i[4]) for i in bars]
    
    def __str__(self):
        return f"Binance prices for {self.coin_id}"


class CPKPricing():
    def __init__(self, coin_id):
        self.coin = coin_id
        self.base_url = 'https://api.coinpaprika.com/v1'
    
    def get_price_at_timestmap(self, timestamp):
        response = requests.get(f"{self.base_url}/tickers/{self.coin}/historical?start={timestamp}")
        return [(i['timestamp'], i['price']) for i in response.json()]


