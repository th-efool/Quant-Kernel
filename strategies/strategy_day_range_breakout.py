import pandas as pd

from indicators.indicator_day_range_percentage import DayRangePct
from strategies.base.strategy_base import StrategyBase
from strategies.base.signal_type import Signal


class DayRangeBreakoutStrategy(StrategyBase):
    signal_column = "day_range_break"

    def __init__(self, threshold=0.05):
        self.threshold = threshold

    def indicators(self):
        return [DayRangePct()]

    def compute(self, df):
        signal = pd.Series(Signal.HOLD, index=df.index)
        signal[df["day_range_pct"] >= self.threshold] = Signal.BUY
        return signal

