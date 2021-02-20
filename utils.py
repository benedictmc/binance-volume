from binance_download import get_historic
from volume_ping_analysis import ohlc_analyis
import datetime


def round_ping(ping):
    columns = ["Net Vol BTC", "Recent Net Vol", "Recent Total Vol BTC"]
    for col in columns:
        ping[col] = round(float(ping[col]), 3)
    return ping

# end_time is time after ping in minutes
def get_ping_results(uid=None, ping=None, end_time=30):
    if not (uid or ping):
        return {}
    if uid: 
        ping = volume_collection.find({"_id" : uid}).limit(1)[0]

    coin = f"{ping['Coin']}BTC"
    start_time = int(datetime.datetime.timestamp(ping['Date']))*1000
    end_time = start_time+60*end_time*1000
    ohlc_data = get_historic(coin, '1m', start_time=start_time, end_time=end_time)
    analysis_data = ohlc_analyis(ohlc_data) 
    print(analysis_data)
    # analysis_data['coin'] = coin
    # analysis_data['date'] = ping['Datetime']
    # analysis_data['_id'] = uid  