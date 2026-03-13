"""Page 3: fin-chat — natural-language data filtering with querychat."""

import html
import os
from functools import cache

import querychat
import querychat.tools as _qc_tools
from chatlas import ChatGithub, ContentToolResult
from shinychat.types import ToolResultDisplay
from shiny import render, ui
from shinywidgets import output_widget, render_altair

from charts.altair_charts import (
    build_cash_flows,
    build_company_comparison_bar,
    build_company_trend,
    build_metric_trend,
    build_peer_scatter,
    build_sector_bar,
    build_single_company_summary,
)
from components.empty_chart import empty_chart
from data import METRIC_CHOICES, df
from pathlib import Path

GLOSSARY_PATH = (  # <-- ADD THIS BLOCK
    Path(__file__).parent.parent.parent
    / "data"
    / "knowledge_base"
    / "finance_glossary.txt"
)

# ---------------------------------------------------------------------------
# Monkey-patch querychat's _update_dashboard_impl to HTML-escape the query and
# title inside the <button> data-attributes.  Without this, SQL containing
# double-quoted identifiers (e.g. "Current Ratio") breaks the HTML attribute
# parsing and the Apply Filter button renders as raw text.
# ---------------------------------------------------------------------------
_orig_update_dashboard_impl = _qc_tools._update_dashboard_impl


def _patched_update_dashboard_impl(data_source, update_fn):
    _orig_fn = _orig_update_dashboard_impl(data_source, update_fn)

    def _wrapper(query: str, title: str) -> ContentToolResult:
        result = _orig_fn(query, title)
        # Fix unescaped double quotes in the button HTML within the display
        display = result.extra.get("display") if result.extra else None
        if display and hasattr(display, "markdown"):
            md = display.markdown
            # Replace the broken button HTML with properly escaped attributes
            if "querychat-update-dashboard-btn" in md:
                safe_query = html.escape(query, quote=True)
                safe_title = html.escape(title, quote=True)
                fixed_button = (
                    '<button class="btn btn-outline-primary btn-sm float-end '
                    'mt-3 querychat-update-dashboard-btn" '
                    f'data-query="{safe_query}" '
                    f'data-title="{safe_title}">'
                    "Apply Filter</button>"
                )
                # Replace everything from <button to </button>
                import re

                md = re.sub(
                    r"<button\s[^>]*querychat-update-dashboard-btn[^>]*>.*?</button>",
                    fixed_button,
                    md,
                    flags=re.DOTALL,
                )
                result.extra["display"] = ToolResultDisplay(
                    markdown=md,
                    title=display.title,
                    show_request=display.show_request,
                    open=display.open,
                    icon=display.icon,
                )
        return result

    return _wrapper


_qc_tools._update_dashboard_impl = _patched_update_dashboard_impl

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

1. **Tool selection rules — read carefully:**
   - Use `querychat_query` for any question needing aggregation (GROUP BY, AVG,
     SUM, COUNT, ranking, TOP N, etc.) or when reporting statistics.
   - Use `querychat_update_dashboard` ONLY for filtering the dashboard.
   - **CRITICAL: `querychat_update_dashboard` queries MUST always start with
     `SELECT * FROM financial_data WHERE …`.**  Never select specific columns.
     Never use GROUP BY, CTEs, JOINs, or subqueries. The query must return
     every column in the table or it will fail.
   - Never guess or hallucinate numbers. If you cannot answer from the data,
     say so.

2. **Always quote column names** that contain spaces, slashes, or parentheses
   with double quotes in SQL. For example: "Current Ratio", "Debt/Equity Ratio",
   "Market Cap(in B USD)", "Cash Flow from Operating", "Earning Per Share",
   "Cash Flow from Investing", "Cash Flow from Financial Activities",
   "Inflation Rate(in US)", "Share Holder Equity", "Net Profit Margin",
   "Free Cash Flow per Share", "Return on Tangible Equity",
   "Number of Employees", "Gross Profit", "Net Income".

3. Structure every response in this format:
   - **Filters applied:** list the filters used (or "None" if showing all data)
   - **Key stats:** 2-3 notable numbers from the query result
   - **Insight:** one sentence interpreting the result
   - **Try next:** one clickable follow-up suggestion as
     `<span class="suggestion">suggestion text</span>`

4. When the user asks about a sector, use the Category column (e.g., IT, BANK).
   When they mention a company name, map it to the ticker in the Company column.

5. Keep responses concise — no more than 5 sentences outside the structured format.

6. **Never include raw HTML, SQL code blocks, or `<button>` markup in your
   response text.** Do not echo the SQL query or the button element back to the
   user. Just call the appropriate tool and provide the structured summary.
"""


def _load_glossary() -> str:
    """Load the finance glossary knowledge base for RAG context."""
    if GLOSSARY_PATH.exists():
        return GLOSSARY_PATH.read_text(encoding="utf-8")
    return ""


def _build_extra_instructions() -> str:
    """Combine base instructions with the finance glossary knowledge base."""
    glossary = _load_glossary()
    if glossary:
        return (
            EXTRA_INSTRUCTIONS
            + "\n<finance_glossary>\n"
            + glossary
            + "\n</finance_glossary>\n"
        )
    return EXTRA_INSTRUCTIONS


@cache
def _get_qc():
    """Lazily create the QueryChat instance (deferred until first use)."""
    return querychat.QueryChat(
        df,
        "financial_data",
        data_description=DATA_DESCRIPTION,
        extra_instructions=_build_extra_instructions(),
        greeting=GREETING,
        client=ChatGithub(model="gpt-4.1-mini"),
    )


def _has_token():
    """Check whether GITHUB_TOKEN is available."""
    return bool(os.environ.get("GITHUB_TOKEN"))


def ai_explorer_ui():
    """Return the fin-chat page layout."""
    if not _has_token():
        return ui.page_fillable(
            ui.h2("fin-chat"),
            ui.card(
                ui.card_header("Configuration Required"),
                ui.p("Set the GITHUB_TOKEN environment variable to enable fin-chat."),
            ),
        )

    qc = _get_qc()
    sidebar = ui.sidebar(
        qc.ui(),
        open="desktop",
        width=400,
    )

    data_card = ui.card(
        ui.card_header(
            ui.div(
                ui.div(
                    ui.output_text("ai_title"),
                    ui.span(" | "),
                    ui.output_text("ai_row_count", inline=True),
                ),
                ui.download_button(
                    "ai_download",
                    ui.span(
                        ui.HTML(
                            '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
                            'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                            'style="vertical-align: -1px; margin-right: 4px;">'
                            '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11'
                            'a2 2 0 0 1-2 2z"/>'
                            '<polyline points="17 21 17 13 7 13 7 21"/>'
                            '<polyline points="7 3 7 8 15 8"/>'
                            "</svg>"
                        ),
                        "Download CSV",
                    ),
                    class_="btn-sm btn-csv-download",
                ),
                class_="d-flex justify-content-between align-items-center w-100",
            )
        ),
        ui.output_data_frame("ai_data_table"),
        full_screen=True,
        height="auto",
        fill=False,
    )

    chart_row = ui.layout_columns(
        ui.card(
            ui.card_header("Sector Profitability"),
            output_widget("ai_chart_a"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Metric Trend"),
            output_widget("ai_chart_b"),
            full_screen=True,
        ),
        col_widths=[6, 6],
    )

    return ui.layout_sidebar(
        sidebar,
        ui.page_fillable(
            ui.h2("fin-chat"),
            data_card,
            chart_row,
        ),
    )


def ai_explorer_server(input, output, session):
    """Server logic for the fin-chat page."""
    if not _has_token():
        return

    qc = _get_qc()
    qc_vals = qc.server()

    @render.text
    def ai_title():
        title = qc_vals.title()
        return title if title else "Filtered Data"

    MAX_ROWS = 10
    ROW_HEIGHT_PX = 32
    HEADER_HEIGHT_PX = 40

    @render.data_frame
    def ai_data_table():
        filtered = qc_vals.df()
        n = len(filtered)
        height = f"{HEADER_HEIGHT_PX + min(n, MAX_ROWS) * ROW_HEIGHT_PX}px"
        return render.DataGrid(filtered, height=height)

    @render.text
    def ai_row_count():
        filtered = qc_vals.df()
        return f"{len(filtered)} rows"

    def _data_shape(filtered):
        """Return (n_companies, n_sectors, n_years) for adaptive chart selection."""
        return (
            filtered["Company"].nunique(),
            filtered["Category"].nunique(),
            filtered["Year"].nunique(),
        )

    @render_altair
    def ai_chart_a():
        filtered = qc_vals.df()
        metric = _infer_metric(qc_vals.title())
        unit = METRIC_CHOICES.get(metric, "")
        if filtered.empty:
            return empty_chart()
        n_companies, n_sectors, n_years = _data_shape(filtered)
        if n_companies == 1:
            return build_single_company_summary(filtered, metric, unit)
        if n_sectors == 1 or n_years == 1:
            return build_company_comparison_bar(filtered, metric, unit)
        return build_sector_bar(filtered, metric, unit)

    @render_altair
    def ai_chart_b():
        filtered = qc_vals.df()
        metric = _infer_metric(qc_vals.title())
        unit = METRIC_CHOICES.get(metric, "")
        if filtered.empty:
            return empty_chart()
        n_companies, n_sectors, n_years = _data_shape(filtered)
        if n_companies == 1:
            company = filtered["Company"].iloc[0]
            return (
                build_company_trend(filtered, metric, unit)
                if n_years > 1
                else build_cash_flows(filtered, company)
            )
        if n_years == 1:
            return build_peer_scatter(filtered, metric, unit)
        if n_companies <= 5:
            return build_company_trend(filtered, metric, unit)
        return build_metric_trend(filtered, metric, unit)

    @render.download(filename="filtered_financial_data.csv")
    def ai_download():
        filtered = qc_vals.df()
        yield filtered.to_csv(index=False)
