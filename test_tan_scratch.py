"""
test_tan_scratch.py
Verification / edge-case harness

Covers the edge cases specifically requested for D2 verification:
  - empty field
  - non-numeric value
  - zero input
  - negative input
  - large input (overflow/underflow-prone range reduction)
  - symmetry: tan(-x) = -tan(x)  (odd-function property, the tan(x)
    analogue of the Beta-function symmetry B(x,y) = B(y,x))
  - repeated calculations (no hidden state / drift across calls)
  - recovery after an error (next valid call still succeeds)
"""

import math
from tan_scratch import (
    compute_tan,
    parse_numeric_input,
    InvalidUnitError,
    UndefinedTangentError,
    NonNumericInputError,
    NonFiniteInputError,
)

PASS, FAIL = 0, 0


def check(label, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"PASS: {label}")
    else:
        FAIL += 1
        print(f"FAIL: {label}  {detail}")


# --------------------------------------------------------------------
# 1. Core accuracy sweep vs math.tan
# --------------------------------------------------------------------
test_angles_deg = [0, 10, 30, 45, 60, 80, -30, -45, 135, 200, 359, 730]
max_diff = 0.0
for a in test_angles_deg:
    got = compute_tan(a, "degrees")
    expected = math.tan(math.radians(a))
    max_diff = max(max_diff, abs(got - expected))
check("core sweep vs math.tan (12 angles)", max_diff < 1e-9, f"max_diff={max_diff:.2e}")

# --------------------------------------------------------------------
# 2. Empty field -> helpful, non-echoing message
# --------------------------------------------------------------------
try:
    parse_numeric_input("")
    check("empty field raises NonNumericInputError", False)
except NonNumericInputError as e:
    msg = str(e)
    check("empty field message is helpful (no bare '' echo, gives example)",
          "''" not in msg and "e.g." in msg, msg)

try:
    parse_numeric_input("   ")
    check("whitespace-only field raises NonNumericInputError", False)
except NonNumericInputError as e:
    check("whitespace-only field handled same as empty", "e.g." in str(e))

# --------------------------------------------------------------------
# 3. Non-numeric value
# --------------------------------------------------------------------
try:
    parse_numeric_input("abc")
    check("non-numeric raises NonNumericInputError", False)
except NonNumericInputError as e:
    check("non-numeric message echoes bad value + gives example", "'abc'" in str(e))

# --------------------------------------------------------------------
# 4. Zero input
# --------------------------------------------------------------------
got0 = compute_tan(0, "degrees")
check("tan(0) == 0.0 exactly", got0 == 0.0, f"got={got0}")

# --------------------------------------------------------------------
# 5. Negative input
# --------------------------------------------------------------------
got_neg = compute_tan(-60, "degrees")
exp_neg = math.tan(math.radians(-60))
check("tan(-60 deg) matches math.tan", abs(got_neg - exp_neg) < 1e-9, f"{got_neg} vs {exp_neg}")

# --------------------------------------------------------------------
# 6. Large input (stresses range reduction; watch for overflow/underflow)
# --------------------------------------------------------------------
large_cases = [1e5, 1e7, 123456789]
for a in large_cases:
    got = compute_tan(a, "degrees")
    expected = math.tan(math.radians(a))
    diff = abs(got - expected)
    # Large-angle range reduction amplifies floating point error; we allow
    # a looser (but still tight) bound and report it rather than hide it.
    check(f"large input {a} deg stays finite and close to math.tan",
          got == got and abs(got) < 1e8 and diff < 1e-3,
          f"got={got}, expected={expected}, diff={diff:.2e}")

# Near-asymptote large-magnitude result (very close to 90 deg, not exactly on it)
near_asym = compute_tan(89.9999, "degrees")
check("near-asymptote input gives a large finite result (no crash)",
      near_asym == near_asym and abs(near_asym) > 1000, f"got={near_asym}")

# Very small result near 0
small_val = compute_tan(0.0001, "degrees")
check("very small angle gives a very small finite result",
      abs(small_val) < 1e-4 and small_val == small_val, f"got={small_val}")

# --------------------------------------------------------------------
# 7. Symmetry: tan(-x) = -tan(x)  (odd-function property)
# --------------------------------------------------------------------
for a in [15, 30, 45, 63.5, 80]:
    pos = compute_tan(a, "degrees")
    neg = compute_tan(-a, "degrees")
    check(f"symmetry tan(-{a}) == -tan({a})", abs(neg - (-pos)) < 1e-9, f"{neg} vs {-pos}")

# --------------------------------------------------------------------
# 8. Repeated calculations (no hidden state / drift across calls)
# --------------------------------------------------------------------
repeat_vals = [compute_tan(37, "degrees") for _ in range(500)]
check("500 repeated calls return identical result (no state leakage)",
      len(set(repeat_vals)) == 1, f"distinct values={len(set(repeat_vals))}")

# --------------------------------------------------------------------
# 9. Undefined / invalid-unit cases
# --------------------------------------------------------------------
try:
    compute_tan(90, "degrees")
    check("tan(90 deg) raises UndefinedTangentError", False)
except UndefinedTangentError:
    check("tan(90 deg) raises UndefinedTangentError", True)

try:
    compute_tan(10, "gradians")
    check("invalid unit raises InvalidUnitError", False)
except InvalidUnitError:
    check("invalid unit raises InvalidUnitError", True)

try:
    compute_tan(float("inf"), "degrees")
    check("infinite input raises NonFiniteInputError", False)
except NonFiniteInputError:
    check("infinite input raises NonFiniteInputError", True)

# --------------------------------------------------------------------
# 10. Recovery after an error: the very next call still succeeds
# --------------------------------------------------------------------
try:
    compute_tan(90, "degrees")  # deliberately trigger an error
except UndefinedTangentError:
    pass
recovered = compute_tan(45, "degrees")
check("valid call immediately after an error still succeeds (recovery)",
      abs(recovered - 1.0) < 1e-9, f"got={recovered}")

# --------------------------------------------------------------------
# 11. Radians mode sanity check
# --------------------------------------------------------------------
got_rad = compute_tan(math.pi / 4, "radians")
check("tan(pi/4 rad) == 1.0", abs(got_rad - 1.0) < 1e-9, f"got={got_rad}")

print(f"\n{PASS} passed, {FAIL} failed out of {PASS + FAIL} checks.")
assert FAIL == 0, "One or more verification checks failed."
