CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    event_time TEXT NOT NULL,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    region TEXT NOT NULL,
    channel TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    unit_cost REAL NOT NULL,
    discount_pct REAL NOT NULL,
    revenue REAL NOT NULL,
    profit REAL NOT NULL
);