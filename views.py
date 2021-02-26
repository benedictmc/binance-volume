from flask import Flask, jsonify
from pymongo import MongoClient
import datetime
from utils import *
from db import db
import traceback

app = Flask(__name__)

db_volume = db['binance-volume-download']
volume_collection = db_volume['volume-pings']


@app.route("/")
def home():
    return "Status: up"


@app.route("/volume/pings")
def volume_pings():
    start = datetime.datetime(2020, 6, 15)
    end = datetime.datetime(2020, 6, 16)
    ping_range = volume_collection.find({"Date" : {'$gte': start, '$lte': end}})
    pings = []
    for ping in ping_range:
        ping = round_ping(ping)
        # get_ping_results(ping=ping)
        ping['Date'] = ping['Date'].strftime("%m/%d/%Y, %H:%M:%S")
        pings.append(ping)
    return jsonify(pings)


@app.route("/volume/stats/<uid>")
def volume_stats(uid):
    try:
        ohlc_data = ping_information(uid=uid)
        clean_ohlc(ohlc_data)
        print(ohlc_data[0])
        schema, data = split_data_schema(ohlc_data)
        return jsonify([data, schema])
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        return "Did not work"
    



if __name__ == '__main__':
    app.debug = True
    app.run()