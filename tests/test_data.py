import ibis
import pandas as pd
from data import (
    df,
    tbl,
    con,
    ALL_SECTORS,
    METRIC_CHOICES,
    CATEGORY_COMPANIES,
    YEAR_MIN,
    YEAR_MAX,
)


def test_connection_is_duckdb():
    """Verify the ibis connection uses the DuckDB backend."""
    assert isinstance(con, ibis.backends.duckdb.Backend)


def test_tbl_is_ibis_table():
    """Verify tbl is an ibis Table expression."""
    assert isinstance(tbl, ibis.expr.types.Table)


def test_df_is_pandas_dataframe():
    """Verify df is a non-empty pandas DataFrame materialized from ibis."""
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


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


def test_ibis_filter_returns_subset():
    """Verify ibis filtering works and returns fewer rows than full table."""
    filtered = tbl.filter(tbl["Category"] == "IT").to_pandas()
    assert len(filtered) > 0
    assert len(filtered) < len(df)
    assert set(filtered["Category"].unique()) == {"IT"}


def test_year_range_constants():
    """Verify YEAR_MIN and YEAR_MAX match the actual data."""
    assert YEAR_MIN == int(df["Year"].min())
    assert YEAR_MAX == int(df["Year"].max())


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
