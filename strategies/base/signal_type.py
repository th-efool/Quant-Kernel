# strategies/base/signal_type.py
from enum import Enum

class Signal(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0