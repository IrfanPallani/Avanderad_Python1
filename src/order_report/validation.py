"""Kontroller av datan."""

from order_report.config import REQUIRED_COLUMNS


class ValidationError(Exception):
    """Datan går inte att använda."""


def check_columns(orders):
    """Alla obligatoriska kolumner måste finnas."""
    missing = [name for name in REQUIRED_COLUMNS if name not in orders.columns]
    if missing:
        raise ValidationError("Kolumner saknas: " + ", ".join(missing))


def check_not_empty(orders):
    """Det måste finnas minst en rad."""
    if orders.empty:
        raise ValidationError("Filen innehåller inga rader")


def check_values(orders):
    """Kontrollerar att värdena är rimliga. Ska köras efter rensningen."""
    if (orders["quantity"] <= 0).any():
        raise ValidationError("quantity måste vara större än 0")
    if (orders["unit_price"] <= 0).any():
        raise ValidationError("unit_price måste vara större än 0")
    if not orders["discount"].between(0, 1).all():
        raise ValidationError("discount måste vara mellan 0 och 1")
