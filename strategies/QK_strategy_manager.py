
import pandas as pd
from strategies.base.strategy_base import StrategyBase
from indicators.QK_indicator_manager import IndicatorManager
from strategies.strategy_day_range_breakout import DayRangeBreakoutStrategy
from strategies.strategy_mcginley_breakout import McGinleyBreakoutStrategy


class StrategyManager:
    def __init__(self):
        self._strategies = {}   # key -> strategy instance
        self._indicator_manager = IndicatorManager()

    def _make_key(self, strategy):
        # unique per class + params
        return (
            strategy.__class__,
            tuple(sorted(strategy.__dict__.items()))
        )

    def add(self, strategy):
        # key must NOT include _instance_id
        key = (
            strategy.__class__,
            tuple(
                (k, v) for k, v in strategy.__dict__.items()
                if k != "_instance_id"
            )
        )

        # 🔥 if already exists → do nothing
        if key in self._strategies:
            return self

        strategy.increment_counter()

        # register indicators
        for ind in strategy.indicators():
            self._indicator_manager.add(ind)

        self._strategies[key] = strategy
        return self


    def run(self, df):
        df = self._indicator_manager.run(df)

        for strategy in self._strategies.values():
            print(strategy)
            signal = strategy.compute(df)
            df[strategy.signal_name] = signal

        return df




from strategies.QK_strategy_manager import StrategyManager
from core.test_data_generator import make_test_df
from strategies.strategy_vwap_crossover import VWAPCrossoverStrategy

if __name__ == "__main__":
    df = make_test_df(100)

    strategy_mgr = StrategyManager()
    strategy_mgr.add(VWAPCrossoverStrategy(1, 7))
    strategy_mgr.add(DayRangeBreakoutStrategy(0.05))



    df = strategy_mgr.run(df)
    print(df)
