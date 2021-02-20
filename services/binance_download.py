import requests
from pymongo import MongoClient
import time
import schedule

# Database Config
client = MongoClient('localhost', 27017)
db = client['price-database']

BASE_URL = "https://api.binance.com/api/v3"

def fetch_prices():
    print("Fetching binance prices....")
    endpoint = "/ticker/price"
    response = requests.get(f"{BASE_URL}{endpoint}")
    if response.status_code == 200:
        res_json = response.json()
        for coin in res_json:
            coin_entry = {
                'price': coin['price'],
                'timestamp': int(time.time()) 
            }
            collection = db[coin['symbol']]
            collection.insert_one(coin_entry)
            

# Will probably move endpoints for binance to a new file
def fetch_historic(coin, interval, start_time=-1, end_time=-1):
    endpoint = '/klines'    
    params = f'?symbol={coin}&interval={interval}'
    if start_time != -1:
        params = f'{params}&startTime={start_time}'
    if end_time != -1:
        params = f'{params}&endTime={end_time}'

    url = f'{BASE_URL}{endpoint}{params}'
    response = requests.get(url)
    if response.status_code == 200:
        close_prices = []
        res_json = response.json()
        return res_json