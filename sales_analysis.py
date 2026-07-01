"""
Project 1: Sales Data Analysis Dashboard
Loads, cleans, and analyzes the sales dataset, then exports summary
JSON files that power the interactive dashboard (dashboard.html).
"""
import pandas as pd
import numpy as np
import json

# ---------- 1. LOAD ----------
df = pd.read_csv("sales_data.csv")
print("Raw shape:", df.shape)
print(df.dtypes)

# ---------- 2. CLEAN ----------
# Remove exact duplicates
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

# Fix inconsistent date formats (mix of YYYY-MM-DD and MM/DD/YYYY)
df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=False)

# Handle missing values
df["Sales"] = df["Sales"].fillna(df.groupby("Category")["Sales"].transform("median"))
df["Region"] = df["Region"].fillna("Unknown")

# Derived columns
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.to_period("M").astype(str)
df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(3)

print("Clean shape:", df.shape)
print("Missing values after cleaning:\n", df.isna().sum())

# ---------- 3. ANALYZE KEY METRICS ----------
total_sales = round(df["Sales"].sum(), 2)
total_profit = round(df["Profit"].sum(), 2)
avg_margin = round(df["Profit Margin"].mean(), 3)
top_products = (df.groupby("Product")["Sales"].sum()
                 .sort_values(ascending=False).round(2).to_dict())
best_regions = (df.groupby("Region")["Sales"].sum()
                 .sort_values(ascending=False).round(2).to_dict())
category_split = (df.groupby("Category")["Sales"].sum().round(2).to_dict())

# ---------- 4. TRENDS ----------
monthly_trend = (df.groupby("Month").agg(Sales=("Sales", "sum"),
                                          Profit=("Profit", "sum"))
                  .round(2).reset_index().sort_values("Month"))
yearly_trend = (df.groupby("Year").agg(Sales=("Sales", "sum"),
                                        Profit=("Profit", "sum"))
                 .round(2).reset_index())

# ---------- 5. EXPORT for dashboard ----------
export = {
    "kpis": {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_margin": avg_margin,
        "orders": int(len(df))
    },
    "top_products": top_products,
    "best_regions": best_regions,
    "category_split": category_split,
    "monthly_trend": monthly_trend.to_dict(orient="records"),
    "yearly_trend": yearly_trend.to_dict(orient="records"),
    "raw_records": df[["Order ID", "Product", "Category", "Sales", "Profit",
                        "Date", "Region", "Month"]].assign(
        Date=lambda x: x["Date"].dt.strftime("%Y-%m-%d")
    ).to_dict(orient="records")
}

with open("dashboard_data.json", "w") as f:
    json.dump(export, f, indent=2)

df.to_csv("sales_data_clean.csv", index=False)

print("\n=== KPIs ===")
print(export["kpis"])
print("\nTop 3 products by sales:", list(top_products.items())[:3])
print("Best region:", list(best_regions.items())[0])
print("\nExported dashboard_data.json and sales_data_clean.csv")
