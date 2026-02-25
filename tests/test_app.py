import pandas as pd
from app import df


def test_data_loaded_successfully():
    """Verify the financial dataset loads as a non-empty DataFrame."""
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_expected_columns_present():
    """Verify key columns required by the app exist after loading."""
    expected = {"Year", "Company", "Category", "Net Profit Margin", "ROE", "ROA", "ROI", "Revenue", "Net Income", "EBITDA", "Current Ratio", "Debt/Equity Ratio"}
    assert expected.issubset(set(df.columns))