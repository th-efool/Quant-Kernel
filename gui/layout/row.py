# gui/layout/row.py
import tkinter as tk
from gui.layout.base.base_layout_container import LayoutContainer


class Row(LayoutContainer):
    def __init__(self, spacing=8):
        super().__init__()
        self.spacing = spacing

    def build(self, parent: tk.Widget):
        frame = tk.Frame(parent)
        self.widget = frame  # 🔥 THIS LINE FIXES EVERYTHING
        frame.pack(fill="both", expand=True)

        for child in self.children:
            if hasattr(child, "build"):
                child.build(frame)

            widget = getattr(child, "widget", None)
            if widget:
                widget.pack(
                    side="top",
                    fill="x",
                    pady=self.spacing
                )

        return frame


