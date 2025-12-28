import pandas as pd
from indicators.base.indicator_base import IndicatorBase


class VWAP(IndicatorBase):
    def __init__(self, days: int):
        self.days = days

    def compute(self, df: pd.DataFrame) -> dict:
        tp = (df["high"] + df["low"] + df["close"]) / 3
        vol = df["volume"]

        vwap = pd.Series(index=df.index, dtype="float64")

        # Normalize timestamps to date boundary
        dates = df["timestamp"].dt.floor("D")

        cum_tp_vol = 0.0
        cum_vol = 0.0
        current_start = dates.iloc[0]

        for i in range(len(df)):
            # reset when window exceeds N days
            if (dates.iloc[i] - current_start).days >= self.days:
                current_start = dates.iloc[i]
                cum_tp_vol = 0.0
                cum_vol = 0.0

            cum_tp_vol += tp.iloc[i] * vol.iloc[i]
            cum_vol += vol.iloc[i]

            if cum_vol == 0:
                vwap.iloc[i] = float("nan")
            else:
                vwap.iloc[i] = cum_tp_vol / cum_vol

        return {self.column_name(): vwap}

    def column_name(self):
        return f"vwap_{self.days}d"
