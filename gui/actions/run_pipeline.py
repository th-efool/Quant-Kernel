# gui/actions/run_pipeline.py
from core.common_types import TickerSource
from data.ticker_symbols.ticker_loader import TickerLoader


def run_pipeline_action(controller, ui_refs):
    """
    Reads UI state, executes pipeline, updates chart.
    """

    api_info = ui_refs["api_config"].get_value()
    if not api_info:
        print("No API selected")
        return

    fetch_config = ui_refs["fetch_config"].get_value()
    indicators = ui_refs["indicators"].get_value()
    strategies = ui_refs["strategies"].get_value()

    api = api_info["api"]
    exchange = api_info["exchange"]
    max_tickers = api_info["max_tickers"]

    # ---------- RESOLVE TICKERS ----------
    loader = TickerLoader(TickerSource.INDIA)
    start = api_info["start_index"]
    end = api_info["end_index"]

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
    # 🔥 CLEAR ALL OLD CHARTS
    chart_view.clear()

    # ---------- RUN PER TICKER ----------
    for ticker in tickers:
        df = controller.run_pipeline(
            api=api,
            ticker=ticker,
            fetch_config=fetch_config,
            indicators=indicators,
            strategies=strategies,
        )

        chart_view.append_data(
            ticker=ticker,
            df=df,
        )

