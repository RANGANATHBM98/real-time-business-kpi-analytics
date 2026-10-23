# Real-Time Business KPI Analytics

A small retail analytics project that generates transaction data, validates and summarizes it with pandas, stores it in SQLite, and provides a Power BI report. A local event simulator can append new transactions to the database and the CSV used by the report.

## Project Contents

| Path | Purpose |
| --- | --- |
| `src/generate_data.py` | Generate 1,000 sample retail transactions in `Data/transactions.csv`. |
| `src/analyze_data.py` | Inspect and validate the transactions, calculate business KPIs, and write `Data/cleaned_transactions.csv`. |
| `src/load_sql.py` | Create the SQLite table and load the cleaned transactions into `Data/business_kpi.db`. |
| `src/run_sql.py` | Print executive, category, regional, and daily revenue summaries from SQLite. |
| `src/stream_transactions.py` | Simulate 10 new transactions and append them to SQLite and the cleaned CSV. |
| `src/verify_stream.py` | Report total, live, and historical transaction counts in SQLite. |
| `sql/schema.sql` | Define the SQLite `transactions` table. |
| `sql/kpi_queries.sql` | Standalone SQL examples for common KPIs. |
| `Data/` | Sample CSV data and the SQLite database. |
| `powerbi/Real_Time_Business_KPI_Analytics.pbix` | Power BI Desktop report. |

## Requirements

- Python 3.10 or later
- Power BI Desktop to open and refresh the `.pbix` report
- Python package listed in `requirements.txt` (`pandas`); SQLite is included with Python

## Setup

From the project root in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run the scripts using `.\.venv\Scripts\python.exe` instead.

## Run the Analytics Pipeline

Run these commands from the project root, in order:

```powershell
python src/generate_data.py
python src/analyze_data.py
python src/load_sql.py
python src/run_sql.py
```

The analysis prints data-quality checks and KPIs including revenue, profit, order count, units sold, average order value, and profit margin. The SQL runner prints aggregate results by category, region, and date.

**Data reset behavior:** `generate_data.py` replaces `Data/transactions.csv`; `analyze_data.py` replaces `Data/cleaned_transactions.csv`; and `load_sql.py` replaces the SQLite `transactions` table with the cleaned CSV contents. Run the loader before streaming if you want to preserve newly simulated events.

## Simulate New Transactions

After completing the pipeline, run:

```powershell
python src/stream_transactions.py
python src/verify_stream.py
python src/run_sql.py
```

The simulator creates 10 events at 3-second intervals. It appends them to `Data/business_kpi.db` and `Data/cleaned_transactions.csv`, then the verification script reports live versus historical row counts. This is a local simulation, not a connection to a live sales system or message broker.

## Open the Power BI Report

Open `powerbi/Real_Time_Business_KPI_Analytics.pbix` in Power BI Desktop. The stream script appends rows to `Data/cleaned_transactions.csv` for the report; use **Refresh** in Power BI Desktop after running the stream. If the report requests its data source, select this workspace's `Data/cleaned_transactions.csv` file. The report is available as a downloadable `.pbix` in GitHub; GitHub does not render Power BI reports interactively.

## Data Fields

The transaction data includes transaction and order IDs, event time, product, category, region, channel, quantity, unit price, unit cost, discount percentage, revenue, and profit. Monetary values are in the sample data's configured currency (INR).