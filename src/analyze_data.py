import pandas as pd
from pathlib import Path

# 1. Locate and load the dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "Data" / "transactions.csv"

df = pd.read_csv(DATA_FILE)

print("========== DATASET OVERVIEW ==========")

# 2. Check dataset size
print("Rows and columns:", df.shape)

# 3. Inspect column names and data types
print("\nColumn names:")
print(df.columns.tolist())

print("\nData types and non-null counts:")
df.info()

# 4. Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# 5. Check duplicate records
print("\nDuplicate rows:", df.duplicated().sum())

# 6. Validate transaction IDs
print("Duplicate transaction IDs:", df["transaction_id"].duplicated().sum())

# 7. Convert event_time to datetime
df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")

# 8. Validate business calculations
expected_revenue = (
    df["quantity"] * df["unit_price"] * (1 - df["discount_pct"])
).round(2)

expected_profit = (
    expected_revenue - df["quantity"] * df["unit_cost"]
).round(2)

print(
    "\nIncorrect revenue calculations:",
    (df["revenue"] - expected_revenue).abs().gt(0.01).sum()
)
print(
    "Incorrect profit calculations:",
    (df["profit"] - expected_profit).abs().gt(0.01).sum()
)

# 9. Calculate key business KPIs
total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
total_orders = df["order_id"].nunique()
units_sold = df["quantity"].sum()

average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

profit_margin = (
    total_profit / total_revenue * 100 if total_revenue else 0
)

print("\n========== BUSINESS KPIs ==========")
print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Units Sold: {units_sold}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")

# 10. Analyze performance by category
print("\n========== CATEGORY PERFORMANCE ==========")

category_summary = df.groupby("category").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    units_sold=("quantity", "sum")
).round(2)

print(category_summary.sort_values("revenue", ascending=False))

# 11. Save the cleaned dataset
CLEAN_FILE = BASE_DIR / "Data" / "cleaned_transactions.csv"

df.to_csv(CLEAN_FILE, index=False)

print("\nCleaned dataset saved to:", CLEAN_FILE)