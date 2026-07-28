# tan(x) Scientific Calculator

SOEN 6011 — Deliverable 2
Avani Dipakbhai Gajjar — Student ID 40345876

A tan(x) calculator implemented **from scratch** in Python: no `math`
library (or any other library) is used to compute the trigonometric
result. Every subordinate operation — the value of pi, factorial,
absolute value, floating-point modulo, and the Maclaurin series terms
for sin(x)/cos(x) — is written out explicitly in [`tan_scratch.py`](tan_scratch.py).
A [Tkinter](https://docs.python.org/3/library/tkinter.html) GUI
([`tan_gui.py`](tan_gui.py)) sits on top of it.

## Features

- Computes tan(x) for an angle in **degrees or radians**
- Detects and reports asymptotes (odd multiples of 90°) as undefined
- 6-decimal-digit precision output
- Custom exception classes with user-friendly error messages
  (`NonNumericInputError`, `InvalidUnitError`, `UndefinedTangentError`,
  `NonFiniteInputError`)
- Simple, dependency-free Tkinter GUI

## Requirements

- Python 3.8+
- Tkinter (bundled with the standard CPython installer on Windows/macOS;
  on Debian/Ubuntu Linux run `sudo apt-get install python3-tk` if it is
  not already present)

No third-party packages and no IDE are required.

## Running the GUI

```bash
python3 tan_gui.py
```

## Running the console tests

```bash
python3 test_tan_scratch.py
```

`test_tan_scratch.py` is a verification harness only — it imports
Python's `math` module solely to check `tan_scratch.py`'s output for
correctness. `math` is never imported by `tan_scratch.py` or
`tan_gui.py` themselves.

## Project structure

```
.
├── tan_scratch.py       # from-scratch tan(x) implementation + custom exceptions
├── tan_gui.py            # Tkinter GUI
├── test_tan_scratch.py   # verification tests against math.tan
└── README.md
```

## Requirements traceability

See `REQUIREMENTS.md` for the full, updated (D2/Problem 7) requirements
list and its traceability to source.

## Algorithm

Maclaurin series expansion of sin(x) and cos(x) around 0, with range
reduction using the π-periodicity of tan(x), followed by division:
tan(x) = sin(x) / cos(x). See the D1 and D2 slide decks for the
pseudocode and the algorithm-selection rationale (Maclaurin series vs.
CORDIC).

## License

Educational project for SOEN 6011, Concordia University.
