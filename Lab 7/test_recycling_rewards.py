"""Property-based tests for malformed and valid Recycling Rewards input."""

from hypothesis import given, strategies as st

from recycling_rewards import net_points, parse_collection, weight_average


arbitrary_input = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.binary(),
    st.lists(st.integers()),
)


@given(arbitrary_input)
def test_parse_collection_never_crashes(value):
    parse_collection(value)


@given(arbitrary_input)
def test_weight_average_never_crashes(value):
    weight_average(value)


@given(arbitrary_input)
def test_net_points_never_crashes(value):
    net_points(value)


@given(st.text())
def test_parse_collection_result_is_valid_or_none(value):
    result = parse_collection(value)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], str)
        and isinstance(result[1], float)
    )


@given(st.text())
def test_weight_average_is_nonnegative_integer(value):
    result = weight_average(value)
    assert isinstance(result, int)
    assert result >= 0


@given(st.text())
def test_net_points_is_finite_and_nonnegative(value):
    result = net_points(value)
    assert isinstance(result, float)
    assert result >= 0
    assert result != float("inf")


def test_parse_collection_valid_input():
    assert parse_collection("  paper:12.5  ") == ("Paper", 12.5)


def test_weight_average_valid_input():
    assert weight_average("5,12,20") == 12


def test_net_points_valid_and_clamped_inputs():
    assert net_points("80|10") == 150.0
    assert net_points("5|20") == 0.0
    assert net_points("1e308|0") == 0.0
