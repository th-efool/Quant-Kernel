import pandas as pd
from strategies.base.strategy_base import StrategyBase
from strategies.base.signal_type import Signal


class VWAPCrossoverStrategy(StrategyBase):
    signal_column = "vwap_cross_signal"

    def __init__(self, vwap_column: str):
        self.vwap_column = vwap_column

    def compute(self, df: pd.DataFrame) -> pd.Series:
        signal = pd.Series(Signal.HOLD, index=df.index)

        if self.vwap_column not in df:
            return signal

        close = df["close"]
        vwap = df[self.vwap_column]

        valid = close.notna() & vwap.notna()

        cross_up = (close > vwap) & (close.shift(1) <= vwap.shift(1))
        cross_dn = (close < vwap) & (close.shift(1) >= vwap.shift(1))

        signal[valid & cross_up] = Signal.BUY
        signal[valid & cross_dn] = Signal.SELL

        return signal
