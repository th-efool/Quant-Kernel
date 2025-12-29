# strategies/strategy_ma_crossover.py
import pandas as pd

from indicators.indicator_moving_average import MovingAverage
from strategies.base.strategy_base import StrategyBase
from strategies.base.signal_type import Signal


class MACrossoverStrategy(StrategyBase):
    signal_column = "ma_cross"

    def __init__(self, fast, slow):
        self.fast = fast
        self.slow = slow

    def indicators(self):
        return [
            MovingAverage(self.fast),
            MovingAverage(self.slow),
        ]

    def compute(self, df):
        signal = pd.Series(Signal.HOLD, index=df.index)
        f, sl = df[self.fast], df[self.slow]

        signal[(f > sl) & (f.shift(1) <= sl.shift(1))] = Signal.BUY
        signal[(f < sl) & (f.shift(1) >= sl.shift(1))] = Signal.SELL
        return signal

