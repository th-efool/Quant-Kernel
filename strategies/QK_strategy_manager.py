
import pandas as pd
from strategies.base.strategy_base import StrategyBase
from indicators.QK_indicator_manager import IndicatorManager


class StrategyManager:
    def __init__(self):
        self._strategies = {}   # key -> strategy instance
        self._indicator_manager = IndicatorManager()

    def _make_key(self, strategy_cls, params: dict):
        return (strategy_cls, frozenset(params.items()))

    def add(self, strategy_type):
        config = strategy_type.value

        strategy_cls = config["strategy"]
        params = config.get("params", {})

        key = self._make_key(strategy_cls, params)

        # Register indicators (idempotent)
        for ind in config["indicators"]:
            self._indicator_manager.add(ind)

        # Override if already exists
        self._strategies[key] = strategy_cls(**params)

        return self

    def run(self, df):
        df = self._indicator_manager.run(df)

        for strategy in self._strategies.values():
            signal = strategy.compute(df)
            df[strategy.signal_column] = signal

        return df




from strategies.QK_strategy_manager import StrategyManager
from strategies.base.strategy_type import StrategyType
from core.test_data_generator import make_test_df

if __name__ == "__main__":
    df = make_test_df(100)

    strategy_mgr = StrategyManager()
    strategy_mgr.add(StrategyType.VWAP_1D_7D)
    df = strategy_mgr.run(df)
    print(df)
