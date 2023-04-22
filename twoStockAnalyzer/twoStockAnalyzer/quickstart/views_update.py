# updated views

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, DataObjectSerializer, InputSerializer
from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework.request import Request
from .data_cleaning import extract, make_stocks_uniform
from .back_end_update import Stock, Portfolio
#from .quick_and_dirty import return_graph_vals

#import yfinance as yf
import pandas as pd
import numpy as np
import time
#########
import builtins
import contextlib, io
from unittest.mock import Mock

print('pandas version: ', pd.__version__)
###############################################################
class DataObject(object):
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
    DataObject(id=1, name='aggressive', b_and_h_value='23458', tactical_rebal_value='6315', 
              b_and_h_allocation=[200, 650, 100, 50], tactical_rebal_allocation=[250, 250, 250, 250], 
              bh_graph_data=[], tr_graph_data=[], holdings=['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']),
    DataObject(id=2, name='moderate', b_and_h_value='18142', tactical_rebal_value='5151', 
              b_and_h_allocation=[250, 400, 200, 150], tactical_rebal_allocation=[250, 250, 250, 250], 
              bh_graph_data=[], tr_graph_data=[], holdings=['ANWPX', 'AMECX', 'ABNDX', 'ABALX']),
    DataObject(id=3, name='conservative', b_and_h_value='11241', tactical_rebal_value='4444', 
              b_and_h_allocation=[200, 100, 700], tactical_rebal_allocation=[250, 250, 250], 
              bh_graph_data=[], tr_graph_data=[], holdings=['ABALX', 'AMECX', 'ABNDX']),
    DataObject(id=4, name='index', b_and_h_value='68686', tactical_rebal_value='5555', 
              b_and_h_allocation=[1000], tactical_rebal_allocation=[1000], 
              bh_graph_data=[], tr_graph_data=[], holdings=['VTSMX'])
]
##############################################################


## Create your views here.
class PortfolioViewSet(viewsets.ViewSet):

    def create(self, request):
        #### test section ####

        Folios = [
            DataObject(id=1, name='aggressive', b_and_h_value='23458', tactical_rebal_value='6315', 
                    b_and_h_allocation=[200, 650, 100, 50], tactical_rebal_allocation=[250, 250, 250, 250], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['AMRMX', 'AGTHX', 'AMECX', 'ABNDX']),
            DataObject(id=2, name='moderate', b_and_h_value='18142', tactical_rebal_value='5151', 
                    b_and_h_allocation=[250, 400, 200, 150], tactical_rebal_allocation=[250, 250, 250, 250], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['ANWPX', 'AMECX', 'ABNDX', 'ABALX']),
            DataObject(id=3, name='conservative', b_and_h_value='11241', tactical_rebal_value='4444', 
                    b_and_h_allocation=[200, 100, 700], tactical_rebal_allocation=[250, 250, 250], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['ABALX', 'AMECX', 'ABNDX']),
            DataObject(id=4, name='index', b_and_h_value='68686', tactical_rebal_value='5555', 
                    b_and_h_allocation=[1000], tactical_rebal_allocation=[1000], 
                    bh_graph_data=[], tr_graph_data=[], holdings=['VTSMX'])
        ]

        s_test = DataObjectSerializer(data=request.data)
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
        #from concurrent.futures import ProcessPoolExecutor
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

        period = 21 # this is roughly monthly. This is a value
        # That will eventually be selected by the user.

        """Now we want to create the stock objects"""
        stock_objects_list = []
        for i in range(0,len(full_list)):
            stock_objects_list.append(Stock(full_list[i], threaded_list[i]))
        """List of stock objects stored in stocck_objects_list. None 
        of these have assigned variable names, and can be viewed by 
        looking at the object 'name' attribute"""

        make_stocks_uniform(stock_objects_list, period)


        """ Now we want to make different portfolios from
        our uniform stock objects"""
        agg_indices = [0,2,3,5]
        agg_bench_mark_list = [stock_objects_list[index] for index in agg_indices]
        mod_indices = [1,2,3,4]
        mod_benchmark_list = [stock_objects_list[index] for index in mod_indices]
        con_indices = [2,3,4]
        con_benchmark_list = [stock_objects_list[index] for index in con_indices]
        ind_indices = [6]
        ind_benchmark_list = [stock_objects_list[index] for index in ind_indices]
        #custom_indices = [7:]
        AggressiveBenchmarkPortoflio = Portfolio("Aggressive Benchmark Portfolio", agg_bench_mark_list, 
                                                 Folios[0].b_and_h_allocation[:], Folios[0].tactical_rebal_allocation[:])
        ModerateBenchmarkPortfolio = Portfolio("Moderate Benchmark Portfolio", mod_benchmark_list, 
                                               Folios[1].b_and_h_allocation[:], Folios[1].tactical_rebal_allocation[:])
        ConservativeBenchmarkPortfolio = Portfolio("Conservative Benchmark Portfolio", con_benchmark_list, 
                                                   Folios[2].b_and_h_allocation[:], Folios[2].tactical_rebal_allocation[:])
        IndexBenchmarkPortfolio = Portfolio("Index Benchmark Portfolio", ind_benchmark_list, 
                                            Folios[3].b_and_h_allocation[:], Folios[3].tactical_rebal_allocation[:])
        CustomPortfolio = Portfolio("Custom Portfolio", stock_objects_list[7:], 
                                    data_test["b_and_h_allocation"][:], data_test["tactical_rebal_allocation"][:])

        
        buy_and_hold_result = CustomPortfolio.buy_and_hold(CustomPortfolio.bh_weightings, CustomPortfolio.returns_table)
        bhagg =  AggressiveBenchmarkPortoflio.buy_and_hold(AggressiveBenchmarkPortoflio.bh_weightings, AggressiveBenchmarkPortoflio.returns_table)
        bhmod = ModerateBenchmarkPortfolio.buy_and_hold(ModerateBenchmarkPortfolio.bh_weightings, ModerateBenchmarkPortfolio.returns_table)
        bhcon = ConservativeBenchmarkPortfolio.buy_and_hold(ConservativeBenchmarkPortfolio.bh_weightings, ConservativeBenchmarkPortfolio.returns_table)
        bhind = IndexBenchmarkPortfolio.buy_and_hold(IndexBenchmarkPortfolio.bh_weightings, IndexBenchmarkPortfolio.returns_table)

        tactical_rebal_result = CustomPortfolio.tactical_rebalance(CustomPortfolio.tact_rebal_weightings, CustomPortfolio.returns_table, CustomPortfolio.immutable_weightings)
        tact_agg = CustomPortfolio.tactical_rebalance(AggressiveBenchmarkPortoflio.tact_rebal_weightings, AggressiveBenchmarkPortoflio.returns_table, AggressiveBenchmarkPortoflio.immutable_weightings)
        tact_mod = CustomPortfolio.tactical_rebalance(ModerateBenchmarkPortfolio.tact_rebal_weightings, ModerateBenchmarkPortfolio.returns_table, ModerateBenchmarkPortfolio.immutable_weightings)
        tact_con = CustomPortfolio.tactical_rebalance(ConservativeBenchmarkPortfolio.tact_rebal_weightings, ConservativeBenchmarkPortfolio.returns_table, ConservativeBenchmarkPortfolio.immutable_weightings)
        tact_ind = CustomPortfolio.tactical_rebalance(IndexBenchmarkPortfolio.tact_rebal_weightings, IndexBenchmarkPortfolio.returns_table, IndexBenchmarkPortfolio.immutable_weightings)

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
        ## temporarily going to be used to hold full dataframe
        #data_test["tr_graph_data"] = percent_table
        data_test["tr_graph_data"] = tactical_rebal_result[2]

        print("---%s seconds ---" % (time.time()-start_time))

        ############################################### 
        print('a')   
        Folios.append(data_test)
        print('b')
        serializer = DataObjectSerializer(instance=Folios, many=True)
        print('c')
        #print(t1.to_string())
        return Response(serializer.data)
        


    def list(self, request):
        #serializer = PortfolioSerializer(instance=Folios.values(), many = True) 
        serializer = DataObjectSerializer(instance=Folios, many = True) 
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