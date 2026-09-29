import pandas as pd
import pytest

# En vanlig, giltig order. Testerna ändrar bara det de vill testa.
BASE_ROW = {
    "order_id": "O1",
    "order_date": "2026-01-01",
    "customer_id": "C1",
    "region": "North",
    "product_category": "Books",
    "quantity": 1,
    "unit_price": 100.0,
    "discount": 0.0,
    "returned": False,
}


@pytest.fixture
def make_orders():
    """Bygger en tabell av de rader man skickar in."""

    def _make(*rows):
        return pd.DataFrame([{**BASE_ROW, **row} for row in rows])

    return _make
