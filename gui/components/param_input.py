# gui/components/param_input.py
import tkinter as tk
from enum import Enum
from typing import Any

from gui.components.param_spec import ParamSpec

from gui.components.base.base_ui_component import UIComponent

from gui.components.error import InvalidInputFormat


class ParamInputComponent(UIComponent):
    def __init__(self, specs: list[ParamSpec], title: str | None = None):
        super().__init__()
        self.specs = specs
        self.title = title
        self._vars: dict[str, tk.Variable] = {}

    # ---------- BUILD ----------

    def build(self, parent: tk.Widget):
        frame = tk.LabelFrame(parent, text=self.title) if self.title else tk.Frame(parent)
        self.widget = frame

        for spec in self.specs:
            row = tk.Frame(frame)
            row.pack(fill="x", pady=4)

            label = tk.Label(
                row,
                text=f"{spec.name} ({spec.type.__name__})",
                width=22,
                anchor="w",
            )
            label.pack(side="left")

            var = self._make_variable(spec)
            self._vars[spec.name] = var

            widget = self._make_input_widget(row, spec, var)
            widget.pack(side="right", fill="x", expand=True)

        return frame

    # ---------- INPUT TYPES ----------

    def _make_variable(self, spec: ParamSpec) -> tk.Variable:
        if spec.type is bool:
            return tk.BooleanVar(value=bool(spec.default))
        return tk.StringVar(value="" if spec.default is None else str(spec.default))

    def _make_input_widget(
        self,
        parent: tk.Widget,
        spec: ParamSpec,
        var: tk.Variable,
    ):
        if spec.type is bool:
            return tk.Checkbutton(parent, variable=var)

        if issubclass(spec.type, Enum):
            options = [e.name for e in spec.type]
            var.set(options[0])
            return tk.OptionMenu(parent, var, *options)

        return tk.Entry(parent, textvariable=var)

    # ---------- DATA EXTRACTION ----------

    def get_value(self) -> dict[str, Any]:
        values = {}

        for spec in self.specs:
            var = self._vars.get(spec.name)

            if var is None:
                continue

            ParamSpec("period", int, default=14)
            raw = var.get()

            if raw == "" and spec.optional:
                continue

            try:
                values[spec.name] = self._cast_value(raw, spec.type)
            except Exception:
                raise InvalidInputFormat(
                    f"Invalid value for '{spec.name}', expected {spec.type.__name__}"
                )

        return values

    @staticmethod
    def _cast_value(value: Any, target_type: type):
        if issubclass(target_type, Enum):
            return target_type[value]

        if target_type is bool:
            return bool(value)

        return target_type(value)
