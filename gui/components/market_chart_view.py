import tkinter as tk

from gui.components.base.base_ui_component import UIComponent
from gui.components.stock_chart import StockChartComponent


class MarketChartView(UIComponent):
    def __init__(self):
        super().__init__()
        self._charts = {}  # ticker -> SingleTickerChart

    def build(self, parent):
        frame = tk.Frame(parent)
        self.widget = frame

        self.canvas = tk.Canvas(frame)
        self.scrollbar = tk.Scrollbar(
            frame, orient="vertical", command=self.canvas.yview
        )

        self.inner = tk.Frame(self.canvas)

        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        return frame

    # ---------- REQUIRED BY UIComponent ----------

    def get_value(self):
        """
        Renderer-only component.
        Does not participate in pipeline input.
        """
        return None

    # ---------- API ----------

    def clear(self):
        for chart in self._charts.values():
            chart.widget.destroy()
        self._charts.clear()

    def append_data(self, *, ticker: str, df):
        chart = StockChartComponent(title=ticker)
        chart.build(self.inner)

        # 🔥 THIS WAS MISSING
        chart.widget.pack(
            fill="x",
            expand=True,
            padx=8,
            pady=8,
        )
        chart.set_data(df)
        self._charts[ticker] = chart
