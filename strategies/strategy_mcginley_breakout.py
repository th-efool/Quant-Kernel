# strategies/strategy_mcginley_breakout.py
import pandas as pd

from indicators.indicator_mcginley import McGinleyDynamic
from strategies.base.strategy_base import StrategyBase
from strategies.base.signal_type import Signal


class McGinleyBreakoutStrategy(StrategyBase):
    signal_column = "mcg_break_signal"

    def __init__(self, period :int =14, k : float =0.6, price_col="close", mcg_col="mcginley"):
        self.period = period
        self.k = k
        self.price = price_col
        self.mcg = mcg_col

    def indicators(self):
        return [
            McGinleyDynamic(period=self.period,source=self.price,k= self.k )
        ]

    def compute(self, df: pd.DataFrame) -> pd.Series:
        signal = pd.Series(Signal.HOLD, index=df.index)

        if self.price not in df or self.mcg not in df:
            return signal

        price = df[self.price]
        mcg = df[self.mcg]

        valid = price.notna() & mcg.notna()

        up = (price > mcg) & (price.shift(1) <= mcg.shift(1))
        down = (price < mcg) & (price.shift(1) >= mcg.shift(1))

        signal[valid & up] = Signal.BUY
        signal[valid & down] = Signal.SELL

        return signal
