#!/usr/bin/env python3
import schedule
from volume_download import fetch_pump_data
from binance_download import fetch_prices
import time

# Sets up schedule
schedule.every(30).seconds.do(fetch_pump_data)
schedule.every(10).seconds.do(fetch_prices)

# Loop to run schedule
while 1:
    schedule.run_pending()
    time.sleep(5)
