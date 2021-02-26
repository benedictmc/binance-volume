import time
import hmac
import json
import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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
        if res_data['success']:
            for market in res_data['result']:
                if 'PERP' in market['name']:
                    print(market['name'])


    def get_market_ohlc(self, start_time, end_time):
        one_min = 60
        # start_time = 1613773559
        # end_time = 1614378383
        name = "COMP-PERP"
        endpoint = f'/markets/{name}/candles?resolution={one_min}&start_time={start_time}&end_time={end_time}'
        url = f'{self.BASE_URL}{endpoint}'
        print(url)
        res = requests.get(url, headers=self.create_headers(url))
        res_data = res.json()
        print("Starting")
        volume, mins = [], []
        if res_data['success']:
            for i, ohlc in enumerate(res_data['result']):
                mins.append(i)
                volume.append(ohlc['volume'])
        return volume, mins


    def plot_volume(self, volum, mins):

        fig, ax = plt.subplots()
        t = np.arange(0.0, 2.0, 0.01)
        ax.plot(mins, volume)

        ax.set(xlabel='mins after 00:00', ylabel='Volume',
            title='Simple Volume Charts')
        ax.grid()
        plt.show()


day = 86400

ftx = FTX_API()

for i in range(7):
    added = day * i
    start_time = 1613692800 + added
    end_time = start_time + 1800
    volume, mins = ftx.get_market_ohlc(start_time, end_time)
    ftx.plot_volume(volume, mins)
