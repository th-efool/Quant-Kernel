# app.py

from gui.QKRenderer import QKRenderer
from gui.views.main_view import build_main_view
from gui.actions.run_pipeline import run_pipeline_action
from app_controller import AppController

from data.QK_data_manager import QKHistoricalData
from strategies.QK_strategy_manager import StrategyManager


def main():
    data_mgr = QKHistoricalData()
    strategy_mgr = StrategyManager()
    controller = AppController(data_mgr, strategy_mgr)

    renderer = QKRenderer(title="Quant Kernel", size=(1800, 600))

    layout, ui_refs = build_main_view(
        on_run_callback=lambda: run_pipeline_action(controller, ui_refs)
    )

    renderer.set_layout(layout)
    renderer.run()


if __name__ == "__main__":
    main()
