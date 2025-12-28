from indicators.base.indicator_base import*


class MovingAverage(IndicatorBase):
    def __init__(self, period: int, source: str = "close"):
        self.period = period
        self.source = source

    def compute(self, df: pd.DataFrame) -> dict:
        ma = df[self.source].rolling(
            window=self.period,
            min_periods=self.period
        ).mean()

        return {f"ma_{self.period}": ma}
