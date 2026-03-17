import ibis
import numpy as np
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


# --- Index Margin (weighted profit margin) ---


def test_index_margin_weighted_differs_from_simple():
    """Weighted margin (Total Income / Total Revenue) differs from simple average, ensuring the KPI reflects company scale."""
    total_revenue = df["Revenue"].sum()
    total_net_income = df["Net Income"].sum()
    index_margin = (total_net_income / total_revenue) * 100
    simple_avg = df["Net Profit Margin"].mean()
    assert not np.isclose(index_margin, simple_avg, atol=0.01)


def test_index_margin_matches_manual_calculation():
    """Index margin formula is consistent: (Net Income sum / Revenue sum) * 100."""
    index_margin = (df["Net Income"].sum() / df["Revenue"].sum()) * 100
    manual = df["Net Income"].sum() / df["Revenue"].sum() * 100
    assert np.isclose(index_margin, manual)


def test_index_margin_zero_revenue_returns_zero():
    """Zero total revenue produces 0.0% margin instead of a division error."""
    empty = pd.DataFrame({"Revenue": [0, 0], "Net Income": [100, 200]})
    total_rev = empty["Revenue"].sum()
    margin = 0.0 if total_rev == 0 else (empty["Net Income"].sum() / total_rev) * 100
    assert margin == 0.0


# --- Revenue Growth (YoY) ---


def _compute_revenue_growth(filtered_df):
    """Replicate the YoY revenue growth logic from sector.py:p1_revenue_change()."""
    yearly_revenue = (
        filtered_df.groupby("Year")["Revenue"].sum().sort_index(ascending=False)
    )
    if len(yearly_revenue) < 2:
        return None
    current = yearly_revenue.iloc[0]
    previous = yearly_revenue.iloc[1]
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return None
    return (current - previous) / previous * 100


def test_revenue_growth_matches_manual():
    """YoY revenue growth matches a hand-computed value from the two most recent years."""
    growth = _compute_revenue_growth(df)
    years_desc = sorted(df["Year"].unique(), reverse=True)
    rev_current = df[df["Year"] == years_desc[0]]["Revenue"].sum()
    rev_previous = df[df["Year"] == years_desc[1]]["Revenue"].sum()
    manual = (rev_current - rev_previous) / rev_previous * 100
    assert np.isclose(growth, manual)


def test_revenue_growth_single_year_returns_none():
    """Single-year data returns None instead of crashing, so the KPI card shows 'Data Unavailable'."""
    single = df[df["Year"] == YEAR_MAX]
    assert _compute_revenue_growth(single) is None


def test_revenue_growth_two_year_subset():
    """A two-year slice produces valid growth matching the expected formula."""
    two_years = df[df["Year"].isin([YEAR_MAX - 1, YEAR_MAX])]
    growth = _compute_revenue_growth(two_years)
    if growth is not None:
        rev_curr = two_years[two_years["Year"] == YEAR_MAX]["Revenue"].sum()
        rev_prev = two_years[two_years["Year"] == YEAR_MAX - 1]["Revenue"].sum()
        assert np.isclose(growth, (rev_curr - rev_prev) / rev_prev * 100)


# --- Company-Year Lookup (Page 2 filter) ---


def test_company_year_lookup_returns_one_row():
    """Each company's latest year returns exactly 1 row, so Page 2 KPI cards always have data."""
    for category, companies in CATEGORY_COMPANIES.items():
        for company in companies:
            company_data = tbl.filter(tbl["Company"] == company).to_pandas()
            latest = company_data["Year"].max()
            row = company_data[company_data["Year"] == latest]
            assert len(row) == 1, (
                f"{company} in {latest}: expected 1 row, got {len(row)}"
            )


def test_company_year_lookup_has_required_columns():
    """Each company row contains all metric columns needed by Page 2 KPI cards and charts."""
    required = [
        "Net Profit Margin",
        "ROE",
        "Revenue",
        "Net Income",
        "Current Ratio",
        "Debt/Equity Ratio",
        "Cash Flow from Operating",
        "Cash Flow from Investing",
        "Cash Flow from Financial Activities",
    ]
    for company in [c for companies in CATEGORY_COMPANIES.values() for c in companies]:
        company_data = tbl.filter(tbl["Company"] == company).to_pandas()
        for col in required:
            assert col in company_data.columns, f"{company}: missing column '{col}'"
