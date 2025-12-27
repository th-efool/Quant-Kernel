import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import Iterable

from data.APIs.historical_data.data_fetcher_base import DataFetcherBase, QKCandle
from core.CommonTypes import Unit


class YahooFetcher(DataFetcherBase):

    supports_intraday = False
    supports_historical = True
    def _connect(self) -> None:
        return


    _UNIT_MAP = {
        Unit.minutes: "m",
        Unit.hours: "h",
        Unit.days: "d",
        Unit.weeks: "wk",
        Unit.months: "mo",
    }
    # ---------- HISTORICAL ----------
    def _fetch_historical(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        unit: Unit,
        interval: int,
    ) -> Iterable[QKCandle]:

        yahoo_interval = f"{interval}{self._UNIT_MAP[unit]}"

        df = yf.download(
            symbol,
            start=start,
            end=end,
            interval=yahoo_interval,
            progress=False,
        )

        if df.empty:
            return []

        df = df.reset_index()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        time_col = "Datetime" if "Datetime" in df.columns else "Date"
        df["timestamp"] = pd.to_datetime(df[time_col])

        df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adjclose",
                "Volume": "volume",
            },
            inplace=True,
        )

        if "adjclose" not in df:
            df["adjclose"] = df["close"]
        return (
            QKCandle(
                timestamp=row["timestamp"],
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                adjclose=row["adjclose"],
                volume=row["volume"],
            )
            for row in df.to_dict("records")
        )



    # ---------- INTRADAY ----------
    def _fetch_intraday(
        self,
        symbol: str,
        unit: Unit,
        interval: int
    ) -> Iterable[QKCandle]:

        yahoo_interval = f"{interval}{unit.value}"

        df = yf.download(
            symbol,
            interval=yahoo_interval,
            period="1d",
            progress=False
        )

        if df.empty:
            return []

        df = df.reset_index()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        time_col = "Datetime" if "Datetime" in df.columns else "Date"
        df["timestamp"] = pd.to_datetime(df[time_col])

        df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adjclose",
                "Volume": "volume",
            },
            inplace=True,
        )

        if "adjclose" not in df:
            df["adjclose"] = df["close"]

        return (
            QKCandle(
                timestamp=row["timestamp"],
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                adjclose=row["adjclose"],
                volume=row["volume"],
            )
            for row in df.to_dict("records")
        )


if __name__ == "__main__":
    YahooFetcher().debug_test('BLUEDART.NS')
