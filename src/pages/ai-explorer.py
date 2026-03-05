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