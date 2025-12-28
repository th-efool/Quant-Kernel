import pandas as pd


class IndicatorBase:
    def compute(self, df: pd.DataFrame) -> dict[str, pd.Series]:
        """
        Must return Series aligned to df.index.
        Length MUST equal len(df).
        Missing values should be NaN.
        """
        raise NotImplementedError
