from typing import Dict
from datetime import datetime
from repositories.stock_data import Stock_Data
from services.back_tester_interface import BackTesterInterface

class Investment_Portfolio:
    def __init__(self, portfolio):
        self.portfolio = portfolio
    
    # currently rebalances on every data point. Need to pre-filter the data coming in for daily,monthly,quarterly,yearly periods
    def time_based_rebalance(weightings, roi_table, immutable_weightings): 
        rebalance_portfolio = weightings
        calc_table = roi_table
        rebalance_results = []
        statement = []
        for index in range(0,len(calc_table[0])): #<-- number of returns
            
            for count in range(0, len(rebalance_portfolio)):
                
                rebalance_portfolio[count] = rebalance_portfolio[count]*calc_table[count][index]
            value = sum(rebalance_portfolio)
            for count in range(0, len(rebalance_portfolio)):
    
                rebalance_portfolio[count] = value*(immutable_weightings[count]/sum(immutable_weightings))
                
            statement.append(value)
        end_val = sum(rebalance_portfolio)
        return end_val, rebalance_portfolio, statement
    

class TimeBasedRebalance(BackTesterInterface):
    def backtest(self, stocks: Dict[str, float], initial_value: float, start_date: datetime, end_date: datetime) -> Dict[datetime, float]:
        stock_tickers = list(stocks)
        stock_price_history = Stock_Data.get_stock_data(stock_tickers, start_date, end_date)

        return_percentages = self.__make_return_percentages(stock_price_history) #Each of these tables need to have another list for dates, or need to be dicts
        percent_table = return_percentages[0]
        date_keys = return_percentages[1][1:-1]

        custom_portfolio_weightings = []
        for weight in stocks:
            custom_portfolio_weightings.append(initial_value * stocks[weight])

        # Creating Portfolio Objects
        custom_portfolio = Investment_Portfolio(stock_tickers)
        time_based_rebal_custom = custom_portfolio.time_based_rebalance(custom_portfolio_weightings, percent_table)

        return_dict = { }
        if (len(date_keys) > 0):
            return_dict = {date_keys[i].to_pydatetime(): buy_and_hold_custom[2][i] for i in range(len(date_keys))}
        
        return return_dict    
   

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
