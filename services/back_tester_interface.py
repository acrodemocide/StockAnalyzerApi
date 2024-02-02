
from typing import Dict

class BackTesterInterface:
    def backtest(self, stocks: Dict[str, float]) -> None:
        pass
