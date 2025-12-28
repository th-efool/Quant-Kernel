from datetime import datetime, timedelta
from typing import Iterable

from dhanhq import dhanhq

from core.env import get_env
from data.APIs.historical_data.data_fetcher_base import (
    DataFetcherBase,
    QKCandle,
)
from core.common_types import Unit


class DhanFetcher(DataFetcherBase):

    supports_intraday = True
    supports_historical = True

    def __init__(self):
        client_id = get_env("DHAN_CLIENT_ID")
        access_token = get_env("DHAN_SECRET_KEY")
        self.dhan = dhanhq(client_id, access_token)

    def _connect(self) -> None:
        # Session is created in __init__
        return

    # ---------- HISTORICAL (DAILY) ----------
    # ---------- HISTORICAL (DAILY ONLY) ----------
    def _fetch_historical(
        self,
        symbol: str,        # security_id
        start: datetime,
        end: datetime,
        unit: Unit,
        interval: int,
    ) -> Iterable[QKCandle]:

        # 🔒 DHAN limitation: ONLY daily candles
        if unit != Unit.days or interval != 1:
            raise ValueError(
                "Dhan historical supports only Unit.days with interval=1"
            )

        response = self.dhan.historical_daily_data(
            security_id=symbol,
            exchange_segment="NSE_EQ",
            instrument_type="EQUITY",
            from_date=start.strftime("%Y-%m-%d"),
            to_date=end.strftime("%Y-%m-%d"),
        )

        if not response or "data" not in response:
            return []

        data = response["data"]

        # DHAN error payload
        if isinstance(data, dict) and "errorMessage" in data:
            raise RuntimeError(
                f"Dhan error {data.get('errorCode')}: {data.get('errorMessage')}"
            )

        if "timestamp" not in data:
            return []

        return self._zip_to_candles(data)

    # ---------- INTRADAY (MINUTES) ----------
    def _fetch_intraday(
        self,
        symbol: str,
        unit: Unit,
        interval: int
    ) -> Iterable[QKCandle]:

        if unit != Unit.MINUTE:
            raise ValueError("Dhan intraday supports minute-based candles only")

        # Dhan hard limit: 90 days per request
        to_dt = datetime.now()
        from_dt = to_dt - timedelta(days=90)

        response = self.dhan.intraday_minute_data(
            security_id=symbol,
            exchange_segment="NSE_EQ",
            instrument_type="EQUITY",
            interval=str(interval),
            from_date=from_dt.strftime("%Y-%m-%d %H:%M:%S"),
            to_date=to_dt.strftime("%Y-%m-%d %H:%M:%S"),
        )

        if not response or "data" not in response:
            return []

        data = response["data"]

        if not data or "timestamp" not in data:
            return []

        return self._zip_to_candles(data)

    # ---------- INTERNAL NORMALIZER ----------
    def _zip_to_candles(self, data: dict) -> Iterable[QKCandle]:
        """
        Convert Dhan column-wise arrays → stream of QKCandle
        """

        opens   = data["open"]
        highs   = data["high"]
        lows    = data["low"]
        closes  = data["close"]
        volumes = data["volume"]
        stamps  = data["timestamp"]

        return (
            QKCandle(
                timestamp=datetime.fromtimestamp(ts),
                open=float(o),
                high=float(h),
                low=float(l),
                close=float(c),
                adjclose=float(c),   # Dhan has no adjusted close
                volume=float(v),
            )
            for o, h, l, c, v, ts in zip(
                opens, highs, lows, closes, volumes, stamps
            )
        )

if __name__ == "__main__":
    fetcher = DhanFetcher()
    fetcher.debug_test('10217')

