
import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ==========================================
# 1. TEST CASES FOR reward_points()
# ==========================================

def test_unknown_material():
    with pytest.raises(ValueError):
        reward_points("glass", 10, False)


def test_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -2, False)


def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0


def test_equal_minimum_weight():
    assert reward_points("paper", 5, False) == 0


def test_bonus_for_paper():
    assert reward_points("paper", 5, True) == 6


def test_bonus_for_plastic():
    assert reward_points("plastic", 3, True) == 6


def test_bonus_not_applied_to_metal():
    assert reward_points("metal", 3, True) == 12


def test_normal_paper_reward():
    assert reward_points("paper", 7, False) == 12


def test_normal_metal_reward():
    assert reward_points("metal", 5, False) == 36


def test_high_weight_nonmetal():
    assert reward_points("paper", 30, False) == 250


def test_high_weight_metal():
    assert reward_points("metal", 23, False) == 378


def test_exactly_twenty_extra_weight():
    assert reward_points("paper", 25, False) == 120


# ==========================================
# 2. TEST CASES FOR collection_accepted()
# ==========================================

def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True


def test_hazardous_within_limit():
    assert collection_accepted(5, 2, True) is True


def test_hazardous_above_limit():
    assert collection_accepted(6, 2, True) is False


def test_weight_above_fifty():
    assert collection_accepted(60, 2, False) is False


def test_weight_exactly_fifty():
    assert collection_accepted(50, 2, False) is True


def test_bags_within_limit():
    assert collection_accepted(20, 3, False) is True


def test_bags_above_limit():
    assert collection_accepted(20, 4, False) is False


# ==========================================
# 3. TEST CASES FOR slot_status()
# ==========================================

def test_morning_open():
    assert slot_status(20, True, False) == "open"


def test_morning_late():
    assert slot_status(10, True, False) == "late"


def test_morning_missed():
    assert slot_status(4, True, False) == "missed"


def test_evening_open():
    assert slot_status(10, False, False) == "open"


def test_evening_late():
    assert slot_status(5, False, False) == "late"


def test_evening_missed():
    assert slot_status(-6, False, False) == "missed"


def test_holiday_open():
    assert slot_status(35, True, True) == "open"


def test_holiday_late():
    assert slot_status(20, True, True) == "late"


def test_holiday_missed():
    assert slot_status(5, True, True) == "missed"
