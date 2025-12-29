from typing import Iterable
from core.common_types import QKApi, QKDate, Unit
from data.historical_data.base.data_fetcher_base import DataFetcherBase
from data.historical_data.fetcher_dhan import DhanFetcher
from data.historical_data.fetcher_upstox import UpstoxFetcher
from data.historical_data.fetcher_yfinance import YahooFetcher
from data.ticker_symbols.QK_ticker_manager import TickerManager
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

    # ---------------- CONFIG ----------------

    def set_params(
        self,
        *,
        api: QKApi | None = None,
        from_date=None,
        to_date=None,
        interval: str | None = None,
        unit: Unit | None = None,
        intraday_interval: int | None = None,
        exchange: str | None = None,
    ):
        if api is not None:
            self.api = api
            self.switch_api(api)

        if from_date is not None:
            self.from_date = from_date

        if to_date is not None:
            self.to_date = to_date

        if interval is not None:
            self.interval = interval

        if unit is not None:
            self.unit = unit

        if intraday_interval is not None:
            self.intraday_interval = intraday_interval

        if exchange is not None:
            self.exchange = exchange

        return self


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

    # ---------------- FETCHERS ----------------

    def fetch_historical(self, ticker: str):
        return self.fetcher.fetch_df(
            symbol=ticker,
            intraday=False,
            start=self.from_date,
            end=self.to_date,
            unit=self.unit,
            interval=self.interval,
        )

    def fetch_intraday(self, ticker: str):
        return self.fetcher.fetch_df(
            symbol=ticker,
            intraday=True,
            start=None,
            end=None,
            unit=self.unit,
            interval=self.intraday_interval,
        )
