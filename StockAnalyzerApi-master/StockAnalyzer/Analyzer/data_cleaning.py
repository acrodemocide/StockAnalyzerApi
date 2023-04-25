# data cleaning and api request module
import yfinance as yf
#import pandas as pd
#import numpy as np
#import time

#import builtins
#import contextlib, io
#from unittest.mock import Mock

#start_time = time.time()

#from concurrent.futures import ProcessPoolExecutor
def extract(stock_symbol):
    data_arr = []
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="max")#, interval="1wk") # updated interval
    close = data["Close"]
    data_arr.append(close)
    return data_arr


#def clean_and_combine(table_of_prices, all_tickers_list):
def make_stocks_uniform(list_of_stock_objects, rebal_period):
    length_arr = []
    #trimmed_data = []

    for i in list_of_stock_objects:
        print('len(i.performance_history): ', len(i.performance_history))
        print('type(i.performance_history): ', type(i.performance_history))
        length_arr.append(len(i.performance_history))
    length_arr.sort()
    smallest_period = length_arr[0]

    for i in list_of_stock_objects:
        i.performance_history = i.performance_history[-smallest_period:]
        i.return_history = i.return_history[-smallest_period:]

    for i in list_of_stock_objects:
        i.performance_history = i.performance_history[0::rebal_period]
        i.return_history = i.return_history[0::rebal_period]

    #return smallest_period <-- we don't need to return anything;
    # this function just modifies stock length

