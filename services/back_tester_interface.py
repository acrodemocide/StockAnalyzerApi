from datetime import datetime
from typing import Dict
from api.transfer_objs.portfolio_response import Portfolio

class BackTesterInterface:
    def backtest(self, stocks: Dict[str, float], initial_value: float, start_date: datetime, end_date: datetime) -> Portfolio:
        pass
