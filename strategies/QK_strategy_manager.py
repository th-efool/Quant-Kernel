# strategies/QK_strategy_manager.py
import pandas as pd
from strategies.base.strategy_base import StrategyBase


class StrategyManager:
    def __init__(self):
        self._strategies: list[StrategyBase] = []

    def add(self, strategy: StrategyBase):
        self._strategies.append(strategy)
        return self

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        for strategy in self._strategies:
            signal = strategy.compute(df)

            if not signal.index.equals(df.index):
                raise ValueError("Signal index mismatch")

            df[strategy.signal_column] = signal

        return df


from indicators.QK_indicator_manager import IndicatorManager
from indicators.base.indicator_type import IndicatorType
from strategies.QK_strategy_manager import StrategyManager
from strategies.strategy_ma_crossover import MACrossoverStrategy
from strategies.strategy_mcginley_breakout import McGinleyBreakoutStrategy
from core.test_data_generator import make_test_df

if __name__ == "__main__":
    df = make_test_df(100)

    # --- indicators ---
    ind_mgr = IndicatorManager()
    ind_mgr.add(IndicatorType.MA(period=7))
    ind_mgr.add(IndicatorType.MA(period=21))
    ind_mgr.add(IndicatorType.MC_GINLEY(period=14))

    df = ind_mgr.run(df)

    # --- strategies ---
    strat_mgr = StrategyManager()
    strat_mgr.add(MACrossoverStrategy("ma_7", "ma_21"))
    strat_mgr.add(McGinleyBreakoutStrategy("close", "mcginley_14"))

    df = strat_mgr.run(df)
    print(df)