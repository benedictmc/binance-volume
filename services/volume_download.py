#!/usr/bin/env python3
import requests
import pandas as pd
from datetime import date as d
import datetime
import os
import schedule
import time
import json
import logging
import subprocess
from pymongo import MongoClient
import hashlib
    import traceback


# Database Config
client = MongoClient('localhost', 27017)
db = client['binance-volume-download']

volume_collection = db['volume-pings']
pump_keys = ["Coin", "Pings", "Net Vol BTC", "Net Vol %", "Recent Total Vol BTC", "Recent Vol %", "Recent Net Vol", "Datetime", "id"]

def generate_hash_id(r_id, datetime, coin):
    pump_id = f"{r_id}_{datetime}_{coin}" 
    hash_id = hashlib.sha1(pump_id.encode('utf-8')).hexdigest()
    return hash_id
    
def fetch_pump_data():
    print("Fetching pump data....")
    try:
        url = "https://agile-cliffs-23967.herokuapp.com/ok"
        r = requests.get(url).json()
    except Exception as e:
        logging.warning(f"***** ERROR OCCURED : {e}")
        return
    if len(r['resu']) == 1:
        # logging.info("No new data")
        return

    pump_id = r['resu'][-1]
    time_stamp = int(time.time())
    db_record_list = []

    for pump in r['resu'][:-1]:
        # Check if already added to db
        pump_data = { pump_keys[idx] : val for idx, val in enumerate(pump.split('|')+[pump_id]) }
        hash_id = generate_hash_id(pump_data['id'], pump_data['Datetime'], pump_data['Coin'] )

        if volume_collection.count_documents({ "_id": hash_id}) == 0:
            pump_data['_id'] = hash_id
            pump_data['Date'] = datetime.datetime.strptime(pump_data['Datetime'], '%H:%M:%S %m/%d/%y')
            pump_data['Timestamp'] = time_stamp
            db_record_list.append(pump_data)
        else:
            # No new data
            return

    volume_collection.insert_many(db_record_list)


