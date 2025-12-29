# gui/views/main_view.py

import tkinter as tk

from gui.layout.column import Column
from gui.components.api_selector import ApiTickerSelector
from gui.components.stock_chart import StockChartComponent
from gui.components.select_and_configure import SelectAndConfigure
from gui.components.param_spec import ParamSpec

from indicators.indicator_moving_average import MovingAverage
from indicators.indicator_vwap import VWAP
from indicators.indicator_day_range_percentage import DayRangePct
from indicators.indicator_mcginley import McGinleyDynamic

from strategies.strategy_ma_crossover import MACrossoverStrategy
from strategies.strategy_vwap_crossover import VWAPCrossoverStrategy
from strategies.strategy_day_range_breakout import DayRangeBreakoutStrategy

from core.common_types import Unit
from gui.components.param_input import ParamInputComponent


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
    api_selector = ApiTickerSelector()

    fetch_config = ParamInputComponent(
        specs=[
            ParamSpec("mode", str, default="historical"),
            ParamSpec("interval", int, default=1),
            ParamSpec("intraday_interval", int, optional=True),
            ParamSpec("from_date", str),
            ParamSpec("to_date", str),
            ParamSpec("unit", Unit, default=Unit.days),
        ],
        title="Fetch Config",
    )

    indicator_selector = SelectAndConfigure(
        title="Add Indicator",
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

    chart = StockChartComponent(title="Market Chart")
    run_button = RunButton(on_run_callback)

    layout = Column(spacing=12)
    layout.add(api_selector)
    layout.add(fetch_config)
    layout.add(indicator_selector)
    layout.add(strategy_selector)
    layout.add(run_button)
    layout.add(chart)

    ui_refs = {
        "api_selector": api_selector,
        "fetch_config": fetch_config,
        "indicator_selector": indicator_selector,
        "strategy_selector": strategy_selector,
        "chart": chart,
    }

    return layout, ui_refs
