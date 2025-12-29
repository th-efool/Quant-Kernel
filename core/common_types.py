from enum import Enum

class QKApi(Enum):
    upstox = 1
    dhan = 2
    yfinance = 3

class Unit(Enum):
    minutes = 'm'
    hours = 'h'
    days = 'd'
    weeks = 'w'
    months = 'mo'
    years = 'y'

class TickerSource(Enum):
    INDIA = "D:/PycharmProjects/quant-kernel/data/ticker_symbols/india.yaml"
    # FUTURE:
    # US = "data/APIs/ticker_symbols/us.yaml"
    # CRYPTO = "data/APIs/ticker_symbols/crypto.yaml"

from datetime import datetime, timedelta


class QKDate:
    def __init__(self, value: str):
        datetime.strptime(value, "%Y-%m-%d")
        self._value = value

    def __str__(self):
        return self._value

    def value(self) -> str:
        return self._value

    @classmethod
    def today(cls):
        return cls(datetime.today().strftime("%Y-%m-%d"))

    @classmethod
    def yesterday(cls):
        return cls((datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"))

    @classmethod
    def days_ago(cls, days: int):
        return cls((datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d"))


class QKCandle:
    def __init__(
        self,
        timestamp: datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        adjclose: float,
        volume: float
    ):
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adjclose = adjclose
        self.volume = volume
