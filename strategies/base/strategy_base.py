# strategies/base/strategy_base.py
from abc import ABC, abstractmethod
import pandas as pd


class StrategyBase(ABC):
    signal_column: str  # must be overridden

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "signal_column"):
            raise TypeError(
                f"{cls.__name__} must define class attribute `signal_column`"
            )

        if not isinstance(cls.signal_column, str):
            raise TypeError(
                f"{cls.__name__}.signal_column must be a string"
            )

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.Series:
        pass
