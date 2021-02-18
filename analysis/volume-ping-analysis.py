from pymongo import MongoClient
import datetime
from binance_download import *

password = "!pword1"
db_uri = f'mongodb://ben:{password}@35.242.129.237:27017/?authSource=admin&ssl=false'

client = MongoClient(db_uri)
db = client['binance-volume-download']
volume_collection = db['volume-pings']


start = datetime.datetime(2021, 2, 15)
end = datetime.datetime(2021, 2, 16)

for item in volume_collection.find({"Date" : {'$gte': start}}).limit(1):
    print(item)
    # get_historic()
    print(int(datetime.datetime.timestamp(item['Date'])))
