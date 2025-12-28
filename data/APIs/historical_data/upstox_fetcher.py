import requests
from datetime import datetime
from typing import Iterable

from core.env import get_env
from data.APIs.historical_data.data_fetcher_base import (
    DataFetcherBase,
    QKCandle,
)
from core.common_types import Unit


class UpstoxFetcher(DataFetcherBase):
    supports_intraday = True
    supports_historical = True

    BASE_URL = "https://api.upstox.com/v3"

    _UNIT_MAP = {
        Unit.minutes: "minutes",
        Unit.hours: "hours",
        Unit.days: "days",
        Unit.weeks: "weeks",
        Unit.months: "months",
    }

    def __init__(self):
        self.access_token = get_env("UPSTOX_ACCESS_TOKEN")

    def _connect(self) -> None:
        return

    def _headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

    def _fetch_intraday(
        self,
        symbol: str,
        unit: Unit,
        interval: int,
    ) -> Iterable[QKCandle]:

        unit_str = self._UNIT_MAP[unit]

        url = (
            f"{self.BASE_URL}/historical-candle/intraday/"
            f"{symbol}/{unit_str}/{interval}"
        )

        response = requests.get(url, headers=self._headers())
        response.raise_for_status()

        candles = response.json().get("data", {}).get("candles", [])
        return (
            QKCandle(
                timestamp=datetime.fromisoformat(c[0]),
                open=float(c[1]),
                high=float(c[2]),
                low=float(c[3]),
                close=float(c[4]),
                adjclose=float(c[4]),
                volume=float(c[5]),
            )
            for c in candles
        )

    # ---------- HISTORICAL ----------
    def _fetch_historical(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        unit: Unit,
        interval: int,
    ) -> Iterable[QKCandle]:

        unit_str = self._UNIT_MAP[unit]

        url = (
            f"{self.BASE_URL}/historical-candle/"
            f"{symbol}/{unit_str}/{interval}/"
            f"{end.date()}/{start.date()}"
        )

        response = requests.get(url, headers=self._headers())
        response.raise_for_status()

        candles = response.json().get("data", {}).get("candles", [])

        return (
            QKCandle(
                timestamp=datetime.fromisoformat(c[0]),
                open=float(c[1]),
                high=float(c[2]),
                low=float(c[3]),
                close=float(c[4]),
                adjclose=float(c[4]),
                volume=float(c[5]),
            )
            for c in candles
        )


if __name__ == "__main__":
    fetcher = UpstoxFetcher()
    fetcher.debug_test('NSE_EQ|INE848E01016')