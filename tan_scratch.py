"""
tan_scratch.py
Student Name: Avani Dipakbhai Gajjar
Student ID: 40345876
Deliverable 2 - Problem 5

"From scratch" implementation of tan(x).

RULES FOLLOWED:
  - No 'import math' (or any other library) is used anywhere in this file.
  - Only Python's core arithmetic operators (+, -, *, /, **, %, comparisons)
    and core control-flow (for/while/if) are used to build every
    trigonometric building block below.
  - Every helper that a stock implementation would normally get "for free"
    from the math module (constant pi, factorial, absolute value, and
    reducing an angle into range) has been written out explicitly, so that
    it is subordinate to compute_tan(), per the assignment instructions.

Algorithm (unchanged from D1/Problem 4): Maclaurin series expansion of
sin(x) and cos(x), with range reduction using the pi-periodicity of
tan(x), followed by division (tan(x) = sin(x) / cos(x)).

Traceability to requirements (see D2/Problem 7 for the updated list):
  REQ-001 -> compute_tan()
  REQ-002 -> unit parameter ("degrees" / "radians")
  REQ-003 -> asymptote / undefined detection near odd multiples of 90 deg
  REQ-004 -> 6 decimal digit output formatting (GUI layer)
  REQ-007 -> no math-library dependency (this whole file)
  REQ-008 -> Tkinter GUI (tan_gui.py)
  REQ-009 -> custom exception classes, defined below
"""

# Custom exception classes (REQ-009)

class TanCalculatorError(Exception):
    
    pass


class NonNumericInputError(TanCalculatorError):

    def __init__(self, raw_value):
        stripped = str(raw_value).strip()
        if stripped == "":
            message = (
                "Please enter a numeric angle value (e.g. 45 or -12.5) "
                "before computing tan(x)."
            )
        else:
            message = (
                f"'{raw_value}' is not a numeric angle. "
                "Please enter a real number such as 45 or -12.5."
            )
        super().__init__(message)
        self.raw_value = raw_value


class InvalidUnitError(TanCalculatorError):

    def __init__(self, raw_unit):
        message = (
            f"'{raw_unit}' is not a valid unit. "
            "Please choose either 'degrees' or 'radians'."
        )
        super().__init__(message)
        self.raw_unit = raw_unit


class UndefinedTangentError(TanCalculatorError):
   
    def __init__(self, x_value, unit):
        message = (
            f"tan({x_value} {unit}) is undefined: this angle is an odd "
            "multiple of 90 degrees (pi/2 radians), where tangent has a "
            "vertical asymptote. Try a value that is not a multiple of 90 "
            "degrees away from 90 degrees."
        )
        super().__init__(message)
        self.x_value = x_value
        self.unit = unit


class NonFiniteInputError(TanCalculatorError):

    def __init__(self, raw_value):
        message = (
            f"'{raw_value}' is not a finite angle. "
            "Please enter a finite real number (not infinity or NaN)."
        )
        super().__init__(message)
        self.raw_value = raw_value

#constants
PI = 3.14159265358979323846 
EPSILON = 1e-9
DEFAULT_TERMS = 25

# Arithmetic helper functions written from scratch (subordinate functions required by the assignment)

def abs_val(x):
    if x < 0:
        return -x
    return x

def factorial(n):
    if n < 0:
        raise ValueError("factorial is undefined for negative integers")
    result = 1
    i = 2
    while i <= n:
        result = result * i
        i = i + 1
    return result

def power(base, exponent):
    result = 1.0
    i = 0
    while i < exponent:
        result = result * base
        i = i + 1
    return result

def mod(a, b):
    quotient = a / b
    truncated = int(quotient)
    return a - truncated * b

def degrees_to_radians(deg):
    return deg * PI / 180.0

# Series expansion helpers

def maclaurin_sin(x, terms=DEFAULT_TERMS):
    total = 0.0
    sign = 1
    for k in range(terms):
        exponent = 2 * k + 1
        term = power(x, exponent) / factorial(exponent)
        total += sign * term
        sign = -sign
    return total


def maclaurin_cos(x, terms=DEFAULT_TERMS):
    total = 0.0
    sign = 1
    for k in range(terms):
        exponent = 2 * k
        term = power(x, exponent) / factorial(exponent)
        total += sign * term
        sign = -sign
    return total


def reduce_angle(x_rad):
    """Reduce x_rad into (-pi/2, pi/2] using pi-periodicity of tan(x)."""
    x_rad = mod(x_rad, PI)
    if x_rad > PI / 2:
        x_rad -= PI
    elif x_rad < -PI / 2:
        x_rad += PI
    return x_rad


# Public entry point

def compute_tan(x_value, unit="degrees", terms=DEFAULT_TERMS, epsilon=EPSILON):
   
    if unit not in ("degrees", "radians"):
        raise InvalidUnitError(unit)

    if x_value != x_value or x_value in (float("inf"), float("-inf")):
        raise NonFiniteInputError(x_value)

    if unit == "degrees":
        x_rad = degrees_to_radians(x_value)
    else:
        x_rad = x_value

    x_reduced = reduce_angle(x_rad)

    if abs_val(abs_val(x_reduced) - PI / 2) < epsilon:
        raise UndefinedTangentError(x_value, unit)

    cos_val = maclaurin_cos(x_reduced, terms)
    sin_val = maclaurin_sin(x_reduced, terms)
    return sin_val / cos_val


def parse_numeric_input(raw_value):
    
    try:
        return float(raw_value)
    except ValueError:
        raise NonNumericInputError(raw_value)
