from typing import Dict

class PortfolioRequest(object):
    def __init__(self, stocks: Dict[str, float], strategy: str, initial_value: float):
        self.stocks = stocks
        self.strategy = strategy
        self.initial_value = initial_value