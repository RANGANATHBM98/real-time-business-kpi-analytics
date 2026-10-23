import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "Data" / "business_kpi.db"

connection = sqlite3.connect(DB_FILE)

queries = {
    "Executive KPIs": """
        SELECT
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS total_orders,
            SUM(quantity) AS units_sold
        FROM transactions
    """,

    "Category Performance": """
        SELECT category,
               ROUND(SUM(revenue), 2) AS total_revenue,
               ROUND(SUM(profit), 2) AS total_profit
        FROM transactions
        GROUP BY category
        ORDER BY total_revenue DESC
    """,

    "Regional Performance": """
        SELECT region,
               ROUND(SUM(revenue), 2) AS total_revenue,
               ROUND(SUM(profit), 2) AS total_profit
        FROM transactions
        GROUP BY region
        ORDER BY total_revenue DESC
    """,

    "Daily Revenue": """
        SELECT DATE(event_time) AS sales_date,
               ROUND(SUM(revenue), 2) AS daily_revenue
        FROM transactions
        GROUP BY DATE(event_time)
        ORDER BY sales_date
    """
}

try:
    for title, query in queries.items():
        print(f"\n===== {title} =====")
        cursor = connection.execute(query)

        print(" | ".join(column[0] for column in cursor.description))

        for row in cursor.fetchall():
            print(row)

finally:
    connection.close()