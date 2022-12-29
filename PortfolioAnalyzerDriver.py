###########################################################################
# BEGIN FUNCTIONS BLOCK #
###########################################################################

import yfinance as yf
#from pandas_datareader import data as pdr
import pandas as pd
import numpy
#%load_ext Cython

#yf.pdr_override()


# DECLARING VARIABLES AT THE BEGINNING...?
# user_input_arr is the user's selected portfolio and the other
# lists are benchmark lists to compare user's portfolio against
# the bench marks
user_input_arr = ['WMT', 'T', 'AAPL', 'MSFT', 'GE']

benchmarks_arr = ['AMRMX', 'ANWPX', 'AMECX', 'ABNDX', 
                 'ABALX', 'AGTHX', 'VTSMX']

full_list = benchmarks_arr + user_input_arr

#                     20%       65%     10%      5%
aggressive_list = ['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']

#                   25%     40%      20%      15%
moderate_list = ['ANWPX', 'AMECX', 'ABNDX', 'ABALX']

#                     20%       10%       70%
conservative_list = ['ABALX', 'AMECX', 'ABNDX']

#              100%
index_list = ['VTSMX']

# takes list of stock picks and creates dataframe of closing prices for 
# all of the stocks over the longest possible time frame 
# (limited by smallest lifespan) (input is user stock list)
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
def extract(stock_symbol):
    data_arr = []
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="max")
    close = data["Close"]
    data_arr.append(close)
    return data_arr


def clean_and_combine(table_of_prices):
    stocks_list = table_of_prices
    #size = len(stock_list)-1
    #time_frame_arr = []
    length_arr = []
    trimmed_data = []
    #count = 0

    for i in table_of_prices:
        length_arr.append(len(i[0])) # i -> i[0]
    length_arr.sort()
    smallest_period = length_arr[0]
    
    trimmed_data = []
    for i in table_of_prices:
        print('type: ', type(i[0]))
        #print('typetype: ', type(i[0][0]))
        series = i[0]
        trim = series.tail(smallest_period) 
        trimmed_data.append(trim)

    ## for some reason, last row is all 'nan' and first row is all 'nan'
    #trimmed_data is a dataframe series that needs the last element removed for being 'nan'
    portfolio_dataframe = pd.concat(trimmed_data, axis=1, keys=full_list)#keys=user_input_arr)
    return portfolio_dataframe






### END TEST BLOCK ###
######################



# This function takes every nth element from each stock price list
# to use as reference for rebalance. In between rebalance periods, we don't
# really care what the stock price is.


# converts dataframe columns to numpy arrays for faster calculations 
# and converts prices into returns on rebalancing time preferences.  
# (input is rebalance period)
def make_return_percentages(rebalance_period, stocks_arr, stock_table):
    table = stock_table
    #print(rebalance_period)
    rebalance_dates = table.iloc[::rebalance_period, :]
    #print(rebalance_dates)
    # user_input_arr <-- list of stock tickers
    # Each column in rebalance_dates is converted to a numpy array
    # for more efficient calculations.
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
                    print('try except clause. except clause activated, break from loop')
                    break
                    #pass
            flag += 1
        performance_table.append(return_list)
        return_list = []
    return performance_table



# calculates 'buy and hold' returns
def buy_and_hold(weightings, roi_table):
    buy_and_hold_portfolio = weightings
    calc_table = roi_table
    #index = 0
    statement = []
    for index in range(0,len(calc_table[0])):
        value = sum(buy_and_hold_portfolio)
        statement.append(value)
        for count in range(0, len(buy_and_hold_portfolio)):
            buy_and_hold_portfolio[count] = buy_and_hold_portfolio[count]*calc_table[count][index]
    #print('buy and hold: ', buy_and_hold_portfolio)
    end_val = sum(buy_and_hold_portfolio)
    #print('end value: $', format(end_val, ',.2f'))
    #print(' ')
    return end_val, buy_and_hold_portfolio, statement

# calculates tactical rebalance returns.
def tactical_rebalance(weightings, roi_table, immutable_weightings):
    rebalance_portfolio = weightings
    calc_table = roi_table
    rebalance_results = []
#    for i in range(0,len(rebalance_portfolio)):
#        rebalance_results.append(0)
        
    statement = []
    ####################
    for index in range(0,len(calc_table[0])): #<-- number of returns
        
        for count in range(0, len(rebalance_portfolio)):
            
            rebalance_portfolio[count] = rebalance_portfolio[count]*calc_table[count][index]
        value = sum(rebalance_portfolio)
        for count in range(0, len(rebalance_portfolio)):

            rebalance_portfolio[count] = value*(immutable_weightings[count]/sum(immutable_weightings))
            
        statement.append(value)
    #print('rebalancing: ', rebalance_portfolio)
    end_val = sum(rebalance_portfolio)
    #print('end value: $', format(end_val, ',.2f'))
    return end_val, rebalance_portfolio, statement


# yearly_return function calculates compounded growth rate for each year
# date list is something like return_table or aggressive_table which is
# one of the cleaned dataframes with just closing price across reinvestment
# time frames.
def yearly_return(p, res, date_list):
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
###################################################################################
# END FUNCTION BLOCK #
###################################################################################




###################################################################################
# I GUESS THIS WOULD BE CONSIDERED MAIN: #
###################################################################################
print('1')


print('2')


# The organize_data_func() function returns a dataframe with the given
# ticker symbols's prices. the dataframe length is limited by the lifetime
# of the youngest/newest ticker symbol. For example, if you had a portfolio
# with General Electric stock and Tesla stock, the dataframe would be limited
# by the available data for Tesla since Tesla has been around for much less
# time.

#aggressive_table = organize_data_func(full_list).iloc[:,[0,5,2,3]] # [0,5,2,3]
print('3')
#print(aggressive_table)
#moderate_table = organize_data_func(full_list).iloc[:,[1,2,3,4]]     # [1,2,3,4]
print('4')
#print(moderate_table)
#conservative_table = organize_data_func(full_list).iloc[:,[4,2,3]] # [4,2,3]
print('5')
#index_table = organize_data_func(full_list).iloc[:,[6]] # [6]
print('6')
#return_table = organize_data_func(full_list).iloc[:,7:] #[7:]
print('7')
#print(return_table)


# This block is calling the function 'extract()' and the
# full_list and processing it already. So after, I have
# to do the clean_and_combine()
test_list = []
import concurrent.futures
def main():
    #with ProcessPoolExecutor(max_workers=4) as executor:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for r in executor.map(extract, full_list): 
            # ^^ instead of 'full_list' can do 'user_input_arr'
            # if we create a database to minimize function calls.
            test_list.append(r)
if __name__ == '__main__':
    main()

print('test_list type: ', type(test_list))
print('test_list len: ', len(test_list))
print('test_list lenlen: ', len(test_list[0]))
print('test_list lenlenlen: ', len(test_list[0][0]))
print('test_list: ', type(test_list))
print('test_list[0]: ', type(test_list[0]))
print('test_list[0][0]: ', type(test_list[0][0]))
print(' ')
# test_list <-- list of stocks 
# test_list[0] <-- list of len==1 of a pandas dataseries
# test_list[0][0] <-- list of all stock prices.
# So iterating will be like: test_list[i][0]

print('a')
t1 = clean_and_combine(test_list)
print('t1 table: ', t1)
print('b')
aggressive_table = t1.iloc[:,[0,5,2,3]]
print('c')
moderate_table = t1.iloc[:,[1,2,3,4]]
conservative_table = t1.iloc[:,[4,2,3]]
index_table = t1.iloc[:,[6]]
return_table = t1.iloc[:,7:]

#test_table = organize_data_func(full_list)
#aggressive_table = test_table.iloc[:,[0,5,2,3]]
#moderate_table = test_table.iloc[:,[1,2,3,4]]
#conservative_table = test_table.iloc[:,[4,2,3]]
#index_table = test_table.iloc[:,[6]]
#return_table = test_table.iloc[:,7:]

print('8')
# period is the rebalancing period. Since each month varies with 
# its number of trading days, periodic rebalance periods are estimated
# to align with available data. There seems to be some weird issue with
# the indexing approach I took where the actually data pulled is every 
# (n+2)th period. So selecting a period of 3 = (3+2) = everty 5th trading
# day. Since the market is closed on the weekends, this is very close
# to a weekly rebalancing strategy.
period = 3 #21 is roughly monthly, period 3 is roughly weekly

print('9')

# here we take our dataframe filled with prices and dates and use the 
# make_return_percentages() function to return growth. e.g. AAPL on Monday
# is $10.00/share and on Tuesday the price is $12.50/share. Then the 
# percent_table gives a value of Tuesday/Monday = 1.25. We will later
# use this to plug in our money and calculate returns. So if I invest
# $100 on monday, I can use the percentage table to determine that I
# would have a portfolio balance of $125 just a day later.
percent_table = make_return_percentages(period, user_input_arr, return_table)
print('10')
aggressive_percent = make_return_percentages(period, aggressive_list, aggressive_table)
print('11')
moderate_percent = make_return_percentages(period, moderate_list, moderate_table)
print('12')
conservative_percent = make_return_percentages(period, conservative_list, conservative_table)
print('13')
index_percent = make_return_percentages(period, index_list, index_table)
print('14')




###############################################
# The following block of code is pretty ugly but is where each 
# portfolio is created and back-tested. There are several arrays
# below that simulate portfolios with different weightings. Each portfolio
# begins with $1000 dollars and then is calculated against a buy and hold
# strategy vs a rebalancing strategy.
##############################################

# need to customize weightings still... Default is equal weightings 
# at the moment.

# main:
# buy and hold
# maybe store these allocation in a global struct, then call
# upon them as needed rather than copy-and-paste
aggressive_allocation = [200, 650, 100, 50]
moderate_allocation = [250, 400, 200, 150]
conservative_allocation = [200, 100, 700]
index_allocation = [1000]

# creates portfolio of equal weightings based on length. for example,
# a user that has created a portfolio of 4 stocks with have a 25%
# weighting in each stock. Will make this customizable in the future
# but for now, this will work.
portfolio_weightings = []
for i in range(0, len(user_input_arr)):
    portfolio_weightings.append(200)
#portfolio_weightings = [200, 200, 200, 200, 200]
buy_and_hold_result = buy_and_hold(portfolio_weightings, percent_table)
bhagg = buy_and_hold(aggressive_allocation, aggressive_percent)
bhmod = buy_and_hold(moderate_allocation, moderate_percent)
bhcon = buy_and_hold(conservative_allocation, conservative_percent)
bhind = buy_and_hold(index_allocation, index_percent)


# rebalance strategy has a bit of extra code to account for the 
# way computers store memory. I need to recalculate the portfolio
# with every rebalance, but sinces separate variables can refer
# to the same memory location, I had to add a few extra things here..
# need to pass in weightings for calculations so weightings stay the same
im_agg = [200, 650, 100, 50]
im_mod = [250, 400, 200, 150]
im_con = [200, 100, 700]
im_ind = [1000]

aggressive_allocation = [200, 650, 100, 50]
moderate_allocation = [250, 400, 200, 150]
conservative_allocation = [200, 100, 700]
index_allocation = [1000]
im_port = []

# creates portfolio of equal weightings based on length. for example,
# a user that has created a portfolio of 4 stocks with have a 25%
# weighting in each stock. Will make this customizable in the future
# but for now, this will work.
portfolio_weightings = []
for i in range(0, len(user_input_arr)):
    portfolio_weightings.append(200)
    im_port.append(200)
#portfolio_weightings = [200, 200, 200, 200, 200]
tactical_rebal_result = tactical_rebalance(portfolio_weightings, percent_table, im_port)
tact_agg = tactical_rebalance(aggressive_allocation, aggressive_percent, im_agg)
tact_mod = tactical_rebalance(moderate_allocation, moderate_percent, im_mod)
tact_con = tactical_rebalance(conservative_allocation, conservative_percent, im_con)
tact_ind = tactical_rebalance(index_allocation, index_percent, im_ind)


#print('buy and hold: ', buy_and_hold_result[0], buy_and_hold_result[1])
#print('length: ', len(buy_and_hold_result[2]))
print('aggressive: ', bhagg[0], bhagg[1])
print('length2: ', len(bhagg[2]))
#print('moderate: ', bhmod[0], bhmod[1])
#print('length3: ', len(bhmod[2]))
#print('conservative: ', bhcon[0], bhcon[1])
#print('length4: ', len(bhcon[2]))
print('index: ', bhind[0], bhind[1])
print('length5: ', len(bhind[2]))
#print(' ')
#print(' ')
#print('tactical_rebal_result: ', tactical_rebal_result[0], tactical_rebal_result[1])
#print('aggressive: ', tact_agg[0], tact_agg[1])
#print('moderate: ', tact_mod[0], tact_mod[1])
#print('conservative: ', tact_con[0], tact_con[1])
#print('index: ', tact_ind[0], tact_ind[1])

#print('time frame: ', len(percent_table[0]))

###############################################################################################
# END MAIN #
###############################################################################################



###############################################################################################
# BEGIN DATA VISUALIZATION/PORTFOLIO PERFORMANCE REPORT FOR USER (I GUESS WHAT IS DISPLAYED TO THE USER) #
###############################################################################################

# heat map of position correlations. Not super important for MVP, but
# will play a large role in demonstrating the way rebalance strategies 
# work

##############################
##### Correlation Matrix #####
#import seaborn as sb
##corr = organize_data_func(user_input_arr).corr()
#corr = return_table.corr()
#sb.heatmap(corr, cmap="Blues", annot=True)



# Data visualization demonstrating select portfolio returns
# for an easy visual comparison of returns
# Attempt to graph:
x_axis = []
for i in range(0,len(percent_table[0])):
    x_axis.append(i)
    
x_arr = []
for i in range(0,len(percent_table[0])):
    x_arr.append(i)

#print(x_arr)
import matplotlib.pyplot as plt
plt.plot(buy_and_hold_result[2], 'r')
#ax.plot(buy_and_hold_result[2])
plt.plot(tactical_rebal_result[2], 'g')
#ax.plot(tactical_rebal_result[2])
plt.plot(bhagg[2], 'b')
#ax.plot(bhagg[2])
plt.plot(bhmod[2], 'y')
#ax.plot(bhmod[2])
plt.plot(bhcon[2], 'c')
#ax.plot(bhcon[2])
plt.plot(bhind[2], 'm')
#ax.plot(bhind[2])
#ax.legend(['buy&hold', 'rebalance', '1', '2', '3', '4'])
plt.ylabel('some numbers')
plt.show()



# returns your average compounding interest rate accross the
# investment time period. Need to add each investment result
principal = 1000 # starting dollar amount
portfolio1 = yearly_return(principal, buy_and_hold_result[0], return_table)
print(portfolio1)
print(buy_and_hold_result[0])
print(' ')

portfolio2 = yearly_return(principal, tactical_rebal_result[0], return_table)
print(portfolio2)
print(tactical_rebal_result[0])

p3 = yearly_return(principal, bhagg[0], aggressive_table)
print('p3: ', bhagg[0])

p4 = yearly_return(principal, bhind[0], index_table)
print('p4: ', bhind[0])

##################################################################################
# END DISPLAY #
##################################################################################
