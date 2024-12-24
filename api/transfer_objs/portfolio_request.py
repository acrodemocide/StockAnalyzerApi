from typing import Dict

class PortfolioRequest(object):
    def __init__(self, stocks: Dict[str, float], strategy: str, initial_value: float, start_date: str, end_date: str):
        self.stocks = stocks
        self.strategy = strategy
        self.initial_value = initial_value
        self.start_date = start_date
        self.end_date = end_date