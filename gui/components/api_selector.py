import tkinter as tk
from gui.components.base.base_ui_component import UIComponent
from core.common_types import QKApi



class ApiTickerSelector(UIComponent):
    DEFAULT_TICKERS = {
        QKApi.yfinance: "3MINDIA.NS",
        QKApi.upstox: "NSE_EQ|INE848E01016",
        QKApi.dhan: "360ONE",
    }

    def __init__(self):
        super().__init__()
        self._api_var = tk.StringVar(value=QKApi.yfinance.name)
        self._ticker_var = tk.StringVar()

        # set initial default
        self._ticker_var.set(
            self.DEFAULT_TICKERS[QKApi.yfinance]
        )

    # ---------- BUILD ----------

    def build(self, parent: tk.Widget):
        frame = tk.LabelFrame(parent, text="API & Ticker")
        self.widget = frame

        # ---- API Dropdown ----
        api_row = tk.Frame(frame)
        api_row.pack(fill="x", pady=4)

        tk.Label(api_row, text="API", width=18, anchor="w").pack(side="left")

        api_menu = tk.OptionMenu(
            api_row,
            self._api_var,
            *[api.name for api in QKApi],
            command=self._on_api_change,   # <── IMPORTANT
        )
        api_menu.pack(side="right", fill="x", expand=True)

        # ---- Ticker Input ----
        ticker_row = tk.Frame(frame)
        ticker_row.pack(fill="x", pady=4)

        tk.Label(ticker_row, text="Ticker", width=18, anchor="w").pack(side="left")

        tk.Entry(
            ticker_row,
            textvariable=self._ticker_var,
        ).pack(side="right", fill="x", expand=True)

        return frame

    # ---------- EVENTS ----------

    def _on_api_change(self, api_name: str):
        api = QKApi[api_name]
        default = self.DEFAULT_TICKERS.get(api, "")
        self._ticker_var.set(default)

    # ---------- DATA ----------

    def get_value(self):
        api = QKApi[self._api_var.get()]
        ticker = self._ticker_var.get().strip()

        if not ticker:
            return None

        return {
            "api": api,
            "ticker": ticker,
        }
