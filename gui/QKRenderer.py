# gui/QKRenderer.py
import tkinter as tk
from gui.layout.base.base_layout_container import LayoutContainer


class QKRenderer:
    def __init__(self, title="Quant Kernel", size=(1200, 800)):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.layout: LayoutContainer | None = None

    def set_layout(self, layout: LayoutContainer):
        self.layout = layout

    def run(self):
        if not self.layout:
            raise RuntimeError("Renderer has no layout")

        self.layout.build(self.root)
        self.root.mainloop()
