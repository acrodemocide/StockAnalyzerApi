from typing import Dict
from datetime import datetime
from services.back_tester_interface import BackTesterInterface

# TODO: dhoward this is a dummy algorithm for testing purposes
class MyNewAlgorithm(BackTesterInterface):
    def backtest(self, stocks: Dict[str, float]) -> Dict[datetime, float]:
        print("My new algorithm is backtesting the following stocks:")
        for stock, price in stocks.items():
            print(f"{stock}: {price}")

        # TODO: dhoward -- come up with a better representation for this data
            # getting returned
        return {'snapshots': {datetime.now(): 100.0}}