from datetime import datetime

import pytest

from simple_agent.graph.tools import calculate, get_current_datetime


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 2 * 2", "6"),
        ("(2 + 3) * 4 / 5", "4"),
        ("10 / 4", "2.5"),
        ("-3 ** 2", "-9"),
        ("7 // 2", "3"),
    ],
)
def test_calculate(expression, expected):
    assert calculate.invoke({"expression": expression}) == expected


@pytest.mark.parametrize(
    "expression",
    ["1 / 0", "__import__('os')", "9 ** 9 ** 9", "2 +", "'abc' * 3"],
)
def test_calculate_returns_error(expression):
    assert calculate.invoke({"expression": expression}).startswith("Ошибка")


def test_get_current_datetime_returns_aware_iso_datetime():
    value = datetime.fromisoformat(get_current_datetime.invoke({}))
    assert value.tzinfo is not None
