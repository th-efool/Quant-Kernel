# gui/layout/panel.py
import tkinter as tk
from gui.layout.base.base_layout_container import LayoutContainer


class Panel(LayoutContainer):
    def __init__(self, width=None, height=None):
        super().__init__()
        self.width = width
        self.height = height

    def build(self, parent: tk.Widget):
        frame = tk.Frame(parent, width=self.width, height=self.height)
        frame.pack_propagate(False)
        frame.pack(side="left", fill="y")

        for child in self.children:
            child.build(frame)
            child.widget.pack(fill="x")

        return frame
