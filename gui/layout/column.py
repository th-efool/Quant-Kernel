# gui/layout/column.py
import tkinter as tk
from gui.layout.base.base_layout_container import LayoutContainer


class Column(LayoutContainer):
    def __init__(self, spacing=8):
        super().__init__()
        self.spacing = spacing

    def build(self, parent: tk.Widget):
        frame = tk.Frame(parent)
        self.widget = frame  # 🔥 consistency
        frame.pack(fill="x", expand=True)

        for child in self.children:
            if hasattr(child, "build"):
                child.build(frame)

            widget = getattr(child, "widget", None)
            if widget:
                widget.pack(
                    side="left",
                    padx=self.spacing,
                    fill="both",
                    expand=True
                )

        return frame

