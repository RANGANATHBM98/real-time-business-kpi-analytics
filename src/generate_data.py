import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# 1. Set the project data folder
DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
DATA_DIR.mkdir(exist_ok=True)

# 2. Define sample products
products = {
    "Laptop": {"category": "Electronics", "price": 55000, "cost": 42000},
    "Mouse": {"category": "Electronics", "price": 800, "cost": 350},
    "Keyboard": {"category": "Electronics", "price": 1500, "cost": 800},
    "Chair": {"category": "Furniture", "price": 6000, "cost": 4000},
    "Notebook": {"category": "Stationery", "price": 100, "cost": 45},
}

regions = ["South", "North", "East", "West"]
channels = ["Website", "Mobile App", "Retail"]

# 3. Generate 1,000 transactions
random.seed(42)
transactions = []

for i in range(1, 1001):
    product = random.choice(list(products.keys()))
    details = products[product]

    quantity = random.randint(1, 5)
    discount_pct = random.choice([0, 0.05, 0.10, 0.15])

    revenue = round(
        quantity * details["price"] * (1 - discount_pct), 2
    )
    profit = round(
        revenue - quantity * details["cost"], 2
    )

    transaction = {
        "transaction_id": f"TXN{i:05d}",
        "order_id": f"ORD{i:05d}",
        "event_time": (
            datetime.now() - timedelta(
                days=random.randint(0, 29),
                minutes=random.randint(0, 1439)
            )
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "product": product,
        "category": details["category"],
        "region": random.choice(regions),
        "channel": random.choice(channels),
        "quantity": quantity,
        "unit_price": details["price"],
        "unit_cost": details["cost"],
        "discount_pct": discount_pct,
        "revenue": revenue,
        "profit": profit,
    }

    transactions.append(transaction)

# 4. Convert records into a Pandas DataFrame
df = pd.DataFrame(transactions)

# 5. Save the dataset
output_file = DATA_DIR / "transactions.csv"
df.to_csv(output_file, index=False)

# 6. Display basic information
print("Dataset created successfully!")
print("Total transactions:", len(df))
print("Total revenue:", round(df["revenue"].sum(), 2))
print("Total profit:", round(df["profit"].sum(), 2))
print("\nFirst five transactions:")
print(df.head())
print("\nSaved to:", output_file)