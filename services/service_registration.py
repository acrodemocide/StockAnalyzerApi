from services.default_backtester import DefaultBackTester
from services.my_new_algorithm import MyNewAlgorithm

algorithm_registry = {
    
    "default": DefaultBackTester(),
    "new_algorithm": MyNewAlgorithm()
}
