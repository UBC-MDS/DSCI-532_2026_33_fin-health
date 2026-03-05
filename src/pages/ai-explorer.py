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

DATA_DESCRIPTION = """
US Corporate financial statement data (2009–2023), covering 12 publicly
traded companies across 8 sectors.

Company-sector mapping:
- BANK: AIG, BCS
- ELEC: INTC, NVDA
- FINANCE: SHLDQ
- FINTECH: PYPL
- FOOD: MCD
- IT: AAPL, GOOG, MSFT
- LOGI: AMZN
- MANUFACTURING: PCG

Column descriptions (with approximate value ranges):
- Year: fiscal year (2009–2023)
- Company: ticker symbol (AAPL, GOOG, MSFT, AMZN, INTC, NVDA, PYPL, MCD, AIG, BCS, SHLDQ, PCG)
- Category: sector (BANK, ELEC, FINANCE, FINTECH, FOOD, IT, LOGI, MANUFACTURING)
- Market Cap(in B USD): market capitalization in billions (~$1B–$3,000B)
- Revenue: annual revenue in millions USD (~$500M–$400,000M)
- Gross Profit: gross profit in millions USD (~$100M–$170,000M)
- Net Income: net income in millions USD (~-$25,000M–$100,000M)
- Earning Per Share: earnings per share in USD (~-$30–$6)
- EBITDA: earnings before interest, taxes, depreciation, amortization in millions USD (~-$5,000M–$130,000M)
- Share Holder Equity: total shareholder equity in millions USD (~-$15,000M–$270,000M)
- Cash Flow from Operating: operating cash flow in millions USD (~-$5,000M–$120,000M)
- Cash Flow from Investing: investing cash flow in millions USD (~-$50,000M–$30,000M)
- Cash Flow from Financial Activities: financing cash flow in millions USD (~-$120,000M–$30,000M)
- Current Ratio: current assets / current liabilities; >1 = healthy liquidity (~0.5–4.0)
- Debt/Equity Ratio: total debt / shareholder equity (~-10–30)
- ROE: return on equity in percent (~-80%–+160%)
- ROA: return on assets in percent (~-15%–+30%)
- ROI: return on investment in percent (~-20%–+50%)
- Net Profit Margin: net income / revenue in percent (~-50%–+35%)
- Free Cash Flow per Share: free cash flow per share in USD (~-$5–$7)
- Return on Tangible Equity: return on tangible equity in percent (~-200%–+200%)
- Number of Employees: headcount (~10,000–1,600,000)
- Inflation Rate(in US): US inflation rate for that year in percent (~0.1%–8%)
"""

GREETING = """
Hi! I can help you explore the financial dataset. Try one of these:

**Filter:** <span class="suggestion">Show tech companies with net profit margin above 20%</span>

**Compare:** <span class="suggestion">Rank all companies by ROE in 2022</span>

**Aggregate:** <span class="suggestion">What is the average revenue by sector?</span>

**Health check:** <span class="suggestion">Which companies have a current ratio below 1?</span>
"""

EXTRA_INSTRUCTIONS = """
You are a financial data analyst assistant. Follow these rules strictly:

1. **Always use `querychat_query` before reporting any statistics.** Never guess,
   estimate, or hallucinate numbers. If you cannot answer from the data, say so.

2. Structure every response in this format:
   - **Filters applied:** list the filters used (or "None" if showing all data)
   - **Key stats:** 2-3 notable numbers from the query result
   - **Insight:** one sentence interpreting the result
   - **Try next:** one clickable follow-up suggestion as
     `<span class="suggestion">suggestion text</span>`

3. When the user asks about a sector, use the Category column (e.g., IT, BANK).
   When they mention a company name, map it to the ticker in the Company column.

4. Keep responses concise — no more than 5 sentences outside the structured format.
"""
