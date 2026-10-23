import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "Data" / "business_kpi.db"

connection = sqlite3.connect(DB_FILE)

try:
    total = connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    live = connection.execute(
        "SELECT COUNT(*) FROM transactions "
        "WHERE transaction_id LIKE 'LIVE_%'"
    ).fetchone()[0]

    print("Total transactions:", total)
    print("Live transactions:", live)
    print("Historical transactions:", total - live)

finally:
    connection.close()