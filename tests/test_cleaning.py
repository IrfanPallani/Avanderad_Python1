import pytest

from order_report.processing import clean_orders
from order_report.validation import ValidationError


def test_region_and_category_are_cleaned(make_orders):
    orders = make_orders(
        {"order_id": "O1", "region": " north ", "product_category": "electronics "},
        {"order_id": "O2", "region": "SOUTH", "product_category": "HOME"},
    )
    cleaned = clean_orders(orders)
    assert cleaned["region"].tolist() == ["North", "South"]
    assert cleaned["product_category"].tolist() == ["Electronics", "Home"]


def test_missing_region_becomes_unknown(make_orders):
    cleaned = clean_orders(make_orders({"region": None}))
    assert cleaned["region"].tolist() == ["Unknown"]


def test_missing_quantity_becomes_one(make_orders):
    cleaned = clean_orders(make_orders({"quantity": None}))
    assert cleaned["quantity"].tolist() == [1]


def test_missing_price_becomes_median(make_orders):
    orders = make_orders(
        {"order_id": "O1", "unit_price": 100.0},
        {"order_id": "O2", "unit_price": 200.0},
        {"order_id": "O3", "unit_price": 900.0},
        {"order_id": "O4", "unit_price": None},
    )
    cleaned = clean_orders(orders)
    assert cleaned["unit_price"].tolist() == [100.0, 200.0, 900.0, 200.0]


def test_bad_discount_becomes_zero(make_orders):
    orders = make_orders(
        {"order_id": "O1", "discount": "0.1"},
        {"order_id": "O2", "discount": "unknown"},
        {"order_id": "O3", "discount": None},
    )
    cleaned = clean_orders(orders)
    assert cleaned["discount"].tolist() == [0.1, 0.0, 0.0]


def test_returned_text_is_turned_into_true_or_false(make_orders):
    values = ["true", "Yes", "1", "ja", "false", "no", None]
    orders = make_orders(*({"order_id": f"O{i}", "returned": v} for i, v in enumerate(values)))
    cleaned = clean_orders(orders)
    assert cleaned["returned"].tolist() == [True, True, True, True, False, False, False]


def test_original_table_is_not_changed(make_orders):
    orders = make_orders({"region": " north "})
    clean_orders(orders)
    assert orders["region"].tolist() == [" north "]


def test_error_if_no_price_is_valid(make_orders):
    orders = make_orders({"unit_price": None})
    with pytest.raises(ValidationError, match="unit_price"):
        clean_orders(orders)
