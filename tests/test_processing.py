import pytest

from order_report.processing import (
    add_order_values,
    build_reports,
    make_overview,
    returns_report,
    sales_report,
)


@pytest.fixture
def orders(make_orders):
    """Fyra order med värden som jag räknat ut för hand.

    order  region  kategori  antal*pris  rabatt  efter rabatt  retur
    O1     North   Books     2*100=200   0.1     180           nej
    O2     North   Books     1*50 =50    0.0     50            ja
    O3     South   Home      3*200=600   0.5     300           ja
    O4     South   Home      1*100=100   0.0     100           ja
    """
    return make_orders(
        {"order_id": "O1", "region": "North", "product_category": "Books",
         "quantity": 2, "unit_price": 100.0, "discount": 0.1, "returned": False},
        {"order_id": "O2", "region": "North", "product_category": "Books",
         "quantity": 1, "unit_price": 50.0, "discount": 0.0, "returned": True},
        {"order_id": "O3", "region": "South", "product_category": "Home",
         "quantity": 3, "unit_price": 200.0, "discount": 0.5, "returned": True},
        {"order_id": "O4", "region": "South", "product_category": "Home",
         "quantity": 1, "unit_price": 100.0, "discount": 0.0, "returned": True},
    )


def test_order_value_and_discounted_value(orders):
    data = add_order_values(orders)
    assert data["order_value"].tolist() == [200.0, 50.0, 600.0, 100.0]
    assert data["discounted_value"].tolist() == [180.0, 50.0, 300.0, 100.0]


def test_overview(orders):
    overview = make_overview(add_order_values(orders))
    values = dict(zip(overview["metric"], overview["value"]))
    assert values == {"total_sales": 630.0, "order_count": 4, "return_count": 3}


def test_overview_counts_same_order_id_once(make_orders):
    orders = make_orders({"order_id": "O1"}, {"order_id": "O1"}, {"order_id": "O2"})
    overview = make_overview(add_order_values(orders))
    values = dict(zip(overview["metric"], overview["value"]))
    assert values["order_count"] == 2


def test_sales_by_category_is_sorted_with_biggest_first(orders):
    report = sales_report(add_order_values(orders), "product_category")
    assert report["product_category"].tolist() == ["Home", "Books"]
    assert report["total_sales"].tolist() == [400.0, 230.0]
    assert report["returns"].tolist() == [2, 1]
    assert report["return_rate"].tolist() == [1.0, 0.5]


def test_sales_by_region(orders):
    report = sales_report(add_order_values(orders), "region")
    assert report["region"].tolist() == ["South", "North"]
    assert report["total_sales"].tolist() == [400.0, 230.0]


def test_return_rate_is_rounded_to_three_decimals(make_orders):
    orders = make_orders(
        {"order_id": "O1", "returned": True},
        {"order_id": "O2"},
        {"order_id": "O3"},
    )
    report = sales_report(add_order_values(orders), "region")
    assert report["return_rate"].tolist() == [0.333]


def test_returns_report_has_highest_return_rate_first(orders):
    report = returns_report(add_order_values(orders), "product_category")
    assert report.columns.tolist() == ["product_category", "order_count", "returns", "return_rate"]
    assert report["product_category"].tolist() == ["Home", "Books"]


def test_build_reports_gives_four_reports(orders):
    reports = build_reports(orders)
    assert list(reports) == [
        "overview", "sales_by_category", "sales_by_region", "returns_by_category",
    ]
