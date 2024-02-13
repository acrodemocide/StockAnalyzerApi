from typing import Dict
from datetime import datetime, timedelta
from services.back_tester_interface import BackTesterInterface

# TODO: dhoward this is a dummy algorithm for testing purposes
class MyNewAlgorithm(BackTesterInterface):
    def backtest(self, stocks: Dict[str, float]) -> Dict[datetime, float]:
        print("My new algorithm is backtesting the following stocks:")
        for stock, price in stocks.items():
            print(f"{stock}: {price}")

        # TODO: dhoward -- come up with a better representation for this data
            # getting returned
        return {
            'snapshots': {
                datetime.now(): 100.0,
                datetime.now() - timedelta(days=1): 200.0,
                datetime.now() - timedelta(days=2): 300.0,
                datetime.now() - timedelta(days=3): 400.0,
                datetime.now() - timedelta(days=4): 500.0,
                datetime.now() - timedelta(days=5): 600.0,
                datetime.now() - timedelta(days=6): 700.0,
                datetime.now() - timedelta(days=7): 800.0,
                datetime.now() - timedelta(days=8): 900.0,
                datetime.now() - timedelta(days=9): 1000.0,
                datetime.now() - timedelta(days=10): 1100.0,
                datetime.now() - timedelta(days=11): 1200.0,
                datetime.now() - timedelta(days=12): 1300.0,
                datetime.now() - timedelta(days=13): 1400.0,
                datetime.now() - timedelta(days=14): 1500.0,
                datetime.now() - timedelta(days=15): 1600.0,
                datetime.now() - timedelta(days=16): 1700.0,
                datetime.now() - timedelta(days=17): 1800.0,
                datetime.now() - timedelta(days=18): 1900.0,
                datetime.now() - timedelta(days=19): 2000.0,
                datetime.now() - timedelta(days=20): 2100.0,
                datetime.now() - timedelta(days=21): 2200.0,
                datetime.now() - timedelta(days=22): 2300.0,
                datetime.now() - timedelta(days=23): 2400.0,
                datetime.now() - timedelta(days=24): 2500.0,
                datetime.now() - timedelta(days=25): 2600.0,
                datetime.now() - timedelta(days=26): 2700.0,
                datetime.now() - timedelta(days=27): 2800.0,
                datetime.now() - timedelta(days=28): 2900.0,
                datetime.now() - timedelta(days=29): 3000.0,
                datetime.now() - timedelta(days=30): 3100.0,
                }
            }