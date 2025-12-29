import tkinter as tk

from data.QK_data_manager import QKHistoricalData
from strategies.QK_strategy_manager import StrategyManager
from gui.QKRenderer import QKRenderer
from gui.components.stock_chart import StockChartComponent
from gui.components.select_and_configure import SelectAndConfigure
from indicators.indicator_moving_average import MovingAverage
from indicators.indicator_vwap import VWAP
from strategies.strategy_day_range_breakout import DayRangeBreakoutStrategy
from gui.components.select_and_configure import SelectAndConfigure
from gui.components.param_spec import ParamSpec
from strategies.strategy_ma_crossover import MACrossoverStrategy
from strategies.strategy_day_range_breakout import DayRangeBreakoutStrategy
from strategies.strategy_vwap_crossover import VWAPCrossoverStrategy

from indicators.indicator_moving_average import MovingAverage
from indicators.indicator_vwap import VWAP
from indicators.indicator_day_range_percentage import DayRangePct
from indicators.indicator_mcginley import McGinleyDynamic

from gui.layout.column import Column
from gui.components.param_input import ParamInputComponent
from gui.components.param_spec import ParamSpec
from gui.components.collapsible_panel import CollapsiblePanel
from gui.components.api_selector import ApiTickerSelector

from core.common_types import Unit
from indicators.base.indicator_type import IndicatorType
from strategies.strategy_ma_crossover import MACrossoverStrategy

TheDataManager = QKHistoricalData()
TheStrategyManager = StrategyManager()
Renderer = QKRenderer(title="QK UI Test", size=(900, 700))

api_selector = ApiTickerSelector()

api_config = ParamInputComponent(
    specs=[
        ParamSpec("api_name", str),
        ParamSpec("client_id", str),
        ParamSpec("secret_key", str),
    ],
    title="API Config"
)

chart = StockChartComponent(title="Market Chart")

fetch_config = ParamInputComponent(
    specs=[
        ParamSpec("mode", str, default="historical"),  # or Enum later
        ParamSpec("interval", int, default=1),
        ParamSpec("intraday_interval", int, optional=True),
        ParamSpec("from_date", str, default='2024-12-01'),
        ParamSpec("to_date", str, default='2024-12-24'),
        ParamSpec("unit", Unit, default=Unit.days),

    ],
    title="Fetch Config"
)

indicator_selector = SelectAndConfigure(
    title="Add Indicator",
    registry={
        "Moving Average": (
            MovingAverage,
            [
                ParamSpec("period", int),
            ],
        ),

        "VWAP": (
            VWAP,
            [
                ParamSpec("days", int),   # 🔥 THIS WAS MISSING
            ],
        ),

        "Day Range %": (
            DayRangePct,
            [],  # no params
        ),

        "McGinley Dynamic": (
            McGinleyDynamic,
            [
                ParamSpec("period", int, default=14),
                ParamSpec("source", str, default="close"),
                ParamSpec("k", float, default=0.6),
            ],
        ),
    },
)


strategy_selector = SelectAndConfigure(
    title="Add Strategy",
    registry={
        "MA Crossover": (
            MACrossoverStrategy,
            [
                ParamSpec("fast", int),
                ParamSpec("slow", int),
            ],
        ),

        "VWAP Crossover": (
            VWAPCrossoverStrategy,
            [
                ParamSpec("fast_days", int),
                ParamSpec("slow_days", int),
            ],
        ),

        "Day Range Breakout": (
            DayRangeBreakoutStrategy,
            [
                ParamSpec("threshold", float, default=0.05),
            ],
        ),
    },
)




def run_pipeline():
    print("\n===== UI STATE =====")

    api_vals = api_config.get_value()
    fetch_vals = fetch_config.get_value()
    indicator = indicator_selector.get_value()
    strategy = strategy_selector.get_value()

    print("API:", api_vals)
    print("FETCH:", fetch_vals)
    print("INDICATOR:", indicator)
    print("STRATEGY:", strategy)

    # ---------------- APPLY FETCH CONFIG ----------------

    fetch_mode = fetch_vals["mode"]  # <── HERE. THIS LINE.

    TheDataManager.set_params(
        from_date=fetch_vals["from_date"],
        to_date=fetch_vals["to_date"],
        interval=fetch_vals["interval"],
        unit=fetch_vals["unit"],
        intraday_interval=fetch_vals.get("intraday_interval"),
    )

    # ---------------- FETCH DATA (TEST ONLY) ----------------
    # using a dummy ticker for now
    api_ticker = api_selector.get_value()
    if not api_ticker:
        print("No API / Ticker selected")
        return

    selected_api = api_ticker["api"]
    ticker = api_ticker["ticker"]
    TheDataManager.switch_api(selected_api)


    if fetch_mode == "intraday":
        print("[FETCH MODE] Intraday")
        df = TheDataManager.fetch_intraday(ticker)
    else:
        print("[FETCH MODE] Historical")
        df = TheDataManager.fetch_historical(ticker)

    print("DF SHAPE:", df.shape)

    # ---------------- STRATEGY (OPTIONAL) ----------------

    if indicator:
        TheStrategyManager._indicator_manager.add(indicator)

    if strategy:
        TheStrategyManager.add(strategy)
    TheStrategyManager._indicator_manager.run(df)
    TheStrategyManager.run(df)

    chart.set_data(df)

    # Just proving the pipeline works
    print("PIPELINE OK")


class RunButton:
    def build(self, parent):
        self.widget = tk.Button(
            parent,
            text="RUN PIPELINE",
            command=run_pipeline,
            height=2,
            bg="#222",
            fg="white",
        )


if __name__ == "__main__":
    layout = Column(spacing=12)
    layout.add(api_selector)
    layout.add(fetch_config)
    layout.add(indicator_selector)
    layout.add(strategy_selector)
    layout.add(RunButton())
    layout.add(chart)

    Renderer.set_layout(layout)
    Renderer.run()
