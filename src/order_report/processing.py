"""Rensar datan och räknar ut rapporterna. Ingen fil läses eller sparas här."""

import logging

import pandas as pd

from order_report.config import TRUE_VALUES
from order_report.validation import ValidationError

logger = logging.getLogger(__name__)


def _warn(column, count):
    """Loggar en varning om värden har ersatts."""
    if count > 0:
        logger.warning("Kolumn %s: %d saknade eller ogiltiga värden ersattes", column, count)


def _clean_text(column):
    """Tar bort mellanslag, sätter stor bokstav först och byter saknat mot Unknown."""
    return column.fillna("Unknown").astype(str).str.strip().str.title()


def clean_orders(orders):
    """Rensar datan. Samma regler som i originalprogrammet."""
    data = orders.copy()

    for name in ["region", "product_category"]:
        _warn(name, data[name].isna().sum())
        data[name] = _clean_text(data[name])

    # Saknat antal blir 1
    quantity = pd.to_numeric(data["quantity"], errors="coerce")
    _warn("quantity", quantity.isna().sum())
    data["quantity"] = quantity.fillna(1)

    # Saknat pris blir medianpriset
    unit_price = pd.to_numeric(data["unit_price"], errors="coerce")
    if unit_price.isna().all():
        raise ValidationError("unit_price saknar giltiga värden")
    _warn("unit_price", unit_price.isna().sum())
    data["unit_price"] = unit_price.fillna(unit_price.median())

    # Saknad rabatt blir 0
    discount = pd.to_numeric(data["discount"], errors="coerce")
    _warn("discount", discount.isna().sum())
    data["discount"] = discount.fillna(0)

    # Saknat värde i returned räknas som "inte returnerad"
    _warn("returned", data["returned"].isna().sum())
    data["returned"] = (
        data["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(TRUE_VALUES)
    )

    return data


def add_order_values(orders):
    """Lägger till order_value och discounted_value."""
    data = orders.copy()
    data["order_value"] = data["quantity"] * data["unit_price"]
    data["discounted_value"] = data["order_value"] * (1 - data["discount"])
    return data


def make_overview(orders):
    """Total försäljning, antal order och antal returer."""
    total_sales = round(orders["discounted_value"].sum(), 2)
    order_count = orders["order_id"].nunique()
    return_count = int(orders["returned"].sum())

    # Listan blandar float och int, så antalen sparas som t.ex. 80.0.
    # Jag har behållit det så att filen blir likadan som i originalet.
    return pd.DataFrame(
        {
            "metric": ["total_sales", "order_count", "return_count"],
            "value": [total_sales, order_count, return_count],
        }
    )


def summarize_by(orders, column):
    """Antal order, försäljning, returer och returandel per grupp."""
    table = orders.groupby(column, as_index=False).agg(
        order_count=("order_id", "nunique"),
        total_sales=("discounted_value", "sum"),
        returns=("returned", "sum"),
    )
    table["total_sales"] = table["total_sales"].round(2)
    table["return_rate"] = (table["returns"] / table["order_count"]).round(3)
    return table


def sales_report(orders, column):
    """Försäljning per grupp, störst först."""
    table = summarize_by(orders, column)
    return table.sort_values("total_sales", ascending=False).reset_index(drop=True)


def returns_report(orders, column):
    """Returer per grupp, högst returandel först."""
    table = summarize_by(orders, column)
    table = table[[column, "order_count", "returns", "return_rate"]]
    return table.sort_values("return_rate", ascending=False).reset_index(drop=True)


def build_reports(orders):
    """Skapar alla rapporter. Returnerar en dict: filnamn (utan .csv) -> tabell."""
    data = add_order_values(orders)
    return {
        "overview": make_overview(data),
        "sales_by_category": sales_report(data, "product_category"),
        "sales_by_region": sales_report(data, "region"),
        "returns_by_category": returns_report(data, "product_category"),
    }
