"""Data loading, cleaning, and shared constants for the fin-health dashboard."""

from pathlib import Path

import ibis

PARQUET_PATH = (
    Path(__file__).parent.parent / "data" / "processed" / "financial_statement.parquet"
)

# --- ibis / DuckDB connection ---
con = ibis.duckdb.connect()
tbl = con.read_parquet(str(PARQUET_PATH))

# Full pandas DataFrame (used by querychat and chart builders)
df = tbl.to_pandas()

# Year range (computed once from ibis, avoids scanning pandas)
YEAR_MIN = int(tbl["Year"].min().execute())
YEAR_MAX = int(tbl["Year"].max().execute())

CATEGORY_COMPANIES = {
    "BANK": ["AIG", "BCS"],
    "ELEC": ["INTC", "NVDA"],
    "FINANCE": ["SHLDQ"],
    "FINTECH": ["PYPL"],
    "FOOD": ["MCD"],
    "IT": ["AAPL", "GOOG", "MSFT"],
    "LOGI": ["AMZN"],
    "MANUFACTURING": ["PCG"],
}
ALL_SECTORS = sorted(CATEGORY_COMPANIES.keys())

METRIC_CHOICES = {
    "Net Profit Margin": "%",
    "ROE": "%",
    "ROA": "%",
    "ROI": "%",
    "Revenue": "USD",
    "Net Income": "USD",
    "EBITDA": "USD",
    "Current Ratio": "",
    "Debt/Equity Ratio": "",
}
