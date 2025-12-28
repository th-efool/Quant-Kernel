# strategies/base/strategy_base.py
from abc import ABC, abstractmethod
import pandas as pd


class StrategyBase(ABC):
    _counter = 0  # class-level counter

    signal_column: str  # must be overridden

    def __init__(self):
        self._instance_id = None

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

    def increment_counter(self):
        type(self)._counter += 1
        self._instance_id = self._counter


    @property
    def signal_name(self):
        return f"{self.signal_column}_{self._instance_id}"

    @abstractmethod
    def indicators(self):
        return []

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.Series:
        pass
