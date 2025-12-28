from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Iterable
import pandas as pd

from core.common_types import QKCandle, Unit


class DataFetcherBase(ABC):
    """
    Enforced contract for any market data provider.
    """
    supports_intraday: bool = True
    supports_historical: bool = True

    # ---------------- LOW-LEVEL PROVIDER HOOKS ----------------

    @abstractmethod
    def _connect(self) -> None:
        pass

    @abstractmethod
    def _fetch_historical(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        unit: Unit,
        interval: int,
    ) -> Iterable[QKCandle]:
        pass

    @abstractmethod
    def _fetch_intraday(
        self,
        symbol: str,
        unit: Unit,
        interval: int,
    ) -> Iterable[QKCandle]:
        pass

    # ---------------- SHARED UTIL ----------------

    @staticmethod
    def _candles_to_df(candles: Iterable[QKCandle]) -> pd.DataFrame:
        candles = list(candles)

        return pd.DataFrame(
            {
                "timestamp": [c.timestamp for c in candles],
                "open": [c.open for c in candles],
                "high": [c.high for c in candles],
                "low": [c.low for c in candles],
                "close": [c.close for c in candles],
                "adjclose": [c.adjclose for c in candles],
                "volume": [c.volume for c in candles],
            }
        )

    # ---------------- PUBLIC ENTRYPOINT ----------------

    def fetch_df(
            self,
            *,
            symbol: str,
            intraday: bool,
            start: datetime | None = None,
            end: datetime | None = None,
            unit: Unit = Unit.days,
            interval: int = 1,
    ) -> pd.DataFrame:

        self._connect()

        if intraday:
            if not self.supports_intraday:
                raise RuntimeError("Intraday data not supported by this fetcher")

            candles = self._fetch_intraday(
                symbol=symbol,
                unit=unit,
                interval=interval,
            )

        else:
            if not self.supports_historical:
                raise RuntimeError("Historical data not supported by this fetcher")

            if start is None or end is None:
                raise ValueError("start and end must be provided for historical data")

            candles = self._fetch_historical(
                symbol=symbol,
                start=start,
                end=end,
                unit=unit,
                interval=interval,
            )

        return self._candles_to_df(candles)

    # ---------------- DEBUG ----------------

    def debug_test(self, input_symbol: str) -> pd.DataFrame:
        print(f"[DEBUG] Running fetcher test: {self.__class__.__name__}")

        end = datetime.now() - timedelta(days=5)
        start = end - timedelta(days=10)

        df = self.fetch_df(
            symbol=input_symbol,
            intraday=False,
            start=start,
            end=end,
        )

        print("[DEBUG] DataFrame shape:", df.shape)
        print("[DEBUG] Columns:", list(df.columns))
        print(df.head())

        return df
