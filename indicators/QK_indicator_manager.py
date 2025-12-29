import pandas as pd
from indicators.base.indicator_base import IndicatorBase


class IndicatorManager:
    def __init__(self):
        self._indicators = {}  # key -> indicator instance

    def _make_key(self, indicator: IndicatorBase):
        # unique key per indicator configuration
        return (indicator.__class__, tuple(sorted(indicator.__dict__.items())))

    def add(self, indicator: IndicatorBase):
        key = self._make_key(indicator)
        self._indicators[key] = indicator
        return self

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        base_index = df.index

        for indicator in self._indicators.values():
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
    manager.add(IndicatorType.MA(period=21))
    manager.add(IndicatorType.MA(period=21))

    df = make_test_df(100)
    df = manager.run(df)
    print(df)
