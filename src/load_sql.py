import sqlite3
import pandas as pd
from pathlib import Path

# 1. Find project files
BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "Data" / "cleaned_transactions.csv"
DB_FILE = BASE_DIR / "Data" / "business_kpi.db"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"

# 2. Read the cleaned dataset
df = pd.read_csv(CSV_FILE)

# 3. Create a database connection
connection = sqlite3.connect(DB_FILE)

try:
    # 4. Create the SQL table
    schema = SCHEMA_FILE.read_text(encoding="utf-8")
    connection.executescript(schema)

    # 5. Load the dataset into the table
    df.to_sql(
        "transactions",
        connection,
        if_exists="replace",
        index=False
    )

    print("Dataset loaded successfully!")

    # 6. Verify how many rows were loaded
    result = pd.read_sql_query(
        "SELECT COUNT(*) AS total_rows FROM transactions",
        connection
    )

    print(result)

finally:
    connection.close()