import altair as alt
import pandas as pd

from charts.altair_charts import (
    build_cash_flows,
    build_company_comparison_bar,
    build_company_trend,
    build_metric_trend,
    build_peer_scatter,
    build_ratio_over_time,
    build_revenue_over_time,
    build_sector_bar,
    build_single_company_summary,
)
from data import df


def test_build_sector_bar_returns_chart():
    """Sector bar chart renders a valid Altair chart so Page 1 can compare sectors by metric."""
    chart = build_sector_bar(df, "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_sector_bar_empty_data():
    """Sector bar chart handles empty data gracefully, preventing crashes when filters return no rows."""
    chart = build_sector_bar(pd.DataFrame(), "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_metric_trend_returns_chart():
    """Metric trend chart renders correctly, enabling users to track sector performance over time."""
    chart = build_metric_trend(df, "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_metric_trend_empty_data():
    """Metric trend chart handles empty data gracefully instead of raising an error."""
    chart = build_metric_trend(pd.DataFrame(), "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_peer_scatter_returns_chart():
    """Peer scatter plot renders correctly, allowing users to compare companies within a sector."""
    chart = build_peer_scatter(df, "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_peer_scatter_empty_data():
    """Peer scatter plot handles empty data gracefully instead of crashing the dashboard."""
    chart = build_peer_scatter(pd.DataFrame(), "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_revenue_over_time_returns_chart():
    """Revenue over time chart renders for a single company, supporting Page 2 company analysis."""
    aapl = df[df["Company"] == "AAPL"]
    chart = build_revenue_over_time(aapl, "AAPL")
    assert isinstance(chart, alt.Chart)


def test_build_ratio_over_time_returns_chart():
    """Ratio trend chart renders with threshold lines, enabling financial health assessment over time."""
    aapl = df[df["Company"] == "AAPL"]
    chart = build_ratio_over_time(aapl, "AAPL", "Current Ratio")
    assert isinstance(chart, (alt.Chart, alt.LayerChart))


def test_build_cash_flows_returns_chart():
    """Cash flow chart renders for a single company, supporting Page 2 liquidity analysis."""
    aapl = df[df["Company"] == "AAPL"]
    chart = build_cash_flows(aapl, "AAPL")
    assert isinstance(chart, alt.Chart)


def test_build_company_comparison_bar_returns_chart():
    """Company comparison bar chart renders, allowing users to rank companies within a sector."""
    banks = df[df["Category"] == "BANK"]
    chart = build_company_comparison_bar(banks, "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_company_comparison_bar_empty_data():
    """Company comparison bar chart handles empty data gracefully instead of crashing."""
    chart = build_company_comparison_bar(pd.DataFrame(), "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_single_company_summary_returns_chart():
    """Single company summary chart renders for one company-year, supporting detailed KPI view."""
    single = df[(df["Company"] == "AAPL") & (df["Year"] == 2022)]
    chart = build_single_company_summary(single, "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_single_company_summary_empty_data():
    """Single company summary chart handles empty data gracefully instead of crashing."""
    chart = build_single_company_summary(pd.DataFrame(), "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_company_trend_returns_chart():
    """Company trend chart renders multi-company lines, supporting cross-company metric comparison."""
    it_companies = df[df["Category"] == "IT"]
    chart = build_company_trend(it_companies, "Revenue", "USD")
    assert isinstance(chart, alt.Chart)


def test_build_company_trend_empty_data():
    """Company trend chart handles empty data gracefully instead of crashing the dashboard."""
    chart = build_company_trend(pd.DataFrame(), "Revenue", "USD")
    assert isinstance(chart, alt.Chart)
