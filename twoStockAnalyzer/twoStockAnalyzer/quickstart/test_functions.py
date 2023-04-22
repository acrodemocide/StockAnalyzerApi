# tests and debugging

# timer
#import builtins
#import contextlib, io
#from unittest.mock import Mock
#import time


######## This block needs unit testing for sure to make sure ######
########the stocks are indeed made uniform########

#period = 21 # this is roughly monthly. This is a value
## That will eventually be selected by the user.
#
#"""Now we want to create the stock objects"""
#stock_objects_list = []
#for i in range(0,len(full_list)):
#    stock_objects_list.append(Stock(full_list[i], threaded_list[i]))
#"""List of stock objects stored in stocck_objects_list. None 
#of these have assigned variable names, and can be viewed by 
#looking at the object 'name' attribute"""
#
#make_stocks_uniform(stock_objects_list, period)

####################

#start_time = time.time()
#print("---%s seconds ---" % (time.time()-start_time))

# This block is calling the function 'extract()' and the
# full_list and processing it already. So after, I have
# to do the clean_and_combine()
"""
#print('1 begin')
###### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ###############
test_list = []
import concurrent.futures
def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for r in executor.map(extract, full_list): 
            # ^^ instead of 'full_list' can do 'user_input_arr'
            # if we create a database to minimize function calls.
            test_list.append(r)
#print('1 end')

########### catch error message from yahoo api ###########
# error handling method taken from:
# https://stackoverflow.com/questions/62360192/how-to-check-that-print-was-called-in-a-function
#print('2 begin')
mock = Mock()
mock.side_effect = print 
print_original = print
builtins.print = mock

try:
    str_io = io.StringIO()
    with contextlib.redirect_stdout(str_io):
        main()
    output = str_io.getvalue()

    if output:
        print('Error from yahoo, quit the program')
        print('yahoo error message: ', output)
        exit()
    else:
        print('no error from yahoo api, continue execution')

finally:
    pass
#print('2 end')"""