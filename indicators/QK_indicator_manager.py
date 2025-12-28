import pandas as pd

from indicators.base.indicator_base import IndicatorBase


class IndicatorManager:
    def __init__(self):
        self._indicators = []

    def add(self, indicator: IndicatorBase):
        self._indicators.append(indicator)
        return self

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        base_index = df.index

        for indicator in self._indicators:
            out = indicator.compute(df)

            for name, series in out.items():
                if not series.index.equals(base_index):
                    raise ValueError(
                        f"Indicator '{name}' returned misaligned index"
                    )

                df[name] = series

        return df

from indicators.base.indicator_type import IndicatorType
from core.test_data_generator import make_test_df

if __name__ == "__main__":
    manager = IndicatorManager()
    manager.add(IndicatorType.MA(period=7))
    manager.add(IndicatorType.MC_GINLEY(period=22))
    manager.add(IndicatorType.MA(period=21))
    df = make_test_df(100)
    df = manager.run(df)
    print(df)
