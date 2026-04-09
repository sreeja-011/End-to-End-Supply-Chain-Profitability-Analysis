import json
from pathlib import Path


def md_cell(text: str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip("\n").split("\n")],
    }


def code_cell(code: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip("\n").split("\n")],
    }


title_md = """
# **END-TO-END SUPPLY CHAIN & PROFITABILITY ANALYSIS**

This project analyzes the Global Superstore dataset to evaluate supply chain performance and profitability.
The notebook follows a complete analytics workflow: data loading, cleaning, feature engineering, KPI development,
shipping efficiency analysis, profitability diagnostics, and business recommendations for Power BI reporting.
"""

cells = [
    md_cell(title_md),
    md_cell("**IMPORT NECESSARY LIBRARIES**"),
    code_cell(
        """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")
"""
    ),
    md_cell("**LOAD DATASET**"),
    code_cell(
        """
candidate_paths = [
    Path("data/Sample - Superstore.csv"),
    Path("Sample - Superstore.csv"),
    Path(r"C:/Users/Hp/Downloads/Sample - Superstore.csv"),
]

csv_path = next((p for p in candidate_paths if p.exists()), None)
if csv_path is None:
    raise FileNotFoundError(
        "Sample - Superstore.csv not found. Place it in data/ or project root."
    )

df = pd.read_csv(csv_path, encoding_errors="ignore")
print(f"Loaded: {csv_path}")
print(f"Shape: {df.shape}")
df.head()
"""
    ),
    md_cell("**INITIAL DATA UNDERSTANDING**"),
    code_cell(
        """
df.info()
"""
    ),
    code_cell(
        """
df.describe(include="all").T.head(15)
"""
    ),
    md_cell("**DATA CLEANING & PREPROCESSING**"),
    code_cell(
        """
# Standardize column names
df.columns = [c.strip() for c in df.columns]

# Date formatting
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Basic null check
nulls = df.isna().sum().sort_values(ascending=False)
nulls[nulls > 0]
"""
    ),
    code_cell(
        """
# Remove duplicate rows, if any
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"Duplicates removed: {before - after}")
"""
    ),
    md_cell("**FEATURE ENGINEERING**"),
    code_cell(
        """
# Delivery time in days
df["Delivery Time (Days)"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Profit margin percentage
df["Profit Margin %"] = np.where(df["Sales"] != 0, (df["Profit"] / df["Sales"]) * 100, 0)

# Year-Month for trend analysis
df["Order YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

df[["Order Date", "Ship Date", "Delivery Time (Days)", "Sales", "Profit", "Profit Margin %"]].head()
"""
    ),
    md_cell("**KPI DEVELOPMENT**"),
    code_cell(
        """
kpis = {
    "Total Sales": df["Sales"].sum(),
    "Total Profit": df["Profit"].sum(),
    "Overall Profit Margin %": (df["Profit"].sum() / df["Sales"].sum()) * 100,
    "Average Delivery Time (Days)": df["Delivery Time (Days)"].mean(),
    "Total Orders": df["Order ID"].nunique(),
    "Total Customers": df["Customer ID"].nunique(),
}

pd.DataFrame({"KPI": list(kpis.keys()), "Value": list(kpis.values())})
"""
    ),
    md_cell("**SHIPPING EFFICIENCY ANALYSIS**"),
    code_cell(
        """
shipping_eff = (
    df.groupby("Ship Mode", as_index=False)
      .agg(
          Avg_Delivery_Days=("Delivery Time (Days)", "mean"),
          Total_Orders=("Order ID", "nunique"),
          Total_Sales=("Sales", "sum"),
          Total_Profit=("Profit", "sum")
      )
      .sort_values("Avg_Delivery_Days")
)
shipping_eff
"""
    ),
    code_cell(
        """
plt.figure(figsize=(9, 5))
sns.barplot(data=shipping_eff, x="Ship Mode", y="Avg_Delivery_Days", palette="viridis")
plt.title("Average Delivery Time by Ship Mode")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()
"""
    ),
    md_cell("**PROFITABILITY ANALYSIS: REGIONS, CATEGORIES, PRODUCTS**"),
    code_cell(
        """
region_profit = (
    df.groupby("Region", as_index=False)
      .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
      .sort_values("Total_Profit")
)
region_profit
"""
    ),
    code_cell(
        """
loss_products = (
    df.groupby(["Product ID", "Product Name"], as_index=False)
      .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
      .query("Total_Profit < 0")
      .sort_values("Total_Profit")
)
loss_products.head(15)
"""
    ),
    code_cell(
        """
subcat_profit = (
    df.groupby("Sub-Category", as_index=False)
      .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
      .sort_values("Total_Profit")
)

fig = px.bar(
    subcat_profit,
    x="Sub-Category",
    y="Total_Profit",
    title="Profitability by Sub-Category",
    color="Total_Profit",
    color_continuous_scale="RdYlGn",
)
fig.update_layout(xaxis_tickangle=45)
fig.show()
"""
    ),
    md_cell("**TREND ANALYSIS**"),
    code_cell(
        """
monthly = (
    df.groupby("Order YearMonth", as_index=False)
      .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
)

fig = px.line(
    monthly,
    x="Order YearMonth",
    y=["Total_Sales", "Total_Profit"],
    title="Monthly Sales and Profit Trend",
)
fig.show()
"""
    ),
    md_cell("**POWER BI DASHBOARD PLANNING**"),
    code_cell(
        """
dashboard_tiles = [
    "KPI Cards: Total Sales, Total Profit, Profit Margin %, Avg Delivery Time",
    "Shipping Efficiency: Avg Delivery Time by Ship Mode",
    "Regional Performance: Sales vs Profit by Region",
    "Profitability Drilldown: Category > Sub-Category > Product",
    "Time Series: Monthly Sales and Profit",
]

pd.DataFrame({"Recommended Dashboard Components": dashboard_tiles})
"""
    ),
    md_cell("**BUSINESS INSIGHTS & RECOMMENDATIONS**"),
    code_cell(
        """
insights = [
    "Identify ship modes with high delivery days and low profitability for process redesign.",
    "Review persistent loss-making products and optimize pricing or discount strategy.",
    "Prioritize high-margin segments/regions for inventory and marketing allocation.",
    "Use monthly trend fluctuations to align procurement and logistics planning.",
]

for i, insight in enumerate(insights, start=1):
    print(f"{i}. {insight}")
"""
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

output = Path("notebooks/end_to_end_supply_chain_profitability_analysis.ipynb")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
print(f"Notebook created at: {output}")
