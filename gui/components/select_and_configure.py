import tkinter as tk
from gui.components.base.base_ui_component import UIComponent
from gui.components.param_input import ParamInputComponent


class SelectAndConfigure(UIComponent):
    """
    Dropdown selector + parameter form builder.
    Emits change events when selection changes.
    """

    def __init__(self, title: str, registry: dict):
        super().__init__()
        self.title = title
        self.registry = registry  # name -> (cls, [ParamSpec])

        self._active_cls = None
        self._active_form = None

        # 🔥 REQUIRED for AddToListComponent
        self._on_change_callbacks = []

        self._var = None
        self._form_container = None

    # ---------- PUBLIC API ----------

    def has_selection(self) -> bool:
        return self._active_cls is not None

    def on_change(self, callback):
        self._on_change_callbacks.append(callback)

    def get_value(self):
        if self._active_cls is None or self._active_form is None:
            return None

        params = self._active_form.get_value()
        return self._active_cls(**params)

    # ---------- BUILD ----------

    def build(self, parent):
        frame = tk.LabelFrame(parent, text=self.title)
        self.widget = frame

        options = list(self.registry.keys())

        self._var = tk.StringVar(value="Select…")

        dropdown = tk.OptionMenu(
            frame,
            self._var,
            *options,
            command=self._on_select,   # 🔥 THIS IS THE DROPDOWN
        )
        dropdown.pack(fill="x", pady=4)

        self._form_container = tk.Frame(frame)
        self._form_container.pack(fill="x")

        return frame

    # ---------- INTERNAL ----------

    def _on_select(self, choice: str):
        # clear old form
        for child in self._form_container.winfo_children():
            child.destroy()

        cls, specs = self.registry[choice]
        self._active_cls = cls

        self._active_form = ParamInputComponent(
            specs=specs,
            title=f"{choice} Params",
        )
        # 🔥 THIS WAS MISSING
        form_widget = self._active_form.build(self._form_container)
        form_widget.pack(fill="x", pady=4)

        # 🔥 NOTIFY LISTENERS (THIS WAS MISSING)
        for cb in self._on_change_callbacks:
            cb()
