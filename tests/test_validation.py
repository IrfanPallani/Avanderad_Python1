import pytest

from order_report.config import REQUIRED_COLUMNS
from order_report.validation import (
    ValidationError,
    check_columns,
    check_not_empty,
    check_values,
)


def test_valid_data_passes(make_orders):
    orders = make_orders({})
    check_columns(orders)
    check_not_empty(orders)
    check_values(orders)


@pytest.mark.parametrize("column", REQUIRED_COLUMNS)
def test_missing_column_is_reported(make_orders, column):
    orders = make_orders({}).drop(columns=[column])
    with pytest.raises(ValidationError, match=column):
        check_columns(orders)


def test_empty_data_gives_error(make_orders):
    empty = make_orders({}).iloc[0:0]
    with pytest.raises(ValidationError):
        check_not_empty(empty)


@pytest.mark.parametrize(
    ("column", "bad_value"),
    [("quantity", 0), ("quantity", -3), ("unit_price", 0), ("unit_price", -10.0),
     ("discount", -0.1), ("discount", 1.5)],
)
def test_unreasonable_values_give_error(make_orders, column, bad_value):
    orders = make_orders({column: bad_value})
    with pytest.raises(ValidationError, match=column):
        check_values(orders)


def test_discount_of_0_and_1_is_allowed(make_orders):
    check_values(make_orders({"discount": 0.0}, {"order_id": "O2", "discount": 1.0}))
