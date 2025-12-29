# gui/views/main_view.py

import tkinter as tk

from gui.components.market_chart_view import MarketChartView
from gui.layout.row import Row
from gui.layout.column import Column
from gui.components.api_selector import ApiTickerSelector
from gui.components.stock_chart import StockChartComponent
from gui.components.select_and_configure import SelectAndConfigure
from gui.components.param_spec import ParamSpec
from gui.components.param_input import ParamInputComponent
from gui.components.add_to_list import AddToListComponent



from core.common_types import Unit, QKDate, QKApi
from indicators.indicator_moving_average import MovingAverage
from indicators.indicator_vwap import VWAP
from indicators.indicator_day_range_percentage import DayRangePct
from indicators.indicator_mcginley import McGinleyDynamic
from strategies.strategy_ma_crossover import MACrossoverStrategy
from strategies.strategy_vwap_crossover import VWAPCrossoverStrategy
from strategies.strategy_day_range_breakout import DayRangeBreakoutStrategy

class RunButton:
    def __init__(self, on_click):
        self.on_click = on_click
        self.widget = None

    def build(self, parent):
        self.widget = tk.Button(
            parent,
            text="RUN PIPELINE",
            command=self.on_click,
            height=2,
            bg="#222",
            fg="white",
        )
        return self.widget


def build_main_view(on_run_callback):
    api_config = ParamInputComponent(
        specs=[
            ParamSpec("api", QKApi, default=QKApi.yfinance),
            ParamSpec("exchange", str, default="NSE"),
            ParamSpec("start_index", int, default=0),
            ParamSpec("end_index", int, default=10),

            ParamSpec("enable_filter", bool, default=False),
            ParamSpec("filter_last_n", int, default=5, optional=True),

        ],
        title="API Selection",
    )

    fetch_config = ParamInputComponent(
        specs=[
            ParamSpec("mode", str, default="historical"),
            ParamSpec("interval", int, default=1),
            ParamSpec("intraday_interval", int, optional=True),
            ParamSpec("from_date", str, default=QKDate.days_ago(50).__str__()),
            ParamSpec("to_date", str, default=QKDate.days_ago(1).__str__()),
            ParamSpec("unit", Unit, default=Unit.days),
        ],
        title="Fetch Config",
    )

    indicator_selector_raw = SelectAndConfigure(
        title="Indicator Config",
        registry={
            "Moving Average": (
                MovingAverage,
                [ParamSpec("period", int)],
            ),
            "VWAP": (
                VWAP,
                [ParamSpec("days", int)],
            ),
            "Day Range %": (
                DayRangePct,
                [],
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

    indicator_list = AddToListComponent(
        selector=indicator_selector_raw,
        title="Indicators",
    )

    strategy_selector_raw = SelectAndConfigure(
        title="Strategy Config",
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

    strategy_list = AddToListComponent(
        selector=strategy_selector_raw,
        title="Strategies",
    )


    chart = MarketChartView()

    run_button = RunButton(on_run_callback)

    # ---------- TOP LEFT (API + Fetch) ----------
    top_left = Column(spacing=12)
    top_left.add(api_config)
    top_left.add(fetch_config)
    top_left.add(run_button)

    # ---------- TOP RIGHT (Indicators + Strategies) ----------
    top_right = Column(spacing=12)
    top_right.add(indicator_list)
    top_right.add(strategy_list)

    # ---------- TOP ROW ----------
    top_row = Row(spacing=16)
    top_row.add(top_left)
    top_row.add(top_right)

    # ---------- ROOT LAYOUT ----------
    layout = Column(spacing=16)
    layout.add(top_row)
    layout.add(chart)

    ui_refs = {
        "api_config": api_config,
        "fetch_config": fetch_config,
        "indicators": indicator_list,
        "strategies": strategy_list,
        "chart": chart,
    }

    return layout, ui_refs
