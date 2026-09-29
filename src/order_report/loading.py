"""Läser in orderfilen."""

import logging
from pathlib import Path

import pandas as pd

from order_report.validation import ValidationError

logger = logging.getLogger(__name__)


def load_orders(path):
    """Läser CSV-filen och returnerar en DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Hittar inte filen: {path}")

    try:
        orders = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ValidationError(f"Filen är tom: {path}")

    logger.info("Läste in %d rader från %s", len(orders), path)
    return orders
