import os
import pandas as pd
from pymongo import MongoClient
import hashlib
import json
import datetime 

# Database Config
password = "!pword1"
db_uri = f'mongodb://ben:{password}@35.242.129.237:27017/?authSource=admin&ssl=false'

client = MongoClient(db_uri)
db = client['binance-volume-download']
volume_collection = db['volume-pings']


def generate_hash_id(r_id, datetime, coin):
    pump_id = f"{r_id}_{datetime}_{coin}" 
    hash_id = hashlib.sha1(pump_id.encode('utf-8')).hexdigest()
    return hash_id
    

# CSV files
def add_csv_files():
    rel_path = 'data/coins/pump_data/'
    for filename in os.listdir(rel_path):
        filepath = f"{rel_path}{filename}"
        df = pd.read_csv(filepath, index_col=0)
        db_record_list = []
        for row in df.to_dict(orient='records'):
            hash_id = generate_hash_id(row['id'], row['Datetime'], row['Coin'])
            row['_id'] = hash_id
            row['Date'] = datetime.datetime.strptime(row['Datetime'], '%H:%M:%S %m/%d/%y')
            db_record_list.append(row)
        volume_collection.insert_many(db_record_list)

 

# JSON files
def add_json_files():
    rel_path = 'data/json'
    for filename in os.listdir(rel_path):
        db_record_list = []
        with open(f"{rel_path}/{filename}", 'r') as f:
            pump_save = json.load(f)
            
        for key, row in pump_save.items():
            hash_id = generate_hash_id(row['id'], row['Datetime'], row['Coin'])
            row['_id'] = hash_id
            row['leg_id'] = row['uid']
            row['Date'] = datetime.datetime.strptime(row['Datetime'], '%H:%M:%S %m/%d/%y')
            del row['uid']
            db_record_list.append(row)
        volume_collection.insert_many(db_record_list)


# add_csv_files()
add_json_files()