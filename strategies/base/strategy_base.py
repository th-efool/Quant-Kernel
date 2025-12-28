# strategies/base/strategy_base.py
from abc import ABC, abstractmethod
import pandas as pd
from strategies.base.signal_type import Signal


class StrategyBase(ABC):
    signal_column: str  # each strategy MUST define this

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.Series:
        """
        Must return a Series aligned with df.index
        """
        pass
