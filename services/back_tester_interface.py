from datetime import datetime
from typing import Dict

class BackTesterInterface:
    def backtest(self, stocks: Dict[str, float], initial_value: float, start_date: datetime, end_date: datetime) -> Dict[datetime, float]:
        pass
