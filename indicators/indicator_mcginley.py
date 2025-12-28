
from indicators.base.indicator_base import*


class McGinleyDynamic(IndicatorBase):
    def __init__(self, period: int = 14, source: str = "close", k: float = 0.6):
        self.period = period
        self.source = source
        self.k = k

    def compute(self, df: pd.DataFrame) -> dict:
        price = df[self.source]
        md = pd.Series(index=df.index, dtype="float64")

        # Initialize first value
        md.iloc[0] = price.iloc[0]

        for i in range(1, len(df)):
            prev = md.iloc[i - 1]
            curr = price.iloc[i]

            # Avoid division explosions
            if prev == 0 or pd.isna(prev):
                md.iloc[i] = curr
            else:
                md.iloc[i] = prev + (
                    (curr - prev)
                    / (self.k * self.period * (curr / prev) ** 4)
                )

        return {f"mcginley_{self.period}": md}


