
# gui/layout/base.py
from abc import ABC, abstractmethod
import tkinter as tk
from gui.components.base.base_ui_component import UIComponent


class LayoutContainer(ABC):
    def __init__(self):
        self.children: list[UIComponent | "LayoutContainer"] = []

    def add(self, child):
        self.children.append(child)
        return self

    @abstractmethod
    def build(self, parent: tk.Widget):
        pass
