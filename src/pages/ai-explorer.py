"""Page 3: fin-chat — natural-language data filtering with querychat."""

import os
from functools import cache

import querychat
from chatlas import ChatGithub
from shiny import render, ui
from shinywidgets import output_widget, render_altair

from charts.altair_charts import (
    build_company_comparison_bar,
    build_company_trend,
    build_cash_flows,
    build_metric_trend,
    build_peer_scatter,
    build_sector_bar,
    build_single_company_summary,
)
from components.empty_chart import empty_chart
from data import METRIC_CHOICES, df

DEFAULT_METRIC = "Net Profit Margin"

# Keyword → metric mapping for inferring metric from querychat title/SQL.
# Order matters: longer/more-specific patterns first to avoid false matches.
_METRIC_KEYWORDS = {
    "net profit margin": "Net Profit Margin",
    "profit margin": "Net Profit Margin",
    "roe": "ROE",
    "return on equity": "ROE",
    "roa": "ROA",
    "return on assets": "ROA",
    "roi": "ROI",
    "return on investment": "ROI",
    "revenue": "Revenue",
    "net income": "Net Income",
    "ebitda": "EBITDA",
    "current ratio": "Current Ratio",
    "debt/equity": "Debt\\Equity Ratio",
    "debt equity": "Debt\\Equity Ratio",
    "debt to equity": "Debt\\Equity Ratio",
}


def _infer_metric(title: str | None) -> str:
    """Infer the metric from the querychat title via keyword matching."""
    if not title:
        return DEFAULT_METRIC
    lower = title.lower()
    for keyword, metric in _METRIC_KEYWORDS.items():
        if keyword in lower:
            return metric
    return DEFAULT_METRIC