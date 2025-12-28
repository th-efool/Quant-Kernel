import pandas as pd
from strategies.base.strategy_base import StrategyBase
from strategies.base.signal_type import Signal


class VWAPCrossoverStrategy(StrategyBase):
    signal_column = "vwap_cross_signal"

    def __init__(self, fast_days: int, slow_days: int):
        self.fast_days = fast_days
        self.slow_days = slow_days

    def compute(self, df: pd.DataFrame) -> pd.Series:
        fast_col = f"vwap_{self.fast_days}d"
        slow_col = f"vwap_{self.slow_days}d"

        signal = pd.Series(Signal.HOLD, index=df.index)

        if fast_col not in df or slow_col not in df:
            return signal

        fast = df[fast_col]
        slow = df[slow_col]

        cross_up = (fast > slow) & (fast.shift(1) <= slow.shift(1))
        cross_dn = (fast < slow) & (fast.shift(1) >= slow.shift(1))

        signal[cross_up] = Signal.BUY
        signal[cross_dn] = Signal.SELL

        return signal
