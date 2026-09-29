"""Inställningar och konstanter."""

from dataclasses import dataclass
from pathlib import Path

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned",
]

# Dessa värden i kolumnen "returned" betyder att ordern är returnerad
TRUE_VALUES = ["true", "yes", "1", "ja"]


@dataclass(frozen=True)
class ReportConfig:
    """Vilken fil som läses och var rapporterna sparas."""

    input_path: Path = Path("data/orders.csv")
    output_dir: Path = Path("output")
