import ffn
import pandas as pd
import numpy
import pandas_datareader.data as web

#input_date = '2010-01-01'

def get_data(user_dict):
    stock_list = list(user_dict.keys())
    weightings = list(user_dict.values())
    stock_data = web.DataReader(stock_list,start='1980-01-01')['Adj Close']
    cleaned_data = stock_data.dropna()
    
    check_max_length = max(data.isnull().sum())
    count = 0 
    list_of_bad_tickers = []
    bad_tickers = data.isnull().sum()
    for i in range(0, len(data.isnull().sum())):
        if bad_tickers.iloc[i] == max(data.isnull().sum()):
            count += 1
            list_of_bad_tickers.append(i)
    bad_tickers_return_list = []
    for i in list_of_bad_tickers:
        bad_tickers_return_list.append(bad_tickers.keys()[i])
    return cleaned_data, weightings, bad_tickers_return_list

def make_return_percentages(stock_table, weightings):
    table = stock_table
    custom_weightings = weightings 
    holdings = list(table.keys())
    # First argument '20' is going to need to be the period chosen by the user
    # 20 is an approximately monthly time frame. Mostly used for rebalance,
    # but also used to return monthly statements of portfolio value.
    rebalance_dates = table.iloc[::20, :]
    price_list = []
    for i in table.keys():#stocks_arr:
        # Each column in rebalance_dates is converted to a numpy array
        # for more efficient calculations
        price_list.append(rebalance_dates[i].to_numpy())
    performance_table = []
    return_list = []
    return_dict = {}
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
                    # return_dict just uses date_list as the keys and return_list as the values
                    #return_dict[rebalance_dates.index[j].strftime('%Y-%m-%d')] = res 
                except:
                    print('flag: ', flag)
                    print('try except clause. except clause activated, break from loop')
                    break
            flag += 1
        performance_table.append(return_list)
        return_list = []
    return weightings, performance_table, date_list, holdings #return_dict

class Investment_Portfolio:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.portfolio_value = 0

    # backtest just calculates 'buy and hold' returns
    def backtest(self, weightings, return_table, date_list, list_of_stocks):
        buy_and_hold_portfolio = weightings
        calc_table = return_table 
        statement = []
        performance_dict = {}
        for index in range(0,len(calc_table[0])):
            value = sum(buy_and_hold_portfolio)
            #statement.append(value)
            performance_dict[date_list[index]] = value
            for count in range(0, len(buy_and_hold_portfolio)):
                buy_and_hold_portfolio[count] = buy_and_hold_portfolio[count]*calc_table[count][index]

        for i in range(0,len(list_of_stocks)):
            self.portfolio[list_of_stocks[i]] = buy_and_hold_portfolio[i]
        self.portfolio_value = sum(self.portfolio.values())
        end_val = sum(buy_and_hold_portfolio)
        return performance_dict#, buy_and_hold_portfolio

""""""
# test region
user_dict = {}
user_dict['MSFT'] = 250
user_dict['AMZN'] = 250
user_dict['PBR'] = 250
user_dict['CLSK'] = 250
#user_dict['SHIT'] = 250
""""""
return_table = get_data(user_dict)#custom_df

# Error handling doesn't work here... consult Dan.
if len(return_table[2]) == 0:
    print('APSDIGUHAPOSDUGH')
    #print('ERROR MESSAGE: ', return_table[2], ' invalid stock tickers. They may be delisted')
else:
    percent_table = make_return_percentages(return_table[0], return_table[1])
    # Creating Portfolio Objects
    custom_portfolio = Investment_Portfolio(user_dict)
    buy_and_hold_custom = custom_portfolio.backtest(percent_table[0], percent_table[1], percent_table[2], percent_table[3])
    print(buy_and_hold_custom)
    #print(custom_portfolio.portfolio)
    #print(custom_portfolio.portfolio_value)
