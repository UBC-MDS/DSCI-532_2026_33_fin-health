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
    chart = build_sector_bar(df, "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_sector_bar_empty_data():
    chart = build_sector_bar(pd.DataFrame(), "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_metric_trend_returns_chart():
    chart = build_metric_trend(df, "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_metric_trend_empty_data():
    chart = build_metric_trend(pd.DataFrame(), "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_peer_scatter_returns_chart():
    chart = build_peer_scatter(df, "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_peer_scatter_empty_data():
    chart = build_peer_scatter(pd.DataFrame(), "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_revenue_over_time_returns_chart():
    aapl = df[df["Company"] == "AAPL"]
    chart = build_revenue_over_time(aapl, "AAPL")
    assert isinstance(chart, alt.Chart)


def test_build_ratio_over_time_returns_chart():
    aapl = df[df["Company"] == "AAPL"]
    chart = build_ratio_over_time(aapl, "AAPL", "Current Ratio")
    assert isinstance(chart, (alt.Chart, alt.LayerChart))


def test_build_cash_flows_returns_chart():
    aapl = df[df["Company"] == "AAPL"]
    chart = build_cash_flows(aapl, "AAPL")
    assert isinstance(chart, alt.Chart)


def test_build_company_comparison_bar_returns_chart():
    banks = df[df["Category"] == "BANK"]
    chart = build_company_comparison_bar(banks, "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_company_comparison_bar_empty_data():
    chart = build_company_comparison_bar(pd.DataFrame(), "ROE", "%")
    assert isinstance(chart, alt.Chart)


def test_build_single_company_summary_returns_chart():
    single = df[(df["Company"] == "AAPL") & (df["Year"] == 2022)]
    chart = build_single_company_summary(single, "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_single_company_summary_empty_data():
    chart = build_single_company_summary(pd.DataFrame(), "Net Profit Margin", "%")
    assert isinstance(chart, alt.Chart)


def test_build_company_trend_returns_chart():
    it_companies = df[df["Category"] == "IT"]
    chart = build_company_trend(it_companies, "Revenue", "USD")
    assert isinstance(chart, alt.Chart)


def test_build_company_trend_empty_data():
    chart = build_company_trend(pd.DataFrame(), "Revenue", "USD")
    assert isinstance(chart, alt.Chart)