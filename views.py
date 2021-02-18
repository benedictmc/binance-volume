from flask import Flask, jsonify
from pymongo import MongoClient
import datetime
from binance_download import get_historic
from volume_ping_analysis import ohlc_analyis

app = Flask(__name__)

password = "!pword1"
db_uri = f'mongodb://ben:{password}@35.242.129.237:27017/?authSource=admin&ssl=false'
client = MongoClient(db_uri)
db_volume = client['binance-volume-download']
volume_collection = db_volume['volume-pings']


@app.route("/")
def hello():
    return "Hello Wordld!"


@app.route("/volume/pings")
def volume_pings():
    start = datetime.datetime(2021, 2, 15)
    ping_range = volume_collection.find({"Date" : {'$gte': start}})
    pings = []
    for ping in ping_range:
        ping['Date'] = ping['Date'].strftime("%m/%d/%Y, %H:%M:%S")
        pings.append(ping)
    
    return jsonify(pings)


@app.route("/volume/stats/<uid>")
def volume_stats(uid):
    ping = volume_collection.find({"_id" : uid}).limit(1)[0]

    coin = f"{ping['Coin']}BTC"
    start_time = int(datetime.datetime.timestamp(ping['Date']))*1000
    end_time = start_time+60*30*1000
    ohlc_data = get_historic(coin, '1m', start_time=start_time, end_time=end_time)
    analysis_data = ohlc_analyis(ohlc_data) 
    analysis_data['coin'] = coin
    analysis_data['date'] = ping['Datetime']
    analysis_data['_id'] = uid  
    return jsonify(analysis_data)





if __name__ == '__main__':
    app.debug = True
    app.run()