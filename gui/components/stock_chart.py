from datetime import datetime
import matplotlib.dates as mdates

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.components.base.base_ui_component import UIComponent


class StockChartComponent(UIComponent):
    def __init__(self, title="Price Chart"):
        super().__init__()
        self.title = title
        self.df: pd.DataFrame | None = None
        self._canvas: FigureCanvasTkAgg | None = None
        self._ax = None

    # ---------- BUILD ----------

    def build(self, parent: tk.Widget):
        frame = tk.LabelFrame(parent, text=self.title)
        self.widget = frame

        fig, ax = plt.subplots(figsize=(7, 4))
        self._ax = ax

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self._canvas = canvas
        if self.df is not None:
            self._redraw()

        return frame

    # ---------- DATA ----------

    def set_data(self, df):
        self.df = df
        if self._ax is not None and self._canvas is not None:
            self._redraw()

    # ---------- RENDER ----------

    def _redraw(self):
        if self.df is None or self._ax is None:
            return

        ax = self._ax
        ax.clear()

        required = {"timestamp", "open", "high", "low", "close"}
        if not required.issubset(self.df.columns):
            ax.text(0.5, 0.5, "Missing OHLC data", ha="center", va="center")
            self._canvas.draw()
            return

        df = self.df.copy()

        # Ensure datetime
        if not isinstance(df["timestamp"].iloc[0], datetime):
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        dates = mdates.date2num(df["timestamp"])

        for i in range(len(df)):
            o = df["open"].iloc[i]
            h = df["high"].iloc[i]
            l = df["low"].iloc[i]
            c = df["close"].iloc[i]

            color = "green" if c >= o else "red"

            # Wick
            ax.plot([dates[i], dates[i]], [l, h], color=color, linewidth=1)

            # Body
            ax.bar(
                dates[i],
                abs(c - o),
                bottom=min(o, c),
                width=0.6,
                color=color,
                align="center",
            )

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        ax.set_title("Candlestick Chart")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.grid(True, alpha=0.3)

        self._canvas.draw()

    # ---------- CONTRACT ----------

    def get_value(self):
        return None  # renderer-only component
