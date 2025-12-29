# engine/app_controller.py

from data.QK_data_manager import QKHistoricalData
from strategies.QK_strategy_manager import StrategyManager


class AppController:
    """
    Central application orchestrator.
    Owns the execution flow:
    UI → Data → Indicators → Strategies → DataFrame
    """

    def __init__(
        self,
        data_manager: QKHistoricalData,
        strategy_manager: StrategyManager,
    ):
        self.data_manager = data_manager
        self.strategy_manager = strategy_manager

    def run_pipeline(
        self,
        *,
        api_info: dict,
        fetch_config: dict,
        indicator,
        strategy,
    ):
        # ---------- APPLY FETCH CONFIG ----------
        self.data_manager.set_params(
            from_date=fetch_config["from_date"],
            to_date=fetch_config["to_date"],
            interval=fetch_config["interval"],
            unit=fetch_config["unit"],
            intraday_interval=fetch_config.get("intraday_interval"),
        )

        # ---------- API SWITCH ----------
        self.data_manager.switch_api(api_info["api"])

        # ---------- FETCH ----------
        if fetch_config["mode"] == "intraday":
            df = self.data_manager.fetch_intraday(api_info["ticker"])
        else:
            df = self.data_manager.fetch_historical(api_info["ticker"])

        # ---------- INDICATORS ----------
        if indicator:
            self.strategy_manager._indicator_manager.add(indicator)

        # ---------- STRATEGIES ----------
        if strategy:
            self.strategy_manager.add(strategy)

        # ---------- EXECUTION ----------
        df = self.strategy_manager.run(df)

        return df
