class PortfolioRequest(object):
    def __init__(self, holdings, buy_and_hold_allocation, tactical_rebalance_allocation):
        self.holdings = holdings
        self.buy_and_hold_allocation = buy_and_hold_allocation
        self.tactical_rebalance_allocation = tactical_rebalance_allocation