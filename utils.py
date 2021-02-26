from API import binance_api
from analysis import volume_analysis
import datetime
from db import db
from itertools import groupby

db_volume = db['binance-volume-download']
volume_collection = db_volume['volume-pings']



def round_ping(ping):
    columns = ["Net Vol BTC", "Recent Net Vol", "Recent Total Vol BTC"]
    for col in columns:
        ping[col] = round(float(ping[col]), 3)
    return ping


# end_time is time after ping in minutes
def ping_information(uid=None, ping=None, time_delta=30):
    if not (uid or ping):
        return {}
    if uid: 
        ping = volume_collection.find({"_id" : uid}).limit(1)[0]
    # time_delta = 85
    ohlc_data = __smart_binance_dl(ping, time_delta)
    # analysis_data = ohlc_analyis(ohlc_data) 
    # print(analysis_data)
    return ohlc_data


def __smart_binance_dl(ping, time_delta):
    # Check is data is in database , 
    # >> if all: then do analysis
    # >> if not all: dl what needs to be downlaoded AND then do analysis
    start_time = int(datetime.datetime.timestamp(ping['Date']))*1000
    end_time = start_time+60*time_delta*1000
    coin = f"{ping['Coin']}BTC"
    ohlc_collection = db['coins_ohlc'][coin]
    data = ohlc_collection.find({"timestamp" : {'$gte': start_time, '$lte': end_time}})
    amount_in_db = data.count()
    
    if data.count() == time_delta:
        print("Retriving from db")
        # All data is in db; retriving 
        return list(data)
    else:
        one_minute = 60*1000
        round_start_time = start_time + (one_minute - (start_time % one_minute))

        ids = [i for i in range(round_start_time, end_time, one_minute)]

        not_in = ohlc_collection.find({"_id" : { '$in': ids }}, {"_id":1})
        ids_in_db = [d['_id'] for d in list(not_in)]
        ids_not_in_db =  list(set(ids) - set(ids_in_db))
        ids_not_in_db.sort()
        
        dl_ids = []
        x = [j-i for i, j in zip(ids_not_in_db[:-1], ids_not_in_db[1:])]

        if all_equal(x):
            start_time = ids_not_in_db[0]
            end_time = ids_not_in_db[-1]
            ohlc_list = list(data)
            new_ohlc = __download_and_add(coin, start_time, end_time)
            ohlc_list.extend(new_ohlc)
        else:
            # Need to figure out this part.
            # This would be when there are different sections of time that need to be downloaded.
            # More then likely wont happen. 
            # I could also just put ids that not present in db
            # I would be dling more then I need there though
            pass
        return ohlc_list


def __download_and_add(coin, start_time, end_time):
    # Downloading all data and putting it in the db 
    binance_api.get_historic(coin, '1m', start_time=start_time, end_time=end_time)
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    ohlc_data = binance_api.get_historic(coin, '1m', start_time=start_time, end_time=end_time)
    ohlc_collection = db['coins_ohlc'][coin]
    ohlc_list = []
    for ohlc in ohlc_data:
        entry = {}
        for i, col in enumerate(columns):
            entry[col] = ohlc[i]
            entry['_id'] = ohlc[0]
        ohlc_list.append(entry)
    ohlc_collection.insert_many(ohlc_list, ordered=False)
    return ohlc_list



def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def clean_ohlc(ohlc_data):
    for row in ohlc_data:
        del row['_id']
        row['time'] = row['timestamp']
        del row['timestamp']        


def split_data_schema(ohlc_data):
    schema, data = [], []
    if len(ohlc_data) > 0:
        key_list = ohlc_data[0].keys()
        for i, key in enumerate(key_list):
            if key == 'time':
                schema.insert(0, {
                    "column": "Date",
                    "format" :"%Y-%m-%d %H:%M:%S",
                    "index": 0,
                    "name": "Date",
                    "type": "date"
                })
                continue

            schema.append({
                "column": key.capitalize(),
                "index": i+1,
                "name": key.capitalize(),
                "type": "number"
            })

    cols = ['time', 'open', 'high', 'low' , 'close']
    for ohlc in ohlc_data:
        row = []
        for col in cols: 
            if col == 'time':
                ts = datetime.datetime.fromtimestamp(ohlc[col] / 1e3)
                dt = ts.strftime("%Y-%m-%d %H:%M:%S")
                row.append(dt)
                continue
            row.append(ohlc[col])   
        data.append(row)

    return schema, data


