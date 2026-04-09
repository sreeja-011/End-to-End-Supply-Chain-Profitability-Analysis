# End-to-End Supply Chain & Profitability Analysis

## Project Overview
This project analyzes the Global Superstore dataset to evaluate supply chain performance and business profitability.
It includes data cleaning, feature engineering, KPI development, shipping efficiency diagnostics, and profitability analysis by region and product hierarchy.

## Objectives
- Analyze Superstore operations with a focus on supply chain and profitability.
- Clean and preprocess data, including date formatting and duplicate handling.
- Engineer features such as delivery time and profit margin.
- Build KPIs like total sales, profit margin, and average delivery time.
- Evaluate shipping efficiency across shipping modes.
- Detect loss-making products, sub-categories, and regions.
- Prepare outputs for interactive Power BI dashboards.
- Provide SQL queries for reproducible metric calculation.

## Project Structure
- `data/` - Dataset assets and metadata.
- `notebooks/end_to_end_supply_chain_profitability_analysis.ipynb` - Main analysis notebook.
- `sql/superstore_kpi_queries.sql` - KPI and diagnostic SQL queries.
- `scripts/generate_notebook.py` - Script used to generate the notebook.

## Dataset
- Metadata source path provided by you: `C:/Users/Hp/Downloads/superstore-dataset-final-metadata.json`
- Expected CSV file: `Sample - Superstore.csv`
  - Put it in `data/` or project root.
  - The notebook also tries `C:/Users/Hp/Downloads/Sample - Superstore.csv`.

## Tools Used
- Python (Pandas, NumPy, Seaborn, Matplotlib, Plotly)
- SQL
- Power BI (dashboard layer)

## How to Run
1. Install dependencies:
   - `pip install -r requirements.txt`
2. Ensure CSV exists at one of the supported paths.
3. Open and run:
   - `notebooks/end_to_end_supply_chain_profitability_analysis.ipynb`

## Key Outcomes
- Operational KPI framework for sales, profit, and delivery performance.
- Shipping-mode level efficiency view with delivery-time benchmarking.
- Profitability hotspot and risk view across regions, categories, and products.
- Dashboard-ready analytical model for executive reporting.
