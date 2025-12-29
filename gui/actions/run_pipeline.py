# gui/actions/run_pipeline.py
# gui/actions/run_pipeline.py

import threading
from core.common_types import TickerSource
from data.ticker_symbols.ticker_loader import TickerLoader


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
