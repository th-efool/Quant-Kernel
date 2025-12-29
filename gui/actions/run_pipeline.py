# gui/actions/run_pipeline.py
# gui/actions/run_pipeline.py

import threading
from core.common_types import TickerSource
from data.ticker_symbols.ticker_loader import TickerLoader
from strategies.base.signal_type import Signal
import pandas as pd


def run_pipeline_action(controller, ui_refs):
    """
    Reads UI state, executes pipeline incrementally,
    updates chart without blocking Tkinter.
    """

    # ---------- READ UI STATE ----------
    api_info = ui_refs["api_config"].get_value()
    if not api_info:
        print("No API selected")
        return

    fetch_config = ui_refs["fetch_config"].get_value()
    indicators = ui_refs["indicators"].get_value()
    strategies = ui_refs["strategies"].get_value()

    enable_filter = api_info.get("enable_filter", False)
    filter_last_n = api_info.get("filter_last_n", 0)

    api = api_info["api"]
    exchange = api_info["exchange"]
    start = api_info["start_index"]
    end = api_info["end_index"]

    # ---------- RESOLVE TICKERS ----------
    loader = TickerLoader(TickerSource.INDIA)
    tickers = loader.get_tickers(
        api=api,
        exchange=exchange,
        start=start,
        end=end,
    )

    def passes_signal_filter(
            df: pd.DataFrame,
            *,
            last_n: int
    ) -> bool:
        """
        Returns True if, in the last `n` candles,
        ALL strategy signal columns contain ONLY BUY or HOLD.
        """
        if last_n <= 0:
            return True

        tail = df.tail(last_n)

        for col in df.columns:
            series = df[col]

            # signal columns only
            if series.dtype != object:
                continue

            if not series.isin([Signal.BUY, Signal.SELL, Signal.HOLD]).any():
                continue

            values = tail[col].dropna().unique()

            # ❌ reject if ANY SELL appears
            if Signal.HOLD in values:
                return False

        return True

    if not tickers:
        print("No tickers resolved")
        return

    chart_view = ui_refs["chart"]

    # 🔥 Clear previous charts (logical reset, not destruction)
    chart_view.clear()

    # ---------- BACKGROUND WORKER ----------
    def worker():
        for ticker in tickers:
            try:
                df = controller.run_pipeline(
                    api=api,
                    ticker=ticker,
                    fetch_config=fetch_config,
                    indicators=indicators,
                    strategies=strategies,
                )

                if enable_filter:
                    if not passes_signal_filter(df, last_n=filter_last_n):
                        continue  # 🔥 skip rendering

                # 🔁 Marshal UI update to main thread
                chart_view.widget.after(
                    0,
                    lambda t=ticker, d=df: chart_view.append_data(
                        ticker=t,
                        df=d,
                    )
                )

            except Exception as e:
                print(f"[ERROR] Failed for {ticker}: {e}")

    # ---------- START THREAD ----------
    threading.Thread(
        target=worker,
        daemon=True,
    ).start()
