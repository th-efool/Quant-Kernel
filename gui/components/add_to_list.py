import tkinter as tk
from tkinter import messagebox

from gui.components.base.base_ui_component import UIComponent
from gui.components.error import InvalidInputFormat


class AddToListComponent(UIComponent):
    """
    Wraps a SelectAndConfigure component and allows adding
    multiple configured instances to a list.
    """

    def __init__(self, selector, title: str):
        super().__init__()
        self.selector = selector
        self.title = title

        self._items = []
        self._listbox = None
        self._add_btn = None

    # ---------- BUILD ----------

    def build(self, parent):
        frame = tk.LabelFrame(parent, text=self.title)
        self.widget = frame

        # --- selector UI ---
        selector_widget = self.selector.build(frame)
        selector_widget.pack(fill="x", pady=4)

        # --- Add button ---
        self._add_btn = tk.Button(
            frame,
            text="Add",
            command=self._add_item,
            bg="#333",
            fg="white",
            state="disabled",  # 🔥 starts disabled
        )
        self._add_btn.pack(fill="x", pady=4)

        # --- Listbox ---
        self._listbox = tk.Listbox(frame, height=5)
        self._listbox.pack(fill="both", expand=True)

        # --- react to selector changes ---
        self.selector.on_change(self._update_add_state)
        self._update_add_state()

        return frame

    # ---------- INTERNAL ----------

    def _update_add_state(self):
        """
        Enable Add button only if something is selected.
        """
        if self.selector.has_selection():
            self._add_btn.config(state="normal")
        else:
            self._add_btn.config(state="disabled")

    def _add_item(self):
        # Guard: nothing selected
        if not self.selector.has_selection():
            messagebox.showwarning(
                "Nothing selected",
                "Please select an item to add."
            )
            return

        # Guard: invalid parameters
        try:
            item = self.selector.get_value()
        except InvalidInputFormat as e:
            messagebox.showerror(
                "Invalid parameters",
                str(e)
            )
            return

        # Success
        self._items.append(item)
        self._listbox.insert("end", self._format_label(item))

    def _format_label(self, item):
        params = ", ".join(
            f"{k}={v}"
            for k, v in item.__dict__.items()
            if not k.startswith("_")
        )
        return f"{item.__class__.__name__}({params})"

    # ---------- DATA API ----------

    def get_value(self):
        """
        Returns list of configured objects.
        """
        return list(self._items)

    def clear(self):
        self._items.clear()
        self._listbox.delete(0, "end")
