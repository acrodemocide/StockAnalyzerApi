class Portfolio(object):
    def __init__(self, id, name, buy_and_hold_final_value, tactical_rebalance_final_value, buy_and_hold_allocation, 
                    tactical_rebalance_allocation, buy_and_hold_graph_data, tactical_rebalance_graph_data, 
                    holdings):
        self.id = id
        self.name = name
        self.buy_and_hold_final_value = buy_and_hold_final_value
        self.tactical_rebalance_final_value = tactical_rebalance_final_value
        self.buy_and_hold_allocation = buy_and_hold_allocation
        self.tactical_rebalance_allocation = tactical_rebalance_allocation
        self.buy_and_hold_graph_data = buy_and_hold_graph_data
        self.tactical_rebalance_graph_data = tactical_rebalance_graph_data
        self.holdings = holdings 