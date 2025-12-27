from typing import Iterable, Sequence
from core.CommonTypes import QKApi
from data.APIs.ticker_symbols.loader import load_tickers_for_api


class TickerManager:
    def __init__(self, api: QKApi, exchange: str = "NSE"):
        self.api = api
        self.exchange = exchange
        self._all_tickers = load_tickers_for_api(api=api, exchange=exchange)

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
        self._all_tickers = load_tickers_for_api(
            api=self.api,
            exchange=self.exchange
        )
