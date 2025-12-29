# gui/components/collapsible_panel.py
import tkinter as tk

from gui.components.base.base_ui_component import UIComponent


class CollapsiblePanel(UIComponent):
    def __init__(self, title: str, content: UIComponent, start_open=True):
        super().__init__()
        self.title = title
        self.content = content
        self.open = start_open

    def build(self, parent: tk.Widget):
        container = tk.Frame(parent)
        self.widget = container

        header = tk.Button(
            container,
            text=self._header_text(),
            anchor="w",
            command=self.toggle,
        )
        header.pack(fill="x")

        self._content_frame = tk.Frame(container)
        self.content.build(self._content_frame)

        if self.open:
            self._content_frame.pack(fill="x")

        self._header = header
        return container

    def toggle(self):
        self.open = not self.open

        if self.open:
            self._content_frame.pack(fill="x")
        else:
            self._content_frame.forget()

        self._header.config(text=self._header_text())

    def _header_text(self):
        return ("▼ " if self.open else "▶ ") + self.title

    def get_value(self):
        if not self.open:
            return None
        return self.content.get_value()
