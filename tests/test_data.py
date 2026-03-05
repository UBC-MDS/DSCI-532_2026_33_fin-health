import pandas as pd
from data import df, load_data, ALL_SECTORS, METRIC_CHOICES, CATEGORY_COMPANIES


def test_load_data_returns_dataframe():
    """Verify load_data() returns a non-empty DataFrame."""
    result = load_data()
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0


def test_expected_columns_present():
    """Verify key columns required by the app exist after loading."""
    expected = {
        "Year",
        "Company",
        "Category",
        "Net Profit Margin",
        "ROE",
        "ROA",
        "ROI",
        "Revenue",
        "Net Income",
        "EBITDA",
        "Current Ratio",
        "Debt/Equity Ratio",
    }
    assert expected.issubset(set(df.columns))


def test_all_sectors_sorted():
    """Verify ALL_SECTORS is a sorted list of category keys."""
    assert ALL_SECTORS == sorted(CATEGORY_COMPANIES.keys())


def test_metric_choices_non_empty():
    """Verify METRIC_CHOICES contains expected metrics."""
    assert len(METRIC_CHOICES) > 0
    assert "Net Profit Margin" in METRIC_CHOICES
    assert "Revenue" in METRIC_CHOICES


def test_category_companies_has_entries():
    """Verify CATEGORY_COMPANIES maps sectors to company lists."""
    assert len(CATEGORY_COMPANIES) > 0
    for sector, companies in CATEGORY_COMPANIES.items():
        assert isinstance(companies, list)
        assert len(companies) > 0
