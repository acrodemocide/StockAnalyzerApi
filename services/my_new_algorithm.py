from typing import Dict
from services.back_tester_interface import BackTesterInterface

# TODO: dhoward this is a dummy algorithm for testing purposes
class MyNewAlgorithm(BackTesterInterface):
    def backtest(self, stocks: Dict[str, float]) -> None:
        print("My new algorithm is backtesting the following stocks:")
        for stock, price in stocks.items():
            print(f"{stock}: {price}")