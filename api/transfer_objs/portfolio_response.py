from typing import Dict
from datetime import datetime

class Portfolio(object):
    def __init__(self, snapshots: Dict[datetime, float]):
        self.snapshots = snapshots