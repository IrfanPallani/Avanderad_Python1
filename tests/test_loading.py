import pytest

from order_report.loading import load_orders
from order_report.validation import ValidationError


def test_reads_csv_file(tmp_path):
    file = tmp_path / "orders.csv"
    file.write_text("order_id,quantity\nO1,2\nO2,3\n")
    orders = load_orders(file)
    assert len(orders) == 2
    assert orders["quantity"].tolist() == [2, 3]


def test_missing_file_gives_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_orders(tmp_path / "finns_inte.csv")


def test_empty_file_gives_error(tmp_path):
    file = tmp_path / "tom.csv"
    file.write_text("")
    with pytest.raises(ValidationError):
        load_orders(file)
