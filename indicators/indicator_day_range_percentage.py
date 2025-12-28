from indicators.base.indicator_base import*


class DayRangePct(IndicatorBase):
    def compute(self, df: pd.DataFrame) -> dict:
        return {
            "day_range_pct": (df["high"] - df["low"]) / df["low"]
        }
