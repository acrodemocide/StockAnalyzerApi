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
    """trimmed_data = []
    for i in table_of_prices:
        series = i[0]
        trim = series.tail(smallest_period) 
        trimmed_data.append(trim)

    # for some reason, last row is all 'nan' and first row is all 'nan'
    # this 'nan' issue only shows up randomly. For example, if rebalance
    # period is 19 days, then 'nan' appears. However there is no problem
    # with 18 or 20 days. 3 days, 100 days, 90 days, 252 days all worked
    # fine as well.
    #trimmed_data is a dataframe series that needs the last element removed for being 'nan'
    ##################################################################
    #print(trimmed_data)
    #items = ['Table ', 'Chair ', 'Mirror ', 'Curtain ', 'Almirah ']
    #items = trimmed_data
    #file = open('items.txt','w')
    #file.writelines(items.to_string())
    #file.close()
    ##################################################################
    #portfolio_dataframe = pd.concat(trimmed_data, axis=1, keys=all_tickers_list)#keys=user_input_arr)
    #portfolio_dataframe.drop(portfolio_dataframe.tail(5).index,inplace=True)
    return portfolio_dataframe"""

#def make_return_percentages(rebalance_period, stocks_arr, stock_table):
#    table = stock_table
#    rebalance_dates = table.iloc[::rebalance_period, :]
#    return rebalance_dates
    """
    price_list = []
    for i in stocks_arr:
        price_list.append(rebalance_dates[i].to_numpy())

    performance_table = []
    return_list = []
    for i in price_list:
        flag = 0
        for j in range(len(i)-1):
            if j == 0:
                pass
            else:
                try:
                    res = i[j+1]/i[j]
                    return_list.append(res)
                except:
                    print('flag: ', flag)
                    print('try except clause. except clause activate, break from loop')
                    break
            flag += 1
        performance_table.append(return_list)
        return_list = []
    return performance_table
    """
