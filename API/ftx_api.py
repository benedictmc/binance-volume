import time
import hmac
import json
import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime


class FTX_API():

    def __init__(self):
        with open('keys.json', 'r') as f:
            keys = json.load(f)

        self.API_KEY = keys['FTX']['API']
        self.SECRET_KEY = keys['FTX']['SECRET']
        self.BASE_URL = "https://ftx.com/api"


    def create_headers(self, url):
        ts = int(time.time() * 1000)
        signature_payload = f'{ts}GET{url}'.encode()
        signature = hmac.new(self.SECRET_KEY.encode(), signature_payload, 'sha256').hexdigest()
        headers = {
            'FTX-KEY' : self.API_KEY,
            'FTX-SIGN' : signature,
            'FTX-TS' : str(ts)
        }
        return headers


    def get_markets(self):
        endpoint = '/markets'
        url = f'{self.BASE_URL}{endpoint}'
        res = requests.get(url, headers=self.create_headers(url))
        res_data = res.json()
        markets = []
        if res_data['success']:
            for market in res_data['result']:
                markets.append(market['name'])
                with open('market.json', 'w') as f:
                    json.dump(markets, f)


    def get_market_ohlc(self, name, start_time, end_time):
        one_min = 60
        
        endpoint = f'/markets/{name}/candles?resolution={one_min}&start_time={start_time}&end_time={end_time}'
        url = f'{self.BASE_URL}{endpoint}'
        print(url)
        res = requests.get(url, headers=self.create_headers(url))
        res_data = res.json()
        print("Starting")
        data, mins = [], []
        if res_data['success']:
            for i, ohlc in enumerate(res_data['result']):
                time_ = datetime.datetime.fromtimestamp(int(ohlc['time']) / 1e3)
                mins.append(time_)
                data.append(ohlc)
        return data, mins


    def plot_line(self, line, mins, chart_name):
        fig, ax = plt.subplots(constrained_layout=True, figsize=(10,5))
        locator = mdates.AutoDateLocator()
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        ax.plot(mins, line)
        ax.set(xlabel='Minutes', ylabel='Volume',
            title=chart_name)
        ax.grid()
        plt.show()



def buy_sell(data):
    short = 0
    max_pct = []
    for i in data:
        if '23:50:00' in i['startTime']:
            short =  i['open']
        if short != 0:
            high =  i['high']
            pct_chg = (short - high) / short
            pct_chg = round(float(pct_chg), 3)
            max_pct.append(pct_chg)
            print(f"Percent change after short open is {pct_chg}")
    print(f"The max percent change was {max(max_pct)}")

day = 86400


ftx = FTX_API()

# ftx.get_markets()


for i in range(7):
    added = day * i
    # Get Perp 00:00 - 00:30
    # name = "ETH-PERP"

    
    # start_time = 1613692800 + added
    # # Plus half hour
    # end_time = start_time + 1800
    # data, mins = ftx.get_market_ohlc(name, start_time, end_time)
    # volume_data = [item['volume'] for item in data]
    # chart_name = f'Volume for {name} between {mins[0].strftime("%d/%m/%Y, %H:%M")} - {mins[-1].strftime("%d/%m/%Y, %H:%M")}'
    # ftx.plot_line(volume_data, mins, chart_name)



    # Get ETH/BTC 23:30 - 00:30
    name = "ETH/USDT"

    # Minus half hour
    start_time = 1613692800 + added - 1800
    # Plus half hour
    end_time = start_time + 3600
    data, mins = ftx.get_market_ohlc(name, start_time, end_time)
    buy_sell(data)
    continue
    open_data = [item['open'] for item in data]
    chart_name = f'Open for {name} between {mins[0].strftime("%d/%m/%Y, %H:%M")} - {mins[-1].strftime("%d/%m/%Y, %H:%M")}'
    ftx.plot_line(open_data, mins, chart_name)



# for i in range(7):
#     added = day * i
#     # Minus half hour
#     start_time = 1613692800 + added - 1800
#     # Plus half hour
#     end_time = start_time + 3600
#     data, mins = ftx.get_market_ohlc(name, start_time, end_time)
#     open_data = [item['open'] for item in data]
#     ftx.plot_line(open_data, mins)



