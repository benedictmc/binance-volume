from pymongo import MongoClient
import datetime
from binance_download import *

password = "!pword1"
db_uri = f'mongodb://ben:{password}@35.242.129.237:27017/?authSource=admin&ssl=false'

client = MongoClient(db_uri)
db = client['binance-volume-download']
volume_collection = db['volume-pings']


def ohlc_analyis(ohlc_data):
    close_prices = []
    open_price = float(ohlc_data[0][1])
    for ohlc in ohlc_data:
        close_prices.append(ohlc[4])
    highest_price = float(max(close_prices))
    price_diff = (highest_price-open_price)/open_price
    return {
        "open-price": open_price,
        "highest-price": highest_price,
        "price-diff": price_diff
        }

    # print(f"Open is {open_price}")
    # print(f"The max is  {highest_price}")
    # print(f"Percent change is: {price_diff}%")


# start = datetime.datetime(2021, 2, 15)
# end = datetime.datetime(2021, 2, 16)

# for item in volume_collection.find({"Date" : {'$gte': start}}):
#     coin = f"{item['Coin']}BTC"
#     # Converts to milliseconds
#     start_time = int(datetime.datetime.timestamp(item['Date']))*1000
#     end_time = start_time+60*30*1000
#     ohlc_data = get_historic(coin, '1m', start_time=start_time, end_time=end_time)
#     ohlc_analyis(ohlc_data)    


