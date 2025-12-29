from datetime import datetime

import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from strategies.base.signal_type import Signal
from gui.components.base.base_ui_component import UIComponent


PRICE_COLUMNS = {
    "open", "high", "low", "close", "adjclose", "volume", "timestamp"
}


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
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

        self._canvas = canvas

        if self.df is not None:
            self._redraw()

        return frame

    # ---------- DATA ----------

    def set_data(self, df: pd.DataFrame):
        self.df = df
        if self._ax is not None and self._canvas is not None:
            self._redraw()

    # ---------- SCALE ROUTING ----------

    def _indicator_scale(self, name: str) -> str:
        """
        Decide which Y-axis an indicator belongs to.
        """
        lname = name.lower()
        if "pct" in lname or "percent" in lname or "range" in lname:
            return "secondary"
        return "primary"

    # ---------- RENDER ----------

    def _redraw(self):
        if self.df is None or self._ax is None:
            return

        ax_price = self._ax
        ax_price.clear()
        ax_secondary = ax_price.twinx()

        df = self.df.copy()

        # ---- EMPTY DF SAFETY ----
        if df.empty:
            ax_price.text(
                0.5, 0.5,
                "No data available",
                ha="center",
                va="center",
                transform=ax_price.transAxes,
            )
            self._canvas.draw()
            return

        # ---- REQUIRED COLUMNS ----
        required = {"timestamp", "open", "high", "low", "close"}
        if not required.issubset(df.columns):
            ax_price.text(
                0.5, 0.5,
                "Missing OHLC data",
                ha="center",
                va="center",
                transform=ax_price.transAxes,
            )
            self._canvas.draw()
            return

        # ---- TIMESTAMP NORMALIZATION ----
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        if df.empty:
            ax_price.text(
                0.5, 0.5,
                "Invalid timestamps",
                ha="center",
                va="center",
                transform=ax_price.transAxes,
            )
            self._canvas.draw()
            return

        dates = mdates.date2num(df["timestamp"])

        # ---------- CANDLESTICKS ----------

        for i in range(len(df)):
            o = df["open"].iloc[i]
            h = df["high"].iloc[i]
            l = df["low"].iloc[i]
            c = df["close"].iloc[i]

            color = "green" if c >= o else "red"

            # Wick
            ax_price.plot(
                [dates[i], dates[i]],
                [l, h],
                color=color,
                linewidth=1,
            )

            # Body
            ax_price.bar(
                dates[i],
                abs(c - o),
                bottom=min(o, c),
                width=0.6,
                color=color,
                align="center",
            )

        # ---------- INDICATOR OVERLAYS ----------

        for col in df.columns:
            series = df[col]

            if not self._is_indicator_column(col, series):
                continue

            target_ax = (
                ax_secondary
                if self._indicator_scale(col) == "secondary"
                else ax_price
            )

            target_ax.plot(
                df["timestamp"],
                series,
                label=col,
                linewidth=1.2,
                linestyle="--" if target_ax is ax_secondary else "-",
                alpha=0.85,
            )

        # ---------- STRATEGY SIGNALS ----------

        for col in df.columns:
            series = df[col]

            if not self._is_signal_column(series):
                continue

            buy_idx = series == Signal.BUY
            sell_idx = series == Signal.SELL

            ax_price.scatter(
                df.loc[buy_idx, "timestamp"],
                df.loc[buy_idx, "close"],
                marker="^",
                s=90,
                color="green",
                zorder=5,
                label=f"{col} BUY",
            )

            ax_price.scatter(
                df.loc[sell_idx, "timestamp"],
                df.loc[sell_idx, "close"],
                marker="v",
                s=90,
                color="red",
                zorder=5,
                label=f"{col} SELL",
            )

        # ---------- AXIS CONFIG ----------

        ax_price.set_title("Candlestick Chart")
        ax_price.set_xlabel("Date")
        ax_price.set_ylabel("Price / MA / VWAP")
        ax_secondary.set_ylabel("Percent / Ratio")

        ax_price.xaxis_date()
        ax_price.xaxis.set_major_formatter(
            mdates.DateFormatter("%Y-%m-%d")
        )

        ax_price.grid(True, alpha=0.3)

        # ---------- LEGEND (BOTH AXES) ----------

        h1, l1 = ax_price.get_legend_handles_labels()
        h2, l2 = ax_secondary.get_legend_handles_labels()

        handles = h1 + h2
        labels = l1 + l2

        if labels:
            ax_price.legend(
                handles,
                labels,
                loc="upper left",
                fontsize=8,
            )

        ax_price.figure.autofmt_xdate()
        self._canvas.draw()

    # ---------- CONTRACT ----------

    def get_value(self):
        return None  # renderer-only component

    # ---------- HELPERS ----------

    def _is_indicator_column(self, name: str, series: pd.Series) -> bool:
        if name in PRICE_COLUMNS:
            return False
        if not pd.api.types.is_numeric_dtype(series):
            return False
        return True

    def _is_signal_column(self, series: pd.Series) -> bool:
        if series.dtype != object:
            return False
        return series.isin([Signal.BUY, Signal.SELL]).any()
