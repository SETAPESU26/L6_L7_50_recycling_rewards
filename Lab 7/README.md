# Lab 7: Fuzz Testing

This lab uses Hypothesis to fuzz the three input-processing functions in
`recycling_rewards.py` and then checks that valid behavior remains intact.

## Run

From this directory, install the dependencies and run the tests:

```powershell
python -m pip install hypothesis pytest
python -m pytest -v test_recycling_rewards.py
python recycling_rewards.py
```

## Input behavior

- `parse_collection("paper:12")` returns `("Paper", 12.0)`. Malformed,
  negative, non-finite, or non-string input returns `None`.
- `weight_average("5,12,20")` returns `12`. Malformed, negative, empty, or
  non-string input returns `0`.
- `net_points("80|10")` returns `150.0`, with negative results clamped to
  `0.0`. Malformed, non-finite, or non-string input returns `0.0`.

The Hypothesis tests feed text, `None`, numbers, bytes, and lists to all three
functions. They check that arbitrary inputs never raise, that results satisfy
the output contracts, and that representative valid inputs keep working.

## Findings

The starter implementation raised exceptions for missing or extra delimiters,
`None`, empty fields, and nonnumeric values. It also accepted non-finite float
values in reward calculations. The fixed implementation validates input types,
field counts, numeric conversion, finite values, and nonnegative weights before
returning results.
