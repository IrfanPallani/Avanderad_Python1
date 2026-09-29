"""Här startar programmet."""

import argparse
import logging
from pathlib import Path

from order_report.config import ReportConfig
from order_report.loading import load_orders
from order_report.processing import build_reports, clean_orders
from order_report.reporting import write_reports
from order_report.validation import (
    ValidationError,
    check_columns,
    check_not_empty,
    check_values,
)

logger = logging.getLogger(__name__)


def run(config):
    """Kör hela flödet: läs in, kontrollera, rensa, räkna och spara."""
    orders = load_orders(config.input_path)
    check_columns(orders)
    check_not_empty(orders)
    logger.info("Kontrollerade kolumner och att datan inte är tom")

    cleaned = clean_orders(orders)
    check_values(cleaned)

    reports = build_reports(cleaned)
    saved = write_reports(reports, config.output_dir)
    logger.info("Klart: %d rapporter sparade i %s", len(saved), config.output_dir)


def main(argv=None):
    """Startpunkt. Returnerar 0 om det gick bra och 1 om något var fel."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    defaults = ReportConfig()
    parser = argparse.ArgumentParser(description="Skapar orderrapporter från en CSV-fil.")
    parser.add_argument("--input", type=Path, default=defaults.input_path)
    parser.add_argument("--output-dir", type=Path, default=defaults.output_dir)
    args = parser.parse_args(argv)
    config = ReportConfig(input_path=args.input, output_dir=args.output_dir)

    try:
        run(config)
    except (FileNotFoundError, ValidationError) as error:
        logger.error("Kunde inte skapa rapporten: %s", error)
        return 1
    return 0
