from typing import Dict
from datetime import datetime
from services.back_tester_interface import BackTesterInterface
from api.transfer_objs.portfolio_response import Portfolio

# TODO: dhoward this is a dummy algorithm for testing purposes
class MyNewAlgorithm(BackTesterInterface):
    def backtest(self, stocks: Dict[str, float]) -> Portfolio:
        print("My new algorithm is backtesting the following stocks:")
        for stock, price in stocks.items():
            print(f"{stock}: {price}")

        return Portfolio({datetime.now(): 100.0})