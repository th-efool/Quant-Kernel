# gui/components/base.py
from abc import ABC, abstractmethod
import tkinter as tk


class UIComponent(ABC):
    def __init__(self):
        self.visible = True
        self.widget: tk.Widget | None = None

    @abstractmethod
    def build(self, parent: tk.Widget):
        """
        Create tkinter widget(s).
        Must assign self.widget.
        """
        pass

    def show(self):
        self.visible = True
        if self.widget:
            self.widget.tkraise()

    def hide(self):
        self.visible = False
        if self.widget:
            self.widget.lower()

    @abstractmethod
    def get_value(self):
        pass

