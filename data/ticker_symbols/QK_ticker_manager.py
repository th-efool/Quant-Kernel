from typing import Sequence
from core.common_types import QKApi, TickerSource
from data.ticker_symbols.ticker_loader import TickerLoader


class TickerManager:
    def __init__(self, api: QKApi, exchange: str = "NSE"):
        self.api = api
        self.exchange = exchange
        self.TicketLoader = TickerLoader(TickerSource.INDIA)
        symbols = self.TicketLoader.for_api(QKApi.yfinance)
        self._all_tickers = symbols


    @property
    def all(self) -> Sequence:
        return self._all_tickers

    def first(self, n: int) -> Sequence:
        return self._all_tickers[:n]

    def slice(self, start: int, end: int) -> Sequence:
        return self._all_tickers[start:end]

    def filter(self, predicate) -> Sequence:
        return [t for t in self._all_tickers if predicate(t)]

    def refresh(self, api: QKApi | None = None):
        if api is not None:
            self.api = api
        self._all_tickers = self.TicketLoader.for_api(
            api=self.api,
            exchange=self.exchange
        )
