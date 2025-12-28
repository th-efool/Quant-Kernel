# strategies/strategy_ma_crossover.py
import pandas as pd
from strategies.base.strategy_base import StrategyBase
from strategies.base.signal_type import Signal


class MACrossoverStrategy(StrategyBase):
    signal_column = "ma_cross_signal"

    def __init__(self, fast: str, slow: str):
        self.fast = fast
        self.slow = slow

    def compute(self, df: pd.DataFrame) -> pd.Series:
        signal = pd.Series(Signal.HOLD, index=df.index)

        if self.fast not in df or self.slow not in df:
            return signal

        fast = df[self.fast]
        slow = df[self.slow]

        valid = fast.notna() & slow.notna()

        cross_up = (fast > slow) & (fast.shift(1) <= slow.shift(1))
        cross_dn = (fast < slow) & (fast.shift(1) >= slow.shift(1))

        signal[valid & cross_up] = Signal.BUY
        signal[valid & cross_dn] = Signal.SELL

        return signal
