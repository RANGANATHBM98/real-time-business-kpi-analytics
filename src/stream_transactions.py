
import csv
import random
import sqlite3
import time
import uuid

from datetime import datetime
from pathlib import Path

# 1. Locate the project files
BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = BASE_DIR / "Data" / "business_kpi.db"
CSV_FILE = BASE_DIR / "Data" / "cleaned_transactions.csv"

# 2. Define available products
PRODUCTS = {
    "Laptop": {
        "category": "Electronics",
        "price": 55000,
        "cost": 42000,
    },
    "Mouse": {
        "category": "Electronics",
        "price": 800,
        "cost": 350,
    },
    "Keyboard": {
        "category": "Electronics",
        "price": 1500,
        "cost": 800,
    },
    "Chair": {
        "category": "Furniture",
        "price": 6000,
        "cost": 4000,
    },
    "Notebook": {
        "category": "Stationery",
        "price": 100,
        "cost": 45,
    },
}

REGIONS = ["South", "North", "East", "West"]
CHANNELS = ["Website", "Mobile App", "Retail"]

# 3. Configure the stream
TOTAL_EVENTS = 10
INTERVAL_SECONDS = 3


def generate_event():
    """Generate one new transaction event."""

    product = random.choice(list(PRODUCTS.keys()))
    details = PRODUCTS[product]

    quantity = random.randint(1, 5)
    discount_pct = random.choice([0, 0.05, 0.10, 0.15])

    revenue = round(
        quantity * details["price"] * (1 - discount_pct), 2
    )

    profit = round(
        revenue - quantity * details["cost"], 2
    )

    # Unique ID prevents collisions with historical transaction IDs
    transaction_id = f"LIVE_{uuid.uuid4().hex[:12].upper()}"

    event = {
        "transaction_id": transaction_id,
        "order_id": f"ORD_{transaction_id}",
        "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product": product,
        "category": details["category"],
        "region": random.choice(REGIONS),
        "channel": random.choice(CHANNELS),
        "quantity": quantity,
        "unit_price": details["price"],
        "unit_cost": details["cost"],
        "discount_pct": discount_pct,
        "revenue": revenue,
        "profit": profit,
    }

    return event


def save_event(connection, event):
    """Insert an event into SQLite and append it to the CSV."""

    columns = list(event.keys())
    placeholders = ", ".join(["?"] * len(columns))
    column_names = ", ".join(columns)

    sql = (
        f"INSERT INTO transactions ({column_names}) "
        f"VALUES ({placeholders})"
    )

    # Insert into SQLite without replacing historical records
    with connection:
        connection.execute(sql, list(event.values()))

    # Append to the CSV used by the existing Power BI report
    file_exists = CSV_FILE.exists()
    needs_header = not file_exists or CSV_FILE.stat().st_size == 0

    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)

        if needs_header:
            writer.writeheader()

        writer.writerow(event)


def main():
    if not DB_FILE.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_FILE}. "
            "Run src/load_sql.py first."
        )

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV not found: {CSV_FILE}. "
            "Run the data preparation scripts first."
        )

    print("Starting simulated transaction stream...")
    print("Historical records will not be replaced.")
    print(f"Events to generate: {TOTAL_EVENTS}")
    print("-" * 55)

    with sqlite3.connect(DB_FILE) as connection:
        for number in range(1, TOTAL_EVENTS + 1):
            event = generate_event()

            # Basic business validation
            if event["quantity"] <= 0 or event["revenue"] < 0:
                print("Invalid event skipped.")
                continue

            save_event(connection, event)

            print(
                f"{number}/{TOTAL_EVENTS} | "
                f"{event['transaction_id']} | "
                f"{event['product']} | "
                f"Revenue: {event['revenue']:.2f} | "
                f"Profit: {event['profit']:.2f}"
            )

            if number < TOTAL_EVENTS:
                time.sleep(INTERVAL_SECONDS)

    print("-" * 55)
    print("Stream finished successfully.")


if __name__ == "__main__":
    main()
