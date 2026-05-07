"""The View layer: tkinter widgets only.

Owns every widget, every StringVar, every grid call. Knows nothing about
parking rules, vehicles, or search strategies. Exposes three kinds of
methods for the Controller:

    read_*      -> pull typed input out of form fields
    show_*      -> write output to the text area
    on_*        -> bind a callback (a Controller method) to a button

This is what removes the module-level `tk.StringVar` globals and the
`tfield.insert(...)` calls that were scattered through the old domain code.
"""

import tkinter as tk
from typing import Callable


class ParkingLotView:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Parking Lot Manager")
        self.root.geometry("650x850")
        self.root.resizable(False, False)

        self._lot_capacity = tk.StringVar()
        self._ev_capacity = tk.StringVar()
        self._level = tk.StringVar(value="1")

        self._make = tk.StringVar()
        self._model = tk.StringVar()
        self._color = tk.StringVar()
        self._regnum = tk.StringVar()
        self._is_ev = tk.IntVar()
        self._is_motor = tk.IntVar()

        self._leave_slot = tk.StringVar()
        self._leave_is_ev = tk.IntVar()

        self._search_regnum = tk.StringVar()
        self._search_color = tk.StringVar()
        self._regnum_by_color = tk.StringVar()

        self._build_widgets()

    def _build_widgets(self) -> None:
        r = self.root

        tk.Label(r, text="Parking Lot Manager", font="Arial 14 bold").grid(
            row=0, column=0, padx=10, columnspan=4
        )

        tk.Label(r, text="Lot Creation", font="Arial 12 bold").grid(
            row=1, column=0, padx=10, columnspan=4
        )
        tk.Label(r, text="Regular Spaces", font="Arial 12").grid(row=2, column=0, padx=5)
        tk.Entry(r, textvariable=self._lot_capacity, width=6, font="Arial 12").grid(
            row=2, column=1, padx=4, pady=2
        )
        tk.Label(r, text="EV Spaces", font="Arial 12").grid(row=2, column=2, padx=5)
        tk.Entry(r, textvariable=self._ev_capacity, width=6, font="Arial 12").grid(
            row=2, column=3, padx=4, pady=4
        )
        tk.Label(r, text="Floor Level", font="Arial 12").grid(row=3, column=0, padx=5)
        tk.Entry(r, textvariable=self._level, width=6, font="Arial 12").grid(
            row=3, column=1, padx=4, pady=4
        )
        self._create_lot_btn = tk.Button(
            r, text="Create Parking Lot", font="Arial 12",
            bg="lightblue", activebackground="teal", padx=5, pady=5,
        )
        self._create_lot_btn.grid(row=4, column=0, padx=4, pady=4)

        tk.Label(r, text="Car Management", font="Arial 12 bold").grid(
            row=5, column=0, padx=10, columnspan=4
        )
        tk.Label(r, text="Make", font="Arial 12").grid(row=6, column=0, padx=5)
        tk.Entry(r, textvariable=self._make, width=12, font="Arial 12").grid(row=6, column=1, padx=4, pady=4)
        tk.Label(r, text="Model", font="Arial 12").grid(row=6, column=2, padx=5)
        tk.Entry(r, textvariable=self._model, width=12, font="Arial 12").grid(row=6, column=3, padx=4, pady=4)
        tk.Label(r, text="Color", font="Arial 12").grid(row=7, column=0, padx=5)
        tk.Entry(r, textvariable=self._color, width=12, font="Arial 12").grid(row=7, column=1, padx=4, pady=4)
        tk.Label(r, text="Registration #", font="Arial 12").grid(row=7, column=2, padx=5)
        tk.Entry(r, textvariable=self._regnum, width=12, font="Arial 12").grid(row=7, column=3, padx=4, pady=4)

        tk.Checkbutton(r, text="Electric", variable=self._is_ev, font="Arial 12").grid(
            row=8, column=0, padx=4, pady=4
        )
        tk.Checkbutton(r, text="Motorcycle", variable=self._is_motor, font="Arial 12").grid(
            row=8, column=1, padx=4, pady=4
        )

        self._park_btn = tk.Button(
            r, text="Park Car", font="Arial 11",
            bg="lightblue", activebackground="teal", padx=5, pady=5,
        )
        self._park_btn.grid(row=9, column=0, padx=4, pady=4)

        tk.Label(r, text="Slot #", font="Arial 12").grid(row=10, column=0, padx=5)
        tk.Entry(r, textvariable=self._leave_slot, width=12, font="Arial 12").grid(
            row=10, column=1, padx=4, pady=4
        )
        tk.Checkbutton(r, text="Remove EV?", variable=self._leave_is_ev, font="Arial 12").grid(
            row=10, column=2, padx=4, pady=4
        )
        self._remove_btn = tk.Button(
            r, text="Remove Car", font="Arial 11",
            bg="lightblue", activebackground="teal", padx=5, pady=5,
        )
        self._remove_btn.grid(row=11, column=0, padx=4, pady=4)

        tk.Label(r, text="").grid(row=12, column=0)

        self._find_by_reg_btn = tk.Button(
            r, text="Get Slot ID by Registration #", font="Arial 11",
            bg="lightblue", activebackground="teal", padx=5, pady=5,
        )
        self._find_by_reg_btn.grid(row=13, column=0, padx=4, pady=4)
        tk.Entry(r, textvariable=self._search_regnum, width=12, font="Arial 12").grid(
            row=13, column=1, padx=4, pady=4
        )

        self._find_by_color_btn = tk.Button(
            r, text="Get Slot ID by Color", font="Arial 11",
            bg="lightblue", activebackground="teal", padx=5, pady=5,
        )
        self._find_by_color_btn.grid(row=13, column=2, padx=4, pady=4)
        tk.Entry(r, textvariable=self._search_color, width=12, font="Arial 12").grid(
            row=13, column=3, padx=4, pady=4
        )

        self._regnum_by_color_btn = tk.Button(
            r, text="Get Registration # by Color", font="Arial 11",
            bg="lightblue", activebackground="teal", padx=5, pady=5,
        )
        self._regnum_by_color_btn.grid(row=14, column=0, padx=4, pady=4)
        tk.Entry(r, textvariable=self._regnum_by_color, width=12, font="Arial 12").grid(
            row=14, column=1, padx=4, pady=4
        )

        self._charge_status_btn = tk.Button(
            r, text="EV Charge Status", font="Arial 11",
            bg="lightblue", activebackground="teal", padx=5, pady=5,
        )
        self._charge_status_btn.grid(row=14, column=2, padx=4, pady=4)

        self._status_btn = tk.Button(
            r, text="Current Lot Status", font="Arial 11",
            bg="PaleGreen1", activebackground="PaleGreen3", padx=5, pady=5,
        )
        self._status_btn.grid(row=15, column=0, padx=4, pady=4)

        self._output = tk.Text(r, width=70, height=15)
        self._output.grid(row=16, column=0, padx=10, pady=10, columnspan=4)

    # --- Input readers (Controller pulls typed values out) ---

    def read_lot_config(self) -> tuple[int, int, int]:
        return (
            int(self._lot_capacity.get()),
            int(self._ev_capacity.get()),
            int(self._level.get()),
        )

    def read_park_form(self) -> dict:
        return {
            "regnum": self._regnum.get(),
            "make": self._make.get(),
            "model": self._model.get(),
            "color": self._color.get(),
            "is_ev": bool(self._is_ev.get()),
            "is_motor": bool(self._is_motor.get()),
        }

    def read_leave_form(self) -> tuple[int, bool]:
        return int(self._leave_slot.get()), bool(self._leave_is_ev.get())

    def read_search_regnum(self) -> str:
        return self._search_regnum.get()

    def read_search_color(self) -> str:
        return self._search_color.get()

    def read_regnum_by_color(self) -> str:
        return self._regnum_by_color.get()

    # --- Output (Controller writes results here) ---

    def show(self, text: str) -> None:
        self._output.insert(tk.INSERT, text)

    # --- Button bindings (Controller registers its methods) ---

    def on_create_lot(self, callback: Callable[[], None]) -> None:
        self._create_lot_btn.config(command=callback)

    def on_park(self, callback: Callable[[], None]) -> None:
        self._park_btn.config(command=callback)

    def on_remove(self, callback: Callable[[], None]) -> None:
        self._remove_btn.config(command=callback)

    def on_find_by_regnum(self, callback: Callable[[], None]) -> None:
        self._find_by_reg_btn.config(command=callback)

    def on_find_by_color(self, callback: Callable[[], None]) -> None:
        self._find_by_color_btn.config(command=callback)

    def on_regnum_by_color(self, callback: Callable[[], None]) -> None:
        self._regnum_by_color_btn.config(command=callback)

    def on_charge_status(self, callback: Callable[[], None]) -> None:
        self._charge_status_btn.config(command=callback)

    def on_status(self, callback: Callable[[], None]) -> None:
        self._status_btn.config(command=callback)
