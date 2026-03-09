# Business Intelligence KPI Reporting and Data Validation System

## Project Overview

This project delivers a production-style Python pipeline for generating synthetic sales data, validating data quality, and computing monthly business KPIs. It is designed to demonstrate enterprise BI workflow patterns with clean, modular, and maintainable code.

## Business Problem

Business teams need timely and trustworthy reporting to make decisions. In many organizations, KPI dashboards are delayed or inaccurate because:

- source data quality is not validated early,
- reporting logic is not standardized,
- outputs are not generated in analyst-friendly formats.

This system addresses those issues by automating data generation, quality checks, and KPI reporting in a single repeatable pipeline.

## Technologies Used (and Why)

- `Python`: Core orchestration and data engineering language.
- `pandas`: Fast tabular processing, grouping, cleaning, and export capabilities.
- `numpy`: Efficient random data generation and numerical calculations.
- `openpyxl`: Excel output engine for KPI report delivery.
- `logging`: Structured execution and monitoring logs for traceability.

## Folder Structure

```text
bi_kpi_reporting_system/
|-- data/
|   `-- sales_data.csv                # Generated synthetic source data
|-- output/
|   |-- validation_report.csv         # Data quality results
|   `-- kpi_report.xlsx               # Monthly KPI report by month and region
|-- src/
|   |-- __init__.py
|   |-- data_generator.py             # Synthetic dataset creation
|   |-- data_validator.py             # Data quality validation checks
|   `-- kpi_calculator.py             # Data cleaning and KPI computation
|-- main.py                           # Pipeline entry point
|-- requirements.txt
`-- README.md
```

## How to Install Dependencies

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## How to Run Locally

From the project root:

```bash
python main.py
```

The pipeline will execute in this order:

1. Generate synthetic sales data in `data/sales_data.csv`
2. Validate the dataset and write `output/validation_report.csv`
3. Calculate monthly KPIs and write `output/kpi_report.xlsx`

## Expected Outputs

- `data/sales_data.csv`
  - Contains at least 1000 records
  - Columns: `Date`, `Product`, `Region`, `Sales_Amount`, `Units_Sold`

- `output/validation_report.csv`
  - Quality checks:
    - Missing values
    - Duplicate rows
    - Negative sales amounts
    - Invalid dates
  - Includes issue counts and pass/fail status

- `output/kpi_report.xlsx`
  - Grouped by `Month` and `Region`
  - KPI metrics:
    - Total Sales
    - Total Units Sold
    - Average Sales per Unit

## Example Business Insights

After running the pipeline, stakeholders can quickly answer questions such as:

- Which regions consistently deliver the highest monthly revenue?
- Are units sold increasing while average selling value declines?
- Which months show unusual dips or spikes in sales performance?
- Does data quality impact reporting reliability over time?

## Engineering Quality Highlights

- Modular architecture with focused responsibilities per module.
- Reusable functions with explicit inputs and outputs.
- Type hints, docstrings, and clean naming conventions.
- Structured logging for operational transparency.
- Output artifacts aligned with analyst and management consumption patterns.
