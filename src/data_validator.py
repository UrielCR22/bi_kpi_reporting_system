"""Validate sales data quality and export validation reports."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd


LOGGER = logging.getLogger(__name__)


def _project_root() -> Path:
    """Return the project root path from this module location."""
    return Path(__file__).resolve().parents[1]


def validate_sales_data(input_csv: Path | None = None, report_csv: Path | None = None) -> pd.DataFrame:
    """Run quality checks on sales data and save a validation report.

    Checks performed:
    - Missing values
    - Duplicate rows
    - Negative sales amounts
    - Invalid dates

    Args:
        input_csv: Optional source CSV path.
        report_csv: Optional report CSV output path.

    Returns:
        DataFrame containing validation summary metrics.
    """
    input_path = input_csv or _project_root() / "data" / "sales_data.csv"
    report_path = report_csv or _project_root() / "output" / "validation_report.csv"

    LOGGER.info("Reading dataset for validation from %s", input_path)
    df = pd.read_csv(input_path)

    original_date = df["Date"].copy()
    parsed_dates = pd.to_datetime(df["Date"], errors="coerce")

    missing_values_count = int(df.isna().sum().sum())
    duplicate_rows_count = int(df.duplicated().sum())
    negative_sales_count = int((pd.to_numeric(df["Sales_Amount"], errors="coerce") < 0).sum())
    invalid_dates_count = int(parsed_dates.isna().sum() - original_date.isna().sum())

    validation_summary = pd.DataFrame(
        [
            {
                "Check": "Missing Values",
                "Issue_Count": missing_values_count,
                "Status": "PASS" if missing_values_count == 0 else "FAIL",
            },
            {
                "Check": "Duplicate Rows",
                "Issue_Count": duplicate_rows_count,
                "Status": "PASS" if duplicate_rows_count == 0 else "FAIL",
            },
            {
                "Check": "Negative Sales Amount",
                "Issue_Count": negative_sales_count,
                "Status": "PASS" if negative_sales_count == 0 else "FAIL",
            },
            {
                "Check": "Invalid Dates",
                "Issue_Count": invalid_dates_count,
                "Status": "PASS" if invalid_dates_count == 0 else "FAIL",
            },
        ]
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    validation_summary.to_csv(report_path, index=False)

    LOGGER.info("Validation completed. Report saved to %s", report_path)
    LOGGER.info("Validation results:\n%s", validation_summary.to_string(index=False))

    return validation_summary
