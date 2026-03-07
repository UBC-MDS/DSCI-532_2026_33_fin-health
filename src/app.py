from pathlib import Path
import subprocess
from charts.altair_charts import build_metric_trend, build_peer_scatter, build_sector_bar
from data import CATEGORY_COMPANIES, ALL_SECTORS, METRIC_CHOICES
import altair as alt
import pandas as pd
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_altair


DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "financial_statement.csv"


def load_data(path: Path) -> pd.DataFrame:
    """Load and clean the financial dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    data = pd.read_csv(path, encoding="utf-8-sig")
    data.columns = data.columns.str.strip()
    data["Category"] = data["Category"].str.upper()
    return data


df = load_data(DATA_PATH)

# Load custom CSS from external file
CSS_PATH = Path(__file__).parent.parent / "assets" / "custom_styles.css"
with open(CSS_PATH, "r") as css_file:
    CUSTOM_CSS = ui.tags.style(css_file.read())


# Page 1: Sector Analysis
def page1_sector_analysis():
    # Sidebar inputs
    year_slider = ui.input_slider(
        id="p1_year_range",
        label="Period",
        min=int(df["Year"].min()),
        max=int(df["Year"].max()),
        value=[int(df["Year"].min()), int(df["Year"].max())],
        sep="",
    )
    sector_select = ui.input_selectize(
        id="p1_sector",
        label="Sector",
        choices=["All"] + ALL_SECTORS,
        selected="All",
    )
    metric_select = ui.input_selectize(
        id="p1_metric",
        label="Metric",
        choices=list(METRIC_CHOICES.keys()),
        selected="Net Profit Margin",
    )
    sidebar = ui.sidebar(
        ui.h4("Analytics Filters"),
        year_slider,
        sector_select,
        metric_select,
        open="desktop",
    )

    # KPI cards
    card_avg_margin = ui.card(
        ui.card_header("Avg Profit Margin"),
        ui.tags.div(
            ui.tags.h3(
                ui.output_text("p1_avg_margin", inline=True),
                class_="kpi-value",
                style="display: inline;",
            ),
            ui.output_ui("p1_margin_trend", style="display: inline;"),
            class_="kpi-value-row",
        ),
        ui.tags.div(
            ui.output_ui("p1_margin_badge"),
            class_="kpi-label-row",
        ),
    )
    card_top_sector = ui.card(
        ui.card_header("Top Sector"),
        ui.tags.div(
            ui.tags.h3(
                ui.output_text("p1_top_sector", inline=True),
                class_="kpi-value",
                style="display: inline;",
            ),
            class_="kpi-value-row",
        ),
        ui.tags.div(
            ui.output_ui("p1_index_performance_display"),
            class_="kpi-label-row",
        ),
    )
    card_revenue_growth = ui.card(
        ui.card_header("Revenue Growth"),
        ui.tags.div(
            ui.output_ui("p1_revenue_growth_display"),
            ui.output_ui("p1_revenue_trend", style="display: inline;"),
            class_="kpi-value-row",
        ),
        ui.tags.div(
            ui.tags.p(
                "YEAR OVER YEAR",
                class_="kpi-label",
                style="margin-top: 0.5rem;",
            ),
            class_="kpi-label-row",
        ),
    )
    kpi_row = ui.layout_columns(
        card_avg_margin,
        card_top_sector,
        card_revenue_growth,
        col_widths=[4, 4, 4],
    )

    # Chart cards
    card_sector_profitability = ui.card(
        ui.card_header("Sector Profitability"),
        output_widget("p1_chart_a"),
        full_screen=True,
    )
    card_trend = ui.card(
        ui.card_header(ui.output_ui("trend_header")),
        output_widget("p1_chart_b"),
        full_screen=True,
    )
    chart_row = ui.layout_columns(
        card_sector_profitability,
        card_trend,
        col_widths=[6, 6],
    )

    # Peer + Table cards
    card_peer = ui.card(
        ui.card_header("Peer Benchmarking"),
        output_widget("p1_chart_c"),
        full_screen=True,
    )
    card_details = ui.card(
        ui.card_header("Company Details"),
        ui.output_data_frame("p1_table_d"),
    )
    peer_row = ui.layout_columns(
        card_peer,
        card_details,
        col_widths=[6, 6],
    )

    return ui.layout_sidebar(
        sidebar,
        ui.page_fillable(
            ui.h2("US Corporate Profitability Analytics"),
            kpi_row,
            chart_row,
            peer_row,
        ),
    )


# Page 2: Company Financial Health
def page2_company_health():
    # Sidebar inputs
    category_select = ui.input_select(
        id="category",
        label="Industry",
        choices=ALL_SECTORS,
        selected=ALL_SECTORS[0],
    )
    company_select = ui.input_select(
        id="company",
        label="Company",
        choices=[],
    )
    year_select = ui.input_select(
        id="year",
        label="Year",
        choices=[str(y) for y in range(2023, 2008, -1)],
        selected="2022",
    )
    sidebar = ui.sidebar(
        ui.h4("Analytics Filters"),
        category_select,
        company_select,
        year_select,
        open="desktop",
    )

    # Profitability cards
    card_npm = ui.card(
        ui.card_header("Net Profit Margin"),
        ui.div(
            ui.span("25.3%", class_="kpi-value"),
            ui.br(),
            ui.span("[Sparkline chart placeholder]", class_="kpi-label"),
        ),
    )
    card_roe = ui.card(
        ui.card_header("Return on Equity (ROE)"),
        ui.div(
            ui.span("196.96%", class_="kpi-value"),
            ui.br(),
            ui.span("[Sparkline chart placeholder]", class_="kpi-label"),
        ),
        style="height: calc(50% - 0.5rem);",
    )
    card_rev_income = ui.card(
        ui.card_header("Revenue & Net Income"),
        ui.tags.span("REVENUE", class_="kpi-label"),
        ui.div(
            ui.span("$394,328M", class_="kpi-value"),
            ui.br(),
            ui.span("Revenue", class_="kpi-label"),
            ui.br(),
            ui.br(),
            ui.span("$99,803M", class_="kpi-value"),
            ui.br(),
            ui.span("Net Income", class_="kpi-label"),
        ),
    )
    card_rev_time = ui.card(
        ui.card_header("Revenue Over Time"),
        ui.p("[Bar chart placeholder — yearly revenue from 2009-2023]"),
        full_screen=True,
    )
    profitability_section = ui.div(
        ui.div("PROFITABILITY", class_="section-label section-label-blue"),
        ui.layout_columns(
            card_npm,
            card_roe,
            card_rev_income,
            card_rev_time,
            col_widths=[3, 3, 3, 3],
        ),
        class_="grid-section",
    )

    # Financial Health cards
    card_current_ratio = ui.card(
        ui.card_header("Current Ratio"),
        ui.div(
            ui.span("0.88", class_="kpi-value"),
            ui.br(),
            ui.span("Current Ratio over time", class_="kpi-label"),
        ),
        ui.p("[Line chart placeholder]"),
        full_screen=True,
    )
    card_debt_equity = ui.card(
        ui.card_header("Debt / Equity Ratio"),
        ui.div(
            ui.span("2.37", class_="kpi-value"),
            ui.br(),
            ui.span("Debt/Equity over time", class_="kpi-label"),
        ),
        ui.p("[Line chart placeholder]"),
        full_screen=True,
    )
    card_cash_flows = ui.card(
        ui.card_header("Cash Flows"),
        ui.div(
            ui.span("Operating: $122,151M", class_="kpi-label"),
            ui.br(),
            ui.span("Investing: -$22,354M", class_="kpi-label"),
            ui.br(),
            ui.span("Financing: -$110,749M", class_="kpi-label"),
        ),
        ui.p("[Grouped bar chart placeholder]"),
        full_screen=True,
    )
    health_section = ui.div(
        ui.div("FINANCIAL HEALTH", class_="section-label section-label-red"),
        ui.layout_columns(
            card_current_ratio,
            card_debt_equity,
            card_cash_flows,
            col_widths=[4, 4, 4],
        ),
        class_="grid-section",
    )

    return ui.layout_sidebar(
        sidebar,
        ui.page_fillable(
            ui.h2("Financial Health Dashboard"),
            ui.p(
                "A comprehensive KPI dashboard highlighting key financial metrics of public companies."
            ),
            profitability_section,
            health_section,
        ),
    )


nav_sector = ui.nav_panel("Sector Analysis", page1_sector_analysis())
nav_company = ui.nav_panel("Company Health", page2_company_health())
navbar = ui.page_navbar(
    nav_sector,
    nav_company,
    title="fin-health",
    id="main_nav",
    fillable=True,
)

footer = ui.tags.footer(
    ui.tags.div(
        ui.p(
            "US Corporate Financial Health Dashboard | ",
            "Team: Jiro Amato, Seungmyun Park, Shruti Sasi, Luke Ni | ",
            ui.a("GitHub Repo", href="https://github.com/UBC-MDS/532-finance-health"),
            " | Last updated: "
            + subprocess.run(
                ["git", "log", "-1", "--format=%ci"], capture_output=True, text=True
            ).stdout.strip()[:10],
            style="text-align: center; font-size: 0.85em; color: #888;",
        ),
        class_="footer-container",
    )
)

app_ui = ui.page_fluid(CUSTOM_CSS, navbar, footer)


def server(input, output, session):

    # Page 1: Sector Analysis
    @reactive.calc
    def p1_selected_metric():
        """Return the selected metric, falling back to default if cleared."""
        metric = input.p1_metric()
        if not metric or metric not in METRIC_CHOICES:
            return "Net Profit Margin"
        return metric

    @reactive.calc
    def p1_filtered_data():
        """Filter dataset by selected year range and sector."""
        year_min, year_max = input.p1_year_range()
        sector = input.p1_sector()
        if not sector:
            sector = "All"

        filtered = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]

        if sector != "All":
            filtered = filtered[filtered["Category"] == sector]

        return filtered

    # KPI outputs
    # Avg Profit Margin
    @render.text
    def p1_avg_margin():
        filtered = p1_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        avg = filtered["Net Profit Margin"].mean()
        return f"{avg:.1f}%"

    @render.ui
    def p1_margin_trend():
        """Render trend indicator for profit margin based on actual data."""
        filtered_df = p1_filtered_data()
        if filtered_df.empty:
            return ui.tags.span()

        # Get years sorted
        years = sorted(filtered_df["Year"].unique())
        if len(years) < 2:
            return ui.tags.span()  # No trend to show with single year

        # Compare most recent year to previous year
        current_year_margin = filtered_df[filtered_df["Year"] == years[-1]][
            "Net Profit Margin"
        ].mean()
        previous_year_margin = filtered_df[filtered_df["Year"] == years[-2]][
            "Net Profit Margin"
        ].mean()

        if pd.isna(current_year_margin) or pd.isna(previous_year_margin):
            return ui.tags.span()

        is_positive = current_year_margin >= previous_year_margin
        trend_char = "▲" if is_positive else "▼"
        trend_class = "up" if is_positive else "down"
        return ui.tags.span(trend_char, class_=f"trend-indicator {trend_class}")

    @render.ui
    def p1_margin_badge():
        filtered = p1_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        n = filtered["Company"].nunique()
        return ui.tags.p(
            f"BASED ON {n} COMPANIES",
            class_="kpi-label",
            style="margin-top: 0.5rem;",
        )

    # Top Sector
    @render.text
    def p1_top_sector():
        filtered = p1_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        top = filtered.groupby("Category")["Net Profit Margin"].mean().idxmax()
        return top

    @reactive.calc
    def p1_index_margin():
        filtered_df = p1_filtered_data()
        if filtered_df.empty:
            return 0.0

        # Aggregated Index Formula: Total Income / Total Revenue
        total_revenue = filtered_df["Revenue"].sum()
        total_net_income = filtered_df["Net Income"].sum()

        if total_revenue == 0:
            return 0.0

        return (total_net_income / total_revenue) * 100

    @render.ui
    def p1_index_performance_display():
        margin = p1_index_margin()
        return ui.tags.p(
            "INDEX PERFORMANCE: ",
            ui.tags.strong(f"{margin:.1f}%"),
            " NET PROFIT MARGIN",
            class_="kpi-label",
        )

    # Revenue Growth
    @reactive.calc
    def p1_revenue_change():
        """Calculate revenue change value and direction (shared by display and trend)."""
        filtered_df = p1_filtered_data()
        yearly_revenue = (
            filtered_df.groupby("Year")["Revenue"].sum().sort_index(ascending=False)
        )

        if len(yearly_revenue) < 2:
            return None

        current = yearly_revenue.iloc[0]
        previous = yearly_revenue.iloc[1]

        if pd.isna(current) or pd.isna(previous) or previous == 0:
            return None

        revenue_growth = (current - previous) / previous * 100
        return {"value": revenue_growth, "is_positive": revenue_growth >= 0}

    @render.ui
    def p1_revenue_growth_display():
        change = p1_revenue_change()
        if change is None:
            return ui.tags.h3(
                "Data Unavailable", class_="kpi-value", style="display: inline;"
            )
        sign = "+" if change["is_positive"] else ""
        return ui.tags.h3(
            f"{sign}{change['value']:.1f}%",
            class_="kpi-value",
            style="display: inline;",
        )

    @render.ui
    def p1_revenue_trend():
        """Render trend indicator for revenue growth based on actual data."""
        change = p1_revenue_change()
        if change is None:
            return ui.tags.span()
        trend_char = "▲" if change["is_positive"] else "▼"
        trend_class = "up" if change["is_positive"] else "down"
        return ui.tags.span(trend_char, class_=f"trend-indicator {trend_class}")

    # Charts
    # Sector Profitability
    @render_altair
    def p1_chart_a():
        filtered = p1_filtered_data()
        metric = p1_selected_metric()
        unit = METRIC_CHOICES[metric]
        return build_sector_bar(filtered, metric, unit)
    
    # Metric Based Trend
    # Change p1_chart_b header based on metric filter selection
    @render.ui
    def trend_header():
        min_year, max_year = input.p1_year_range()
        return f"Trend - {p1_selected_metric()}  ({min_year}-{max_year})"

    @render_altair
    def p1_chart_b():
        filtered = p1_filtered_data()
        metric = p1_selected_metric()
        unit = METRIC_CHOICES[metric]
        return build_metric_trend(filtered, metric, unit)
    
    # Peer Benchmarking Scatterplot
    @render_altair
    def p1_chart_c():
        filtered = p1_filtered_data()
        metric = p1_selected_metric()
        unit = METRIC_CHOICES[metric]
        return build_peer_scatter(filtered, metric, unit)

    # Company Details
    @render.data_frame
    def p1_table_d():
        filtered = p1_filtered_data()
        cols = [
            "Company",
            "Category",
            "Year",
            "Revenue",
            "Net Income",
            "Net Profit Margin",
        ]
        return filtered[cols]

    # Page 2: Company Financial Health
    @reactive.effect
    @reactive.event(input.category)
    def _update_company_choices():
        companies = CATEGORY_COMPANIES.get(input.category(), [])
        selected = companies[0] if companies else None
        ui.update_select("company", choices=companies, selected=selected)


# Create app
app = App(app_ui, server)
