import pandas as pd
from indicators.base.indicator_base import IndicatorBase


class VWAP(IndicatorBase):
    def __init__(self, timeframe: str = "D"):
        """
        timeframe:
            'D' = Daily VWAP
            'W' = Weekly VWAP
        """
        self.timeframe = timeframe.lower()

    def compute(self, df: pd.DataFrame) -> dict:
        df = df.copy()

        df["tp"] = (df["high"] + df["low"] + df["close"]) / 3
        df["tp_vol"] = df["tp"] * df["volume"]

        period = df["timestamp"].dt.to_period(self.timeframe)

        vwap = (
            df.groupby(period)
            .apply(lambda x: x["tp_vol"].cumsum() / x["volume"].cumsum())
            .reset_index(level=0, drop=True)
        )

        return {f"vwap_{self.timeframe}": vwap}
