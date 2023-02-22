from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, PortfolioSerializer, InputSerializer
from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework.request import Request
from .portfolio_analyzer import *
#from .quick_and_dirty import return_graph_vals

#import yfinance as yf
import pandas as pd
import numpy
import time
#########
#import builtins
#import contextlib, io
#from unittest.mock import Mock


###############################################################
class Portfolio(object):
    def __init__(self, id, name, b_and_h_value, tactical_rebal_value, b_and_h_allocation, 
                 tactical_rebal_allocation, bh_graph_data, tr_graph_data, holdings):
        self.id = id
        self.name = name
        self.b_and_h_value = b_and_h_value
        self.tactical_rebal_value = tactical_rebal_value
        self.b_and_h_allocation = b_and_h_allocation
        self.tactical_rebal_allocation = tactical_rebal_allocation
        self.bh_graph_data = bh_graph_data
        self.tr_graph_data = tr_graph_data
        self.holdings = holdings 

Folios = [
    Portfolio(id=1, name='aggressive', b_and_h_value='23458', tactical_rebal_value='6315', 
              b_and_h_allocation=[200, 650, 100, 50], tactical_rebal_allocation=[250, 250, 250, 250], 
              bh_graph_data=[], tr_graph_data=[], holdings=['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']),
    Portfolio(id=2, name='moderate', b_and_h_value='18142', tactical_rebal_value='5151', 
              b_and_h_allocation=[250, 400, 200, 150], tactical_rebal_allocation=[250, 250, 250, 250], 
              bh_graph_data=[], tr_graph_data=[], holdings=['ANWPX', 'AMECX', 'ABNDX', 'ABALX']),
    Portfolio(id=3, name='conservative', b_and_h_value='11241', tactical_rebal_value='4444', 
              b_and_h_allocation=[200, 100, 700], tactical_rebal_allocation=[250, 250, 250], 
              bh_graph_data=[], tr_graph_data=[], holdings=['ABALX', 'AMECX', 'ABNDX']),
    Portfolio(id=4, name='index', b_and_h_value='68686', tactical_rebal_value='5555', 
              b_and_h_allocation=[1000], tactical_rebal_allocation=[1000], 
              bh_graph_data=[], tr_graph_data=[], holdings=['VTSMX'])
]
##############################################################


## Create your views here.
class PortfolioViewSet(viewsets.ViewSet):

    def create(self, request):
        #### test section ####

        Folios = [
            Portfolio(id=1, name='aggressive', b_and_h_value='23458', tactical_rebal_value='6315', 
                    b_and_h_allocation=[200, 650, 100, 50], tactical_rebal_allocation=[250, 250, 250, 250], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']),
            Portfolio(id=2, name='moderate', b_and_h_value='18142', tactical_rebal_value='5151', 
                    b_and_h_allocation=[250, 400, 200, 150], tactical_rebal_allocation=[250, 250, 250, 250], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['ANWPX', 'AMECX', 'ABNDX', 'ABALX']),
            Portfolio(id=3, name='conservative', b_and_h_value='11241', tactical_rebal_value='4444', 
                    b_and_h_allocation=[200, 100, 700], tactical_rebal_allocation=[250, 250, 250], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['ABALX', 'AMECX', 'ABNDX']),
            Portfolio(id=4, name='index', b_and_h_value='68686', tactical_rebal_value='5555', 
                    b_and_h_allocation=[1000], tactical_rebal_allocation=[1000], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['VTSMX'])
        ]

        s_test = PortfolioSerializer(data=request.data)
        s_test.is_valid(raise_exception=True)
        data_test = s_test.validated_data # This is the new custom portfolio object.
        ###############################################
        start_time = time.time()
        benchmarks_arr = ['AMRMX', 'ANWPX', 'AMECX', 'ABNDX', 
                'ABALX', 'AGTHX', 'VTSMX']
        aggressive_list = ['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']
        moderate_list = ['ANWPX', 'AMECX', 'ABNDX', 'ABALX']
        conservative_list = ['ABALX', 'AMECX', 'ABNDX']
        index_list = ['VTSMX']

        user_input_arr = data_test["holdings"]
        print('user_input_arr: ', user_input_arr)
        full_list = benchmarks_arr + user_input_arr

        threaded_list = []
        import concurrent.futures
        def main():
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for r in executor.map(extract, full_list): 
                    # ^^ instead of 'full_list' can do 'user_input_arr'
                    # if we create a database to minimize function calls.
                    threaded_list.append(r)

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

        t1 = clean_and_combine(threaded_list, full_list)
        aggressive_table = t1.iloc[:,[0,5,2,3]]
        moderate_table = t1.iloc[:,[1,2,3,4]]
        conservative_table = t1.iloc[:,[4,2,3]]
        index_table = t1.iloc[:,[6]]
        return_table = t1.iloc[:,7:]
        #print('t1 titles: ', t1.columns)
        #print('return table titles: ', return_table.keys())


        period = 20 #21 is roughly monthly, period 3 is roughly weekly
        #print('period type: ', type(period))
        #print('user_input_arr type: ', type(user_input_arr))
        #print('user_input_arr: ', user_input_arr)
        #print('return table type: ', type(return_table))
        #print('return_table keys: ', return_table.keys())
        percent_table = make_return_percentages(period, user_input_arr, return_table)
        aggressive_percent = make_return_percentages(period, aggressive_list, aggressive_table)
        moderate_percent = make_return_percentages(period, moderate_list, moderate_table)
        conservative_percent = make_return_percentages(period, conservative_list, conservative_table)
        index_percent = make_return_percentages(period, index_list, index_table)


        # This is repeated... 
        aggressive_allocation = Folios[0].b_and_h_allocation[:]#[200, 650, 100, 50]
        moderate_allocation = Folios[1].b_and_h_allocation[:]#[250, 400, 200, 150]
        conservative_allocation = Folios[2].b_and_h_allocation[:]#[200, 100, 700]
        index_allocation = Folios[3].b_and_h_allocation[:]#[1000]

        
        ###############################################
        #buy_and_hold_weightings = []
        #for i in range(0, len(user_input_arr)):
        #    buy_and_hold_weightings.append(250)
        buy_and_hold_weightings = data_test["b_and_h_allocation"][:]
        ###############################################

        # Creating Porfolio Objects
        custom_portfolio = Investment_Portfolio(user_input_arr)
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

        im_agg = Folios[0].tactical_rebal_allocation[:]#[200, 650, 100, 50]
        im_mod = Folios[1].tactical_rebal_allocation[:]#[250, 400, 200, 150]
        im_con = Folios[2].tactical_rebal_allocation[:]#[200, 100, 700]
        im_ind = Folios[3].tactical_rebal_allocation[:]#[1000]

        aggressive_allocation = Folios[0].tactical_rebal_allocation[:]#[200, 650, 100, 50]
        moderate_allocation = Folios[1].tactical_rebal_allocation[:]#[250, 400, 200, 150]
        conservative_allocation = Folios[2].tactical_rebal_allocation[:]#[200, 100, 700]
        index_allocation = Folios[3].tactical_rebal_allocation[:]#[1000]
        im_port = data_test["tactical_rebal_allocation"][:]#[250, 250, 250, 250]
        #im_port = []
        
    
        #############################
        tactical_rebal_weightings = data_test["tactical_rebal_allocation"][:]
        im_port = data_test["tactical_rebal_allocation"][:]
        #############################

        tactical_rebal_result = custom_portfolio.tactical_rebalance(tactical_rebal_weightings, percent_table, im_port)
        tact_agg = aggressive_portfolio.tactical_rebalance(aggressive_allocation, aggressive_percent, im_agg)
        tact_mod = moderate_portfolio.tactical_rebalance(moderate_allocation, moderate_percent, im_mod)
        tact_con = conservative_portfolio.tactical_rebalance(conservative_allocation, conservative_percent, im_con)
        tact_ind = index_portfolio.tactical_rebalance(index_allocation, index_percent, im_ind)

        ############### --> end calculation <-- ################
        #### 
        # Portfolio performance returns:
        ## standard portfolios for benchmarks ##
        Folios[0].b_and_h_value = bhagg[0]
        Folios[1].b_and_h_value = bhmod[0]
        Folios[2].b_and_h_value = bhcon[0]
        Folios[3].b_and_h_value = bhind[0]
        Folios[0].b_and_h_allocation = bhagg[1]
        Folios[1].b_and_h_allocation = bhmod[1]
        Folios[2].b_and_h_allocation = bhcon[1]
        Folios[3].b_and_h_allocation = bhind[1]
        Folios[0].bh_graph_data = bhagg[2]
        Folios[1].bh_graph_data = bhmod[2]
        Folios[2].bh_graph_data = bhcon[2]
        Folios[3].bh_graph_data = bhind[2]


        ## custom Portfolio ##
        data_test["b_and_h_value"] = buy_and_hold_result[0]
        data_test["tactical_rebal_value"] = tactical_rebal_result[0]
        data_test["b_and_h_allocation"] = buy_and_hold_result[1]
        data_test["tactical_rebal_allocation"] = tactical_rebal_result[1]
        data_test["bh_graph_data"] = buy_and_hold_result[2]
        data_test["tr_graph_data"] = tactical_rebal_result[2]

        print("---%s seconds ---" % (time.time()-start_time))

        ###############################################    
        Folios.append(data_test)
        serializer = PortfolioSerializer(instance=Folios, many=True)
        return Response(serializer.data)


    def list(self, request):
        #serializer = PortfolioSerializer(instance=Folios.values(), many = True) 
        serializer = PortfolioSerializer(instance=Folios, many = True) 
        return Response(serializer.data)
    

        



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]