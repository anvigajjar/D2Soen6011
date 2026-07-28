"""
tan_gui.py
Student Name: Avani Dipakbhai Gajjar
Student ID: 40345876
Deliverable 2 - Problem 5

Tkinter GUI for the from-scratch tan(x) calculator implemented in
tan_scratch.py.

Run with:
    python3 tan_gui.py

No IDE is required -- this is a plain script run from any terminal with
Python 3 and its standard library (tkinter ships with CPython on
Windows/macOS; on Linux, install the 'python3-tk' package if not already
present).
"""

import tkinter as tk
from tkinter import ttk

from tan_scratch import (
    compute_tan,
    parse_numeric_input,
    TanCalculatorError,
    DEFAULT_TERMS,
)


class TanCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator - tan(x)")
        self.root.resizable(False, False)

        padding = {"padx": 10, "pady": 6}

        main = ttk.Frame(root, padding=16)
        main.grid(row=0, column=0, sticky="nsew")

        title_label = ttk.Label(
            main, text="tan(x) Calculator", font=("Segoe UI", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 12))

        # Angle input
        ttk.Label(main, text="Angle value:").grid(row=1, column=0, sticky="e", **padding)
        self.angle_var = tk.StringVar()
        self.angle_entry = ttk.Entry(main, textvariable=self.angle_var, width=20)
        self.angle_entry.grid(row=1, column=1, sticky="w", **padding)
        self.angle_entry.focus()

        domain_hint = ttk.Label(
            main,
            text="Domain: any real number. Undefined at odd multiples of 90\u00b0 (\u03c0/2 rad).",
            font=("Segoe UI", 8), foreground="#555555",
        )
        domain_hint.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 6))

        # Unit selection
        ttk.Label(main, text="Unit:").grid(row=3, column=0, sticky="e", **padding)
        self.unit_var = tk.StringVar(value="degrees")
        unit_frame = ttk.Frame(main)
        unit_frame.grid(row=3, column=1, sticky="w", **padding)
        ttk.Radiobutton(
            unit_frame, text="Degrees", variable=self.unit_var, value="degrees"
        ).pack(side="left")
        ttk.Radiobutton(
            unit_frame, text="Radians", variable=self.unit_var, value="radians"
        ).pack(side="left")

        # Compute button
        self.compute_btn = ttk.Button(main, text="Compute tan(x)", command=self.on_compute)
        self.compute_btn.grid(row=4, column=0, columnspan=2, pady=(8, 4))
        self.root.bind("<Return>", lambda event: self.on_compute())

        # Result label
        self.result_var = tk.StringVar(value="Result will appear here.")
        self.result_label = ttk.Label(
            main, textvariable=self.result_var, font=("Segoe UI", 12, "bold"),
            foreground="#1a5d1a", wraplength=320, justify="center",
        )
        self.result_label.grid(row=5, column=0, columnspan=2, pady=(8, 0))

        # Error label
        self.error_var = tk.StringVar(value="")
        self.error_label = ttk.Label(
            main, textvariable=self.error_var, foreground="#b00020",
            wraplength=320, justify="center",
        )
        self.error_label.grid(row=6, column=0, columnspan=2, pady=(4, 0))

    def on_compute(self):
        self.result_var.set("")
        self.error_var.set("")

        raw_angle = self.angle_var.get().strip()
        unit = self.unit_var.get()

        try:
            x_value = parse_numeric_input(raw_angle)
            result = compute_tan(x_value, unit, terms=DEFAULT_TERMS)
            self.result_var.set(f"tan({x_value} {unit}) = {result:.6f}")
        except TanCalculatorError as e:
            self.error_var.set(str(e))
        except Exception as e:  # pragma: no cover - safety net
            self.error_var.set(f"Unexpected error: {e}")


def main():
    root = tk.Tk()
    app = TanCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
