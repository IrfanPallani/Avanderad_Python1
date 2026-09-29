"""Sparar rapporterna som CSV-filer."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_reports(reports, output_dir):
    """Sparar varje rapport som <namn>.csv. Skapar mappen om den saknas."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for name, table in reports.items():
        path = output_dir / f"{name}.csv"
        table.to_csv(path, index=False)
        logger.info("Sparade %s", path)
        saved.append(path)
    return saved
