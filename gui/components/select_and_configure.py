import tkinter as tk
from typing import Callable

from gui.components.base.base_ui_component import UIComponent
from gui.components.param_input import ParamInputComponent
from gui.components.param_spec import ParamSpec


class SelectAndConfigure(UIComponent):
    """
    Generic dropdown + param form switcher.
    """

    def __init__(
        self,
        title: str,
        registry: dict[str, tuple[Callable, list[ParamSpec]]],
    ):
        super().__init__()
        self.title = title
        self.registry = registry

        self._selected_name = tk.StringVar()
        self._param_components: dict[str, ParamInputComponent] = {}
        self._active_form: ParamInputComponent | None = None

    # ---------- BUILD ----------

    def build(self, parent: tk.Widget):
        frame = tk.LabelFrame(parent, text=self.title)
        self.widget = frame

        # ---- Dropdown ----
        top = tk.Frame(frame)
        top.pack(fill="x", pady=4)

        options = list(self.registry.keys())
        self._selected_name.set(options[0])

        dropdown = tk.OptionMenu(
            top,
            self._selected_name,
            *options,
            command=self._on_select,
        )
        dropdown.pack(fill="x", expand=True)

        # ---- Param Forms ----
        for name, (_, specs) in self.registry.items():
            form = ParamInputComponent(specs, title=name)
            self._param_components[name] = form

        self._form_container = tk.Frame(frame)
        self._form_container.pack(fill="x")

        # Build + show first
        self._show_form(options[0])

        return frame

    # ---------- EVENTS ----------

    def _on_select(self, name: str):
        self._show_form(name)

    def _show_form(self, name: str):
        if self._active_form:
            self._active_form.widget.pack_forget()

        form = self._param_components[name]
        if not form.widget:
            form.build(self._form_container)

        form.widget.pack(fill="x")
        self._active_form = form

    # ---------- DATA ----------

    def get_value(self):
        if not self._active_form:
            return None

        name = self._selected_name.get()
        ctor, _ = self.registry[name]

        params = self._active_form.get_value()
        return ctor(**params)
