import tkinter as tk

from data.QK_data_manager import QKHistoricalData
from strategies.QK_strategy_manager import StrategyManager
from gui.QKRenderer import QKRenderer

from gui.layout.column import Column
from gui.components.param_input import ParamInputComponent
from gui.components.param_spec import ParamSpec
from gui.components.collapsible_panel import CollapsiblePanel

from core.common_types import Unit
from indicators.base.indicator_type import IndicatorType
from strategies.strategy_ma_crossover import MACrossoverStrategy

TheDataManager = QKHistoricalData()
TheStrategyManager = StrategyManager()
Renderer = QKRenderer(title="QK UI Test", size=(900, 700))

api_config = ParamInputComponent(
    specs=[
        ParamSpec("api_name", str),
        ParamSpec("client_id", str),
        ParamSpec("secret_key", str),
    ],
    title="API Config"
)

fetch_config = ParamInputComponent(
    specs=[
        ParamSpec("mode", str, default="historical"),  # or Enum later
        ParamSpec("interval", int, default=1),
        ParamSpec("intraday_interval", int, optional=True),
        ParamSpec("from_date", str),
        ParamSpec("to_date", str),
        ParamSpec("unit", Unit, default=Unit.days),

    ],
    title="Fetch Config"
)

indicator_params = ParamInputComponent(
    specs=[
        ParamSpec("period", int),
    ],
    title="Moving Average Params"
)

indicator_panel = CollapsiblePanel(
    title="Add Indicator (MA)",
    content=indicator_params,
    start_open=False,
)

strategy_params = ParamInputComponent(
    specs=[
        ParamSpec("fast", int),
        ParamSpec("slow", int),
    ],
    title="MA Crossover Strategy"
)

strategy_panel = CollapsiblePanel(
    title="Add Strategy (MA Crossover)",
    content=strategy_params,
    start_open=False,
)


def run_pipeline():
    print("\n===== UI STATE =====")

    api_vals = api_config.get_value()
    fetch_vals = fetch_config.get_value()
    ind_vals = indicator_panel.get_value()
    strat_vals = strategy_panel.get_value()

    print("API:", api_vals)
    print("FETCH:", fetch_vals)
    print("INDICATOR:", ind_vals)
    print("STRATEGY:", strat_vals)

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

    ticker = "3MINDIA.NS"

    if fetch_mode == "intraday":
        print("[FETCH MODE] Intraday")
        df = TheDataManager.fetch_intraday(ticker)
    else:
        print("[FETCH MODE] Historical")
        df = TheDataManager.fetch_historical(ticker)

    print("DF SHAPE:", df.shape)

    # ---------------- STRATEGY (OPTIONAL) ----------------

    if strat_vals:
        TheStrategyManager.add(
            MACrossoverStrategy(**strat_vals)
        )

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
    layout.add(api_config)
    layout.add(fetch_config)
    layout.add(indicator_panel)
    layout.add(strategy_panel)
    layout.add(RunButton())

    Renderer.set_layout(layout)
    Renderer.run()
