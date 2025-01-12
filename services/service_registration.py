from services.default_backtester import DefaultBackTester
from services.my_new_algorithm import MyNewAlgorithm
from services.buy_and_hold import BuyAndHold

algorithm_registry = {
    "default": DefaultBackTester(),
    "new_algorithm": MyNewAlgorithm(),
    "buy_and_hold": BuyAndHold()
}
