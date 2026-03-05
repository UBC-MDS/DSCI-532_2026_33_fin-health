"""Data loading, cleaning, and shared constants for the fin-health dashboard."""

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "financial_statement.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and clean the financial dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    data = pd.read_csv(path, encoding="utf-8-sig")
    data.columns = data.columns.str.strip()
    data["Category"] = data["Category"].str.upper()
    return data


df = load_data()

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
