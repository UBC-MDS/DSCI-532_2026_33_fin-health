import pandas as pd
from app import DATA_PATH, load_data


def test_data_loaded_successfully():
    """Verify the financial dataset loads as a non-empty DataFrame."""
    df = load_data(DATA_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_expected_columns_present():
    """Verify key columns required by the app exist after loading."""
    df = load_data(DATA_PATH)
    expected = {"Year", "Company", "Category", "Net Profit Margin", "ROE", "ROA", "ROI", "Revenue", "Net Income", "EBITDA", "Current Ratio", "Debt/Equity Ratio"}
    assert expected.issubset(set(df.columns))