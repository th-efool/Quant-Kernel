from typing import Iterable
from core.common_types import QKApi, QKDate, Unit
from data.APIs.historical_data.data_fetcher_base import DataFetcherBase
from data.APIs.historical_data.dhan_fetcher import DhanFetcher
from data.APIs.historical_data.upstox_fetcher import UpstoxFetcher
from data.APIs.historical_data.yfinance_fetcher import YahooFetcher
from data.APIs.ticker_symbols.ticker_manager import TickerManager
from typing import assert_never


class QKHistoricalData:
    def __init__(
        self,
        api: QKApi = QKApi.yfinance,
        from_date=None,
        to_date=None,
        interval: str = "1d",
        unit: Unit = Unit.days,
        intraday_interval: int = 1,
        exchange: str = "NSE",
    ):
        self.api = api
        self.from_date = from_date or QKDate.days_ago(30)
        self.to_date = to_date or QKDate.yesterday()

        self.interval = interval
        self.unit = unit
        self.intraday_interval = intraday_interval

        self.fetcher: DataFetcherBase = self._get_fetcher(api)
        self.tickers = TickerManager(api=api, exchange=exchange)

    # ---------------- API SWITCH ----------------

    def switch_api(self, new_api: QKApi) -> None:
        if new_api == self.api:
            return

        self.api = new_api
        self.fetcher = self._get_fetcher(new_api)
        self.tickers.refresh(api=new_api)

    # ---------------- FETCHER ----------------

    def _get_fetcher(self, api: QKApi) -> DataFetcherBase:
        match api:
            case QKApi.yfinance:
                return YahooFetcher()
            case QKApi.upstox:
                return UpstoxFetcher()
            case QKApi.dhan:
                return DhanFetcher()
            case _:
                assert_never(api)

    # ---------------- DATA MANAGER API ----------------

    def getHistoricalData(
        self,
        tickers: Iterable,
    ) -> dict:
        """
        Fetch historical data for multiple tickers.
        Returns: { ticker: Iterable[QKCandle] }
        """
        results = {}

        for ticker in tickers:
            try:
                candles = self.fetcher._fetch_historical(
                    symbol=ticker,
                    start=self.from_date,
                    end=self.to_date,
                    interval=self.interval,
                )
                results[ticker] = candles
            except Exception as e:
                results[ticker] = e

        return results

    def getIntradayData(
        self,
        tickers: Iterable,
    ) -> dict:
        """
        Fetch intraday data for multiple tickers.
        Returns: { ticker: Iterable[QKCandle] }
        """
        results = {}

        for ticker in tickers:
            try:
                candles = self.fetcher._fetch_intraday(
                    symbol=ticker,
                    unit=self.unit,
                    interval=self.intraday_interval,
                )
                results[ticker] = candles
            except Exception as e:
                results[ticker] = e

        return results
