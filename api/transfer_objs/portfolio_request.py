from typing import Dict

class PortfolioRequest(object):
    def __init__(self, stocks: Dict[str, float], strategy: str):
        self.stocks = stocks
        self.strategy = strategy