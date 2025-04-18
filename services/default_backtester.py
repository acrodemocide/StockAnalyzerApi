from datetime import datetime
from typing import Dict
import yfinance as yf
import pandas as pd
import time
from api.transfer_objs.portfolio_response import Portfolio
import time
import contextlib, io
from services.back_tester_interface import BackTesterInterface

class DefaultBackTester(BackTesterInterface):
    start_time = time.time()

    def backtest(self, user_portfolio: Dict[str, float], initial_value: float, start_date: str, end_date: str) -> Dict[datetime, float]:
        portfolios = self.__generate_portfolios()

        ###############################################
        start_time = time.time()
        benchmarks_arr = ['AMRMX', 'ANWPX', 'AMECX', 'ABNDX', 'ABALX', 'AGTHX', 'VTSMX']
        aggressive_list = ['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']
        moderate_list = ['ANWPX', 'AMECX', 'ABNDX', 'ABALX']
        conservative_list = ['ABALX', 'AMECX', 'ABNDX']
        index_list = ['VTSMX']

        user_stock_picks = user_portfolio.holdings
        # TODO: dhoward -- Do we need the following printout?
        print('user_stock_picks: ', user_stock_picks)
        full_list = benchmarks_arr + user_stock_picks

        threaded_list = []
        import concurrent.futures
        def main():
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for r in executor.map(self.__extract, full_list): 
                    # ^^ instead of 'full_list' can do 'user_input_arr'
                    # if we create a database to minimize function calls.
                    threaded_list.append(r)

        try:
            str_io = io.StringIO()
            with contextlib.redirect_stdout(str_io):
                main()
            output = str_io.getvalue()

            if output:
                # TODO: dhoward -- we need to throw 400 here depending
                # deppending on the context of the error (i.e.: if we get
                # an error indicating that a given stock cannot be found)
                print('Error from yahoo, quit the program')
                print('yahoo error message: ', output)
                exit()
            else:
                print('no error from yahoo api, continue execution')

        finally:
            pass

        t1 = self.__clean_and_combine(threaded_list, full_list)
        aggressive_table = t1.iloc[:,[0,5,2,3]]
        moderate_table = t1.iloc[:,[1,2,3,4]]
        conservative_table = t1.iloc[:,[4,2,3]]
        index_table = t1.iloc[:,[6]]
        return_table = t1.iloc[:,7:]


        period = 20 #21 is roughly monthly, period 3 is roughly weekly
        percent_table = self.make_return_percentages(period, user_stock_picks, return_table)
        aggressive_percent = self.make_return_percentages(period, aggressive_list, aggressive_table)
        moderate_percent = self.make_return_percentages(period, moderate_list, moderate_table)
        conservative_percent = self.make_return_percentages(period, conservative_list, conservative_table)
        index_percent = self.make_return_percentages(period, index_list, index_table)


        # This is repeated... 
        aggressive_allocation = portfolios[0].buy_and_hold_allocation[:]
        moderate_allocation = portfolios[1].buy_and_hold_allocation[:]
        conservative_allocation = portfolios[2].buy_and_hold_allocation[:]
        index_allocation = portfolios[3].buy_and_hold_allocation[:]
        buy_and_hold_weightings = user_portfolio.buy_and_hold_allocation[:]

        # Creating Porfolio Objects
        custom_portfolio = Investment_Portfolio(user_stock_picks)
        aggressive_portfolio = Investment_Portfolio(aggressive_list)
        moderate_portfolio = Investment_Portfolio(moderate_list)
        conservative_portfolio = Investment_Portfolio(conservative_list)
        index_portfolio = Investment_Portfolio(index_list)

        # Now that the objects exist, we can call the member data from the porfolio object
        # and perform their own calculations on themselves.
        buy_and_hold_result = custom_portfolio.buy_and_hold(buy_and_hold_weightings, percent_table)
        bhagg = aggressive_portfolio.buy_and_hold(aggressive_allocation, aggressive_percent)
        bhmod = moderate_portfolio.buy_and_hold(moderate_allocation, moderate_percent)
        bhcon = conservative_portfolio.buy_and_hold(conservative_allocation, conservative_percent)
        bhind = index_portfolio.buy_and_hold(index_allocation, index_percent)


        # rebalance strategy has a bit of extra code to account for the 
        # way computers store memory. I need to recalculate the portfolio
        # with every rebalance, but sinces separate variables can refer
        # to the same memory location, I had to add a few extra things here..
        # need to pass in weightings for calculations so weightings stay the same

        aggressive_allocation = portfolios[0].tactical_rebalance_allocation[:]
        moderate_allocation = portfolios[1].tactical_rebalance_allocation[:]
        conservative_allocation = portfolios[2].tactical_rebalance_allocation[:]
        index_allocation = portfolios[3].tactical_rebalance_allocation[:]
        im_port = user_portfolio.tactical_rebalance_allocation[:]

        #############################
        tactical_rebal_weightings = user_portfolio.tactical_rebalance_allocation[:]
        im_port = user_portfolio.tactical_rebalance_allocation[:]
        #############################

        tactical_rebal_result = custom_portfolio.tactical_rebalance(tactical_rebal_weightings, percent_table, im_port)

        ############### --> end calculation <-- ################
        #### 
        # Portfolio performance returns:
        ## standard portfolios for benchmarks ##
        portfolios[0].buy_and_hold_final_value = bhagg[0]
        portfolios[1].buy_and_hold_final_value = bhmod[0]
        portfolios[2].buy_and_hold_final_value = bhcon[0]
        portfolios[3].buy_and_hold_final_value = bhind[0]
        portfolios[0].buy_and_hold_allocation = bhagg[1]
        portfolios[1].buy_and_hold_allocation = bhmod[1]
        portfolios[2].buy_and_hold_allocation = bhcon[1]
        portfolios[3].buy_and_hold_allocation = bhind[1]
        portfolios[0].buy_and_hold_graph_data = bhagg[2]
        portfolios[1].buy_and_hold_graph_data = bhmod[2]
        portfolios[2].buy_and_hold_graph_data = bhcon[2]
        portfolios[3].buy_and_hold_graph_data = bhind[2]


        ## custom Portfolio ##
        updated_data_test = Portfolio(
            name = 'custom',
            buy_and_hold_final_value = buy_and_hold_result[0],
            tactical_rebalance_final_value = tactical_rebal_result[0],
            buy_and_hold_allocation = buy_and_hold_result[1],
            tactical_rebalance_allocation = tactical_rebal_result[1],
            buy_and_hold_graph_data = buy_and_hold_result[2],
            tactical_rebalance_graph_data = tactical_rebal_result[2],
            holdings = user_portfolio.holdings
        )

        print("---%s seconds ---" % (time.time()-start_time))
        portfolios.append(updated_data_test)

        return portfolios

    def __generate_portfolios(self):
        aggressive_holdings = ['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']
        moderate_holdings = [['ANWPX', 'AMECX', 'ABNDX', 'ABALX']]
        conservative_holdings = ['ABALX', 'AMECX', 'ABNDX']
        index_holdings = ['VTSMX']

        portfolios = [
            Portfolio(
                name='aggressive',
                buy_and_hold_final_value='23458',
                tactical_rebalance_final_value='6315',
                buy_and_hold_allocation=[200, 650, 100, 50],
                tactical_rebalance_allocation=[250, 250, 250, 250],
                buy_and_hold_graph_data=[],
                tactical_rebalance_graph_data=[],
                holdings=aggressive_holdings),

            Portfolio(
                name='moderate',
                buy_and_hold_final_value='18142',
                tactical_rebalance_final_value='5151',
                buy_and_hold_allocation=[250, 400, 200, 150],
                tactical_rebalance_allocation=[250, 250, 250, 250],
                buy_and_hold_graph_data=[],
                tactical_rebalance_graph_data=[],
                holdings=moderate_holdings),

            Portfolio(
                name='conservative',
                buy_and_hold_final_value='11241',
                tactical_rebalance_final_value='4444',
                buy_and_hold_allocation=[200, 100, 700],
                tactical_rebalance_allocation=[250, 250, 250],
                buy_and_hold_graph_data=[],
                tactical_rebalance_graph_data=[],
                holdings=conservative_holdings),

            Portfolio(
                name='index',
                buy_and_hold_final_value='68686',
                tactical_rebalance_final_value='5555',
                buy_and_hold_allocation=[1000],
                tactical_rebalance_allocation=[1000],
                buy_and_hold_graph_data=[],
                tactical_rebalance_graph_data=[],
                holdings=index_holdings)
        ]
        return portfolios

    #def return_graph_vals(user_ticker_list):#, user_ticker_weightings):

    # user_input_arr is the user's selected portfolio and the other
    # lists are benchmark lists to compare user's portfolio against
    # the bench marks

    #user_input_arr = ["msft", "t", "f", "amzn", "wmt", "NTB", "FHB", "MARUY",
    #                "FITB", "ITOCY", "ACNB", "B"]

    #user_input_arr = user_ticker_list

    #benchmarks_arr = ['AMRMX', 'ANWPX', 'AMECX', 'ABNDX', 
    #                'ABALX', 'AGTHX', 'VTSMX']

    #full_list = benchmarks_arr + user_input_arr

    #                     20%       65%     10%      5%m,
    #aggressive_list = ['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']

    #                   25%     40%      20%      15%
    #moderate_list = ['ANWPX', 'AMECX', 'ABNDX', 'ABALX']

    #                     20%       10%       70%
    #conservative_list = ['ABALX', 'AMECX', 'ABNDX']

    #              100%
    #index_list = ['VTSMX']

    # takes list of stock picks and creates dataframe of closing prices for 
    # all of the stocks over the longest possible time frame 
    # (limited by smallest lifespan) (input is user stock list)

    #TODO: dhoward the following function is not referenced -- remove
    def organize_data_func(arr):
        stock_list = arr
        size = len(stock_list)-1
        time_frame_arr = []
        length_arr = []
        trimmed_data = []
        count = 0
        for i in stock_list:
            stock = yf.Ticker(i)
            print('1')
            print('count: ', count)
            data = stock.history(period="max")
            #data = pdr.get_data_yahoo(i, start='1970-01-01')
            close = data['Close']
            time_frame_arr.append(close)
            count += 1
            
        for i in time_frame_arr:
            length_arr.append(len(i))
        length_arr.sort()
        smallest_period = length_arr[0]
        
        trimmed_data = []
        for i in time_frame_arr:
            trim = i.tail(smallest_period) 
            trimmed_data.append(trim)

        ## for some reason, last row is all 'nan' and first row is all 'nan'
        #trimmed_data is a dataframe series that needs the last element removed for being 'nan'
        portfolio_dataframe = pd.concat(trimmed_data, axis=1, keys=arr)
        return portfolio_dataframe



    #####################################
    ## Need to put this in main after user_list has been
    ## defined by the user.
    ### TEST BLOCK FOR MULTITHREADING ###
    from concurrent.futures import ProcessPoolExecutor
    def __extract(self, stock_symbol):
        data_arr = []
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="max")
        close = data["Close"]
        data_arr.append(close)
        return data_arr


    def __clean_and_combine(self, table_of_prices, all_tickers_list):
        length_arr = []
        trimmed_data = []

        for i in table_of_prices:
            length_arr.append(len(i[0]))
        length_arr.sort()
        smallest_period = length_arr[0]
        
        trimmed_data = []
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
        portfolio_dataframe = pd.concat(trimmed_data, axis=1, keys=all_tickers_list)#keys=user_input_arr)
        return portfolio_dataframe


    ### END TEST BLOCK ###
    ######################



    # This function takes every nth element from each stock price list
    # to use as reference for rebalance. In between rebalance periods, we don't
    # really care what the stock price is.


    # converts dataframe columns to numpy arrays for faster calculations 
    # and converts prices into returns on rebalancing time preferences.  
    # (input is rebalance period)
    def __make_return_percentages(self, rebalance_period, stocks_arr, stock_table):
        table = stock_table
        print('table keys: ', table.keys())
        rebalance_dates = table.iloc[::rebalance_period, :]
        print('reblance_dates keys: ', rebalance_dates.keys())
        # user_input_arr <-- list of stock tickers
        # Each column in rebalance_dates is converted to a numpy array
        # for more efficient calculations.
        price_list = []
        for i in stocks_arr:
            print('i: ', i, 'type: ', type(i))
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
                        print('try except clause. except clause activated, break from loop')
                        break
                flag += 1
            performance_table.append(return_list)
            return_list = []
        return performance_table
            
    ###################################################################################
    # END FUNCTION BLOCK #
    ###################################################################################


class Investment_Portfolio:

    def __init__(self, portfolio):
        self.portfolio = portfolio

    # calculates 'buy and hold' returns
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
        end_val = sum(rebalance_portfolio)
        return end_val, rebalance_portfolio, statement


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