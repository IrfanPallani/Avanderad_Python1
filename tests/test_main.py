from pathlib import Path

import pytest

from order_report.main import main

TESTS_DIR = Path(__file__).parent
ORDERS_CSV = TESTS_DIR.parent / "data" / "orders.csv"
EXPECTED_DIR = TESTS_DIR / "expected"
REPORT_FILES = [
    "overview.csv",
    "sales_by_category.csv",
    "sales_by_region.csv",
    "returns_by_category.csv",
]


@pytest.mark.parametrize("filename", REPORT_FILES)
def test_reports_are_same_as_from_original_program(tmp_path, filename):
    """Filerna i tests/expected skapades genom att köra originalskriptet.
    Testet visar att refaktoreringen inte ändrat resultaten."""
    main(["--input", str(ORDERS_CSV), "--output-dir", str(tmp_path)])

    result = (tmp_path / filename).read_text()
    expected = (EXPECTED_DIR / filename).read_text()
    assert result == expected


def test_main_returns_0_when_all_is_ok(tmp_path):
    code = main(["--input", str(ORDERS_CSV), "--output-dir", str(tmp_path)])
    assert code == 0


def test_main_returns_1_if_file_is_missing(tmp_path):
    code = main(["--input", str(tmp_path / "saknas.csv"), "--output-dir", str(tmp_path)])
    assert code == 1


def test_main_returns_1_and_saves_nothing_if_column_is_missing(tmp_path):
    bad_file = tmp_path / "bad.csv"
    bad_file.write_text("order_id,region\nO1,North\n")
    output_dir = tmp_path / "ut"

    code = main(["--input", str(bad_file), "--output-dir", str(output_dir)])

    assert code == 1
    assert not output_dir.exists()
