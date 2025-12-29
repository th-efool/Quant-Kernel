# gui/layout/row.py
import tkinter as tk
from gui.layout.base.base_layout_container import LayoutContainer


class Row(LayoutContainer):
    def __init__(self, spacing=8):
        super().__init__()
        self.spacing = spacing

    def build(self, parent: tk.Widget):
        frame = tk.Frame(parent)
        frame.pack(fill="x")

        for child in self.children:
            child.build(frame)
            child.widget.pack(
                side="left",
                padx=self.spacing
            )

        return frame
