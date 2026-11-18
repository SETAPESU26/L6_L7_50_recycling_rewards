"""Input parsing helpers for the Recycling Rewards application."""

import math


def parse_collection(text):
    """Parse ``material:weight``; return None when the input is invalid."""
    if not isinstance(text, str) or text.count(":") != 1:
        return None

    material, raw_weight = (part.strip() for part in text.split(":", 1))
    if not material or not raw_weight:
        return None

    try:
        weight = float(raw_weight)
    except (TypeError, ValueError):
        return None

    if not math.isfinite(weight) or weight < 0:
        return None
    return material.title(), weight


def weight_average(weights_csv):
    """Return the integer average of comma-separated nonnegative weights.

    Invalid input or an empty list returns 0, keeping the CLI safe to use with
    malformed or fuzz-generated input.
    """
    if not isinstance(weights_csv, str) or not weights_csv.strip():
        return 0

    try:
        values = [int(value.strip()) for value in weights_csv.split(",")]
    except (TypeError, ValueError):
        return 0

    if not values or any(value < 0 for value in values):
        return 0
    return sum(values) // len(values)


def net_points(text):
    """Return doubled points minus penalty, clamped at zero.

    Invalid or non-finite values return 0.0.
    """
    if not isinstance(text, str) or text.count("|") != 1:
        return 0.0

    raw_points, raw_penalty = (part.strip() for part in text.split("|", 1))
    if not raw_points or not raw_penalty:
        return 0.0

    try:
        points, penalty = float(raw_points), float(raw_penalty)
    except (TypeError, ValueError):
        return 0.0

    if not math.isfinite(points) or not math.isfinite(penalty):
        return 0.0
    total = points * 2 - penalty
    if not math.isfinite(total):
        return 0.0
    return max(total, 0.0)


def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    print("Material and Weight:", parse_collection(user_input))

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    print("Average Weight:", weight_average(user_input))

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    print("Net Points:", net_points(user_input))


if __name__ == "__main__":
    main()
