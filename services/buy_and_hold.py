from typing import Dict
from datetime import datetime, timedelta
from services.back_tester_interface import BackTesterInterface
import ffn
import numpy
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
yf.pdr_override()

class Investment_Portfolio:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    # backtest just calculates 'buy and hold' returns
    def buy_and_hold(self, weightings, roi_table):
        buy_and_hold_portfolio = weightings
        calc_table = roi_table
        statement = []
        for index in range(0,len(calc_table[0])):
            value = sum(buy_and_hold_portfolio)
            statement.append(value)
            for count in range(0, len(buy_and_hold_portfolio)):
                buy_and_hold_portfolio[count] = buy_and_hold_portfolio[count]*calc_table[count][index]

        end_val = sum(buy_and_hold_portfolio)
        return end_val, buy_and_hold_portfolio, statement

class BuyAndHold(BackTesterInterface):
    def backtest(self, stocks: Dict[str, float], initial_value: float, start_date: datetime, end_date: datetime) -> Dict[datetime, float]:

        print('stocks: ', stocks)
        frontend_arr = list(stocks)

        user_data = web.DataReader(frontend_arr, start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'))['Adj Close']
        print ('user_data: ', user_data)
        cleaned_data = user_data.dropna()
        print('cleaned_data: ', cleaned_data)
        return_table = cleaned_data 
        print('return_table: ', return_table)

        #period = 21 #roughly a monthly rebalance schedule... This is something that won't come into
                    #play with a buy and hold initial iteration of the program.
        return_percentages = self.__make_return_percentages(return_table) #Each of these tables need to have another list for dates, or need to be dicts
        percent_table = return_percentages[0]
        date_keys = return_percentages[1][1:-1]

        custom_portfolio_weightings = []
        for weight in stocks:
            custom_portfolio_weightings.append(initial_value * stocks[weight])

        # Creating Portfolio Objects
        custom_portfolio = Investment_Portfolio(frontend_arr)
        buy_and_hold_custom = custom_portfolio.buy_and_hold(custom_portfolio_weightings, percent_table)
        return_dict = { }
        if (len(date_keys) > 0):
            return_dict = {date_keys[i].to_pydatetime(): buy_and_hold_custom[2][i] for i in range(len(date_keys))}
        
        ret_val = {
            'snapshots': return_dict
            }

        return ret_val

    def __make_return_percentages(self, stock_table,rebal_period=21):
        table = stock_table
        print('table keys: ', table.keys()) 
        # First argument '21' is going to need to be the period chosen by the user
        # 21 is an approximately monthly time frame. Mostly used for rebalance,
        # but also used to return monthly statements of portfolio value.
        rebalance_dates = table.iloc[::rebal_period, :]
        date_keys = rebalance_dates.index
        print('rebalance_dates (inside func): ', rebalance_dates, 'len: ', len(rebalance_dates), 'len(date_keys): ', len(date_keys))
        price_list = []
        for i in stock_table.keys():#stocks_arr:
            print('i: ', i, 'type: ', type(i))
            # Each column in rebalance_dates is converted to a numpy array
            # for more efficient calculations
            price_list.append(rebalance_dates[i].to_numpy())
        performance_table = []
        return_list = []
        for i in price_list:
            flag = 0
            date_list = []
            for j in range(len(i)-1):
                if j == 0:
                    pass
                else:
                    try:
                        res = i[j+1]/i[j]
                        return_list.append(res)
                        date_list.append(rebalance_dates.index[j].strftime('%Y-%m-%d')) #%X'))
                    except:
                        print('flag: ', flag)
                        print('try except clause. except clause activated, break from loop')
                        break
                flag += 1
            print('len(return_list): ', len(return_list))
            performance_table.append(return_list)
            return_list = []
            print('len(date_list): ', len(date_list))

        return performance_table, date_keys