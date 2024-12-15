from typing import Dict
from api.transfer_objs.portfolio_response import Portfolio

class BackTesterInterface:
    def backtest(self, stocks: Dict[str, float], initial_value: float) -> Portfolio:
        pass
