"""Clean sales data and compute monthly KPI reports."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd


LOGGER = logging.getLogger(__name__)


def _project_root() -> Path:
    """Return the project root path from this module location."""
    return Path(__file__).resolve().parents[1]


def clean_sales_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Apply standard cleaning rules before KPI calculation."""
    df = dataframe.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales_Amount"] = pd.to_numeric(df["Sales_Amount"], errors="coerce")
    df["Units_Sold"] = pd.to_numeric(df["Units_Sold"], errors="coerce")

    initial_rows = len(df)
    df = df.dropna(subset=["Date", "Product", "Region", "Sales_Amount", "Units_Sold"])
    df = df.drop_duplicates()
    df = df[(df["Sales_Amount"] >= 0) & (df["Units_Sold"] > 0)]

    dropped_rows = initial_rows - len(df)
    LOGGER.info("Data cleaning removed %s invalid rows.", dropped_rows)

    return df


def calculate_monthly_kpis(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly KPI metrics grouped by month and region."""
    df = clean_df.copy()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    kpi_df = (
        df.groupby(["Month", "Region"], as_index=False)
        .agg(
            Total_Sales=("Sales_Amount", "sum"),
            Total_Units_Sold=("Units_Sold", "sum"),
        )
        .sort_values(by=["Month", "Region"])
    )

    kpi_df["Average_Sales_per_Unit"] = np.where(
        kpi_df["Total_Units_Sold"] > 0,
        kpi_df["Total_Sales"] / kpi_df["Total_Units_Sold"],
        0,
    )

    kpi_df["Total_Sales"] = kpi_df["Total_Sales"].round(2)
    kpi_df["Average_Sales_per_Unit"] = kpi_df["Average_Sales_per_Unit"].round(2)

    LOGGER.info("Calculated %s monthly KPI rows.", len(kpi_df))
    return kpi_df


def generate_kpi_report(input_csv: Path | None = None, output_excel: Path | None = None) -> Path:
    """Load sales data, compute KPIs, and export the report to Excel."""
    input_path = input_csv or _project_root() / "data" / "sales_data.csv"
    output_path = output_excel or _project_root() / "output" / "kpi_report.xlsx"

    LOGGER.info("Reading sales data for KPI computation from %s", input_path)
    raw_df = pd.read_csv(input_path)
    clean_df = clean_sales_data(raw_df)
    kpi_df = calculate_monthly_kpis(clean_df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        kpi_df.to_excel(writer, sheet_name="Monthly_KPI_Report", index=False)

    LOGGER.info("KPI report exported to %s", output_path)
    return output_path
