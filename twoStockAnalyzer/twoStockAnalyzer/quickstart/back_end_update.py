# back end update

import statistics
import numpy as np
import pandas as pd

class Stock: # 5 attributes: name, performance_history, end_val, return_history, volatility, variance/beta
    def __init__(self, name, performance_history):
        self.name = name
        self.performance_history = performance_history # historic stock prices
        #print('test print performance_history: ', len(self.performance_history))
        #print('^^^^^^^^^^^^^^^^^^ what??? ^^^^^^^^^^^^^^^^^')
        self.end_val = performance_history[-1]

        """3 more stock attributes are calculated from performance_history: 
        return history(percent returns), volatility, and variance/beta"""
        temp_list = []
        flag = 0
        #print('POOP POOP POOP POOP POOP POOP POOP POOP POOP POOP POOP')
        #print('performance_history lenth: ', len(performance_history))
        #print('self.performance_history length: ', len(self.performance_history))
        for j in range(0, len(performance_history)-1): 
            #print('j: ', j)
            try:
                res = performance_history[(j+1)]/performance_history[j]
                #print('test print res: ', res)
                #print('ASDUGHPUOASDHGPOUHASPDOUGHAP!)@#%^@)#(&%^)#@(&%^)(@&#%#%)')
            except: 
                print('flag: ', flag)
                print('try except clause. except clause activated, break from loop')
                break
            flag += 1
            temp_list.append(res)
        #print('test print temp_list: ', temp_list)

        self.return_history = temp_list # percent returns calculated between price periods
        #print('test print return_history: ', self.return_history)
        self.volatility = statistics.pstdev(self.return_history) 
        self.variance = statistics.variance(self.return_history) # variance/beta


class Portfolio:
    def __init__(self, name, list_of_stocks, bh_weightings, tact_rebal_weightings):#, immutable_weightings):# limiting_size_factor):
        self.name = name
        self.list_of_stocks = list_of_stocks
        self.bh_weightings = bh_weightings
        self.tact_rebal_weightings = tact_rebal_weightings
        self.immutable_weightings = tact_rebal_weightings[:] #therefore, do not need to pass in 'immutable_weightings'

        self.size = len(list_of_stocks) # number of holdings
        """ avg_volatility, determinant, avg beta, num_holdings, normalized_r_squared,
        avg_price_differential are all derived from the list of stock objects """

        # Gather all portfolio analytics in single loop
        key_names = []
        returns_table = []
        volatility_list = []
        variance_list = []
        stock_ending_vals = []
        for i in list_of_stocks:
            key_names.append(i.name)
            returns_table.append(i.return_history)
            volatility_list.append(i.volatility)
            variance_list.append(i.variance)
            stock_ending_vals.append(i.end_val)
        self.returns_table = returns_table
        self.portfolio_volatility = sum(volatility_list)/len(volatility_list)
        self.portoflio_variance = sum(variance_list)/len(variance_list)
        print('key_names: ', key_names)


        # get determinant for portfolio            
        stocks_dict = dict(zip(key_names, returns_table))
        dataframe = pd.DataFrame(stocks_dict)
        corr_matrix = dataframe.corr()
        numpy_matrix = corr_matrix.to_numpy()
        self.determinant = np.linalg.det(numpy_matrix)
        # end determinant block

        # get r_squared values
        sum_val = sum(stock_ending_vals)/len(stock_ending_vals)
        difference_list = []
        for i in stock_ending_vals:
            difference = i - sum_val
            difference_squared = (difference**2)
            difference_list.append(difference_squared)

        #print('len(difference_list): ', len(difference_list))
        #print('type(difference_list): ', type(difference_list))
        root_difference = (sum(difference_list)/len(difference_list))**(1/2)
        self.portfolio_sum_of_differences = root_difference

        """^^^ normalization for r_squared must be calculated outside of 
        portfolio object since all portfolios must be analyzed to determine
        normalization constant"""
        # end r_squared block

    # yearly_return function calculates compounded growth rate for each year
    # date list is something like return_table or aggressive_table which is
    # one of the cleaned dataframes with just closing price across reinvestment
    # time frames.
    def yearly_return(self, p, res, date_list):
        from datetime import date
        opening = date(date_list.index[0].year, date_list.index[0].month, date_list.index[0].day)
        closing = date(date_list.index[-1].year, date_list.index[-1].month, date_list.index[-1].day)
        delta = closing - opening
        days = delta.days
        years = days/365.25
        #################
        
        compound_interest_factor = res/p
        exp_val = compound_interest_factor**(1/(years))
        exp_val -= 1
        exp_val = 100*exp_val
        return exp_val

    """Member functions for portfolio strategies"""
    def buy_and_hold(self, weightings, roi_table):
        buy_and_hold_portfolio = weightings
        calc_table = roi_table
        statement = []
        #print('Error searching 1: len(calc_table[0])', len(calc_table[0]))
        for index in range(0,len(calc_table[0])):
            value = sum(buy_and_hold_portfolio)
            statement.append(value)
            #print('Error searching 2: len(buy_and_hold_portfolio)', len(buy_and_hold_portfolio))
            for count in range(0, len(buy_and_hold_portfolio)):
                #print('Error seraching 3: count', count)
                buy_and_hold_portfolio[count] = buy_and_hold_portfolio[count]*calc_table[count][index]

        end_val = sum(buy_and_hold_portfolio)
        print('=====================================')
        print('len(bh statement): ', len(statement))
        print('statement: ', statement)
        print('=====================================')
        return end_val, buy_and_hold_portfolio, statement



    # calculates tactical rebalance returns.
    def tactical_rebalance(self, weightings, roi_table, immutable_weightings):
        rebalance_portfolio = weightings
        calc_table = roi_table

        statement = []
        for index in range(0,len(calc_table[0])): #<-- number of returns
            for count in range(0, len(rebalance_portfolio)):
                rebalance_portfolio[count] = rebalance_portfolio[count]*calc_table[count][index]

            value = sum(rebalance_portfolio)
            for count in range(0, len(rebalance_portfolio)):
                rebalance_portfolio[count] = value*(immutable_weightings[count]/sum(immutable_weightings))
                
            statement.append(value)
        statement.insert(0, 1000.00) # $1,000 inserted to begining of rebalance list
        statement.pop() # since we added '1,000' to front of list, we're now popping last element

        end_val = sum(rebalance_portfolio)
        print('=====================================')
        print('len(reb statement): ', len(statement))
        print('statement: ', statement)
        print('=====================================')
        return end_val, rebalance_portfolio, statement





###########################################
# Machine Learning block/module will be the over-seeing module
# that can see all portfolios and concern itself with normalization
###########################################

    

        


