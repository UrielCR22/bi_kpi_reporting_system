"""Generate synthetic sales data for BI reporting pipelines."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd


LOGGER = logging.getLogger(__name__)


def _project_root() -> Path:
    """Return the project root path from this module location."""
    return Path(__file__).resolve().parents[1]


def generate_sales_data(num_rows: int = 1500, random_seed: int = 42) -> pd.DataFrame:
    """Create a realistic synthetic sales dataset.

    Args:
        num_rows: Number of records to generate.
        random_seed: Seed used to make outputs reproducible.

    Returns:
        DataFrame with Date, Product, Region, Sales_Amount, and Units_Sold columns.
    """
    rng = np.random.default_rng(random_seed)

    product_catalog = {
        "Laptop": 1200,
        "Tablet": 500,
        "Smartphone": 850,
        "Monitor": 300,
        "Keyboard": 65,
        "Headphones": 120,
    }
    products = list(product_catalog.keys())
    regions = ["North", "South", "East", "West", "Central"]

    end_date = pd.Timestamp.today().normalize()
    start_date = end_date - pd.Timedelta(days=730)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    sampled_products = rng.choice(products, size=num_rows, replace=True)
    sampled_regions = rng.choice(regions, size=num_rows, replace=True, p=[0.22, 0.18, 0.2, 0.2, 0.2])
    sampled_dates = rng.choice(date_range, size=num_rows, replace=True)
    units_sold = rng.integers(1, 40, size=num_rows)

    base_prices = np.array([product_catalog[item] for item in sampled_products], dtype=float)
    regional_factor_map = {"North": 1.04, "South": 0.96, "East": 1.02, "West": 1.0, "Central": 0.98}
    regional_factors = np.array([regional_factor_map[item] for item in sampled_regions], dtype=float)
    noise = rng.normal(loc=1.0, scale=0.08, size=num_rows)

    sales_amount = base_prices * regional_factors * units_sold * noise
    sales_amount = np.clip(sales_amount, 1, None)

    sales_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(sampled_dates).strftime("%Y-%m-%d"),
            "Product": sampled_products,
            "Region": sampled_regions,
            "Sales_Amount": np.round(sales_amount, 2),
            "Units_Sold": units_sold,
        }
    )

    LOGGER.info("Generated synthetic sales dataset with %s rows.", len(sales_df))
    return sales_df


def save_sales_data(dataframe: pd.DataFrame, file_path: Path | None = None) -> Path:
    """Save generated sales data to CSV.

    Args:
        dataframe: Sales DataFrame to save.
        file_path: Optional custom output path.

    Returns:
        Path where the file was saved.
    """
    output_path = file_path or _project_root() / "data" / "sales_data.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)
    LOGGER.info("Saved sales data to %s", output_path)
    return output_path


def generate_and_save_sales_data(num_rows: int = 1500, random_seed: int = 42) -> Path:
    """Generate and persist the synthetic sales dataset in one step."""
    sales_df = generate_sales_data(num_rows=num_rows, random_seed=random_seed)
    return save_sales_data(sales_df)
