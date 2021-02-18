import requests
from pymongo import MongoClient
import time
import schedule

# Database Config
# Database Config
password = "!pword1"
db_uri = f'mongodb://ben:{password}@35.242.129.237:27017/?authSource=admin&ssl=false'

DB_CLIENT = MongoClient(db_uri)
DB = DB_CLIENT['price-database']

BASE_URL = "https://api.binance.com/api/v3"

def get_prices():
    endpoint = "/ticker/price"
    response = requests.get(f"{BASE_URL}{endpoint}")
    if response.status_code == 200:
        res_json = response.json()
        for coin in res_json:
            coin_entry = {
                'price': coin['price'],
                'timestamp': int(time.time()) 
            }
            collection = DB[coin['symbol']]
            collection.insert_one(coin_entry)
            


def get_historic(coin, interval, start_time=-1, end_time=-1):
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

# schedule.every(10).seconds.do(get_prices)

# while 1:
#     schedule.run_pending()
#     time.sleep(5)


# coin = "CHRBTC"
# interval = "1m"
# start = 1613459480
# start = start*1000

# thirty_minutes = 30*60
# end = start + thirty_minutes



# get_historic(coin, interval, start_time=start)