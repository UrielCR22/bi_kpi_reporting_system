"""Entry point for the BI KPI reporting and validation pipeline."""

from __future__ import annotations

import logging
from pathlib import Path

from src.data_generator import generate_and_save_sales_data
from src.data_validator import validate_sales_data
from src.kpi_calculator import generate_kpi_report


def configure_logging() -> None:
    """Configure consistent logging format for the pipeline."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main() -> None:
    """Execute the full data pipeline end to end."""
    configure_logging()
    project_root = Path(__file__).resolve().parent

    print("Starting BI KPI Reporting and Data Validation pipeline...")

    print("1/3 Generating synthetic sales data...")
    sales_path = generate_and_save_sales_data(num_rows=1500, random_seed=42)
    print(f"   Sales dataset generated: {sales_path.relative_to(project_root)}")

    print("2/3 Validating data quality...")
    validation_df = validate_sales_data()
    print("   Validation complete. Summary:")
    print(validation_df.to_string(index=False))

    print("3/3 Calculating monthly KPIs...")
    kpi_path = generate_kpi_report()
    print(f"   KPI report generated: {kpi_path.relative_to(project_root)}")

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
