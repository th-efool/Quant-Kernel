import pandas as pd

from indicators.indicator_vwap import VWAP
from strategies.base.strategy_base import StrategyBase
from strategies.base.signal_type import Signal

class VWAPCrossoverStrategy(StrategyBase):
    signal_column = "vwap_cross"

    def __init__(self, fast_days, slow_days):
        self.fast = fast_days
        self.slow = slow_days

    def indicators(self):
        return [
            VWAP(self.fast),
            VWAP(self.slow),
        ]

    def compute(self, df):
        f = df[f"vwap_{self.fast}d"]
        s = df[f"vwap_{self.slow}d"]

        signal = pd.Series(Signal.HOLD, index=df.index)
        signal[(f > s) & (f.shift(1) <= s.shift(1))] = Signal.BUY
        signal[(f < s) & (f.shift(1) >= s.shift(1))] = Signal.SELL
        return signal

