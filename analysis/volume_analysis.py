import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
import datetime
from db import db

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

