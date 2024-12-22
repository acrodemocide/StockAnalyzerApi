from typing import Dict
from datetime import datetime, timedelta
from services.back_tester_interface import BackTesterInterface

# TODO: dhoward this is a dummy algorithm for testing purposes
class MyNewAlgorithm(BackTesterInterface):
    def backtest(self, stocks: Dict[str, float], initial_value: float) -> Dict[datetime, float]:
        print("My new algorithm is backtesting the following stocks:")
        for stock, price in stocks.items():
            print(f"{stock}: {price}")

        # TODO: dhoward -- come up with a better representation for this data
            # getting returned
        return {
            'snapshots': {
                datetime.now(): initial_value + 100.0,
                datetime.now() - timedelta(days=1): initial_value + 200.0,
                datetime.now() - timedelta(days=2): initial_value + 300.0,
                datetime.now() - timedelta(days=3): initial_value + 400.0,
                datetime.now() - timedelta(days=4): initial_value + 500.0,
                datetime.now() - timedelta(days=5): initial_value + 600.0,
                datetime.now() - timedelta(days=6): initial_value + 700.0,
                datetime.now() - timedelta(days=7): initial_value + 800.0,
                datetime.now() - timedelta(days=8): initial_value + 900.0,
                datetime.now() - timedelta(days=9): initial_value + 1000.0,
                datetime.now() - timedelta(days=10): initial_value + 1100.0,
                datetime.now() - timedelta(days=11): initial_value + 1200.0,
                datetime.now() - timedelta(days=12): initial_value + 1300.0,
                datetime.now() - timedelta(days=13): initial_value + 1400.0,
                datetime.now() - timedelta(days=14): initial_value + 1500.0,
                datetime.now() - timedelta(days=15): initial_value + 1600.0,
                datetime.now() - timedelta(days=16): initial_value + 1700.0,
                datetime.now() - timedelta(days=17): initial_value + 1800.0,
                datetime.now() - timedelta(days=18): initial_value + 1900.0,
                datetime.now() - timedelta(days=19): initial_value + 2000.0,
                datetime.now() - timedelta(days=20): initial_value + 2100.0,
                datetime.now() - timedelta(days=21): initial_value + 2200.0,
                datetime.now() - timedelta(days=22): initial_value + 2300.0,
                datetime.now() - timedelta(days=23): initial_value + 2400.0,
                datetime.now() - timedelta(days=24): initial_value + 2500.0,
                datetime.now() - timedelta(days=25): initial_value + 2600.0,
                datetime.now() - timedelta(days=26): initial_value + 2700.0,
                datetime.now() - timedelta(days=27): initial_value + 2800.0,
                datetime.now() - timedelta(days=28): initial_value + 2900.0,
                datetime.now() - timedelta(days=29): initial_value + 3000.0,
                datetime.now() - timedelta(days=30): initial_value + 3100.0,
                }
            }