from pathlib import Path
import altair as alt
import pandas as pd
from datetime import datetime
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_altair


# Data loading from module level
DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "financial_statement.csv"
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df["Category"] = df[
    "Category"
].str.upper()  # Fix: Category column has 'BANK' and 'bank'

# Load custom CSS from external file
CSS_PATH = Path(__file__).parent.parent / "assets" / "custom_styles.css"
with open(CSS_PATH, "r") as css_file:
    CUSTOM_CSS = ui.tags.style(css_file.read())

CATEGORY_COMPANIES = {
    "BANK": ["AIG", "BCS"],
    "ELEC": ["INTC", "NVDA"],
    "FINANCE": ["SHLDQ"],
    "FINTECH": ["PYPL"],
    "FOOD": ["MCD"],
    "IT": ["AAPL", "GOOG", "MSFT"],
    "LOGI": ["AMZN"],
    "MANUFACTURING": ["PCG"],
}
ALL_CATEGORIES = sorted(CATEGORY_COMPANIES.keys())
ALL_SECTORS = [
    "BANK",
    "ELEC",
    "FINANCE",
    "FINTECH",
    "FOOD",
    "IT",
    "LOGI",
    "MANUFACTURING",
]

METRIC_CHOICES = {
    "Net Profit Margin": "%",
    "ROE": "%",
    "ROA": "%",
    "ROI": "%",
    "Revenue": "USD",
    "Net Income": "USD",
    "EBITDA": "USD",
    "Current Ratio": "",
    "Debt/Equity Ratio": "",
}


# Page 1: Sector Analysis
def page1_sector_analysis():
    return ui.layout_sidebar(
        ui.sidebar(
            ui.h4("Analytics Filters"),
            ui.input_slider(
                id="p1_year_range",
                label="Period",
                min=int(df["Year"].min()),
                max=int(df["Year"].max()),
                value=[int(df["Year"].min()), int(df["Year"].max())],
                sep="",
            ),
            ui.input_selectize(
                id="p1_sector",
                label="Sector",
                choices=["All"] + ALL_SECTORS,
                selected="All",
            ),
            ui.input_select(
                id="p1_metric",
                label="Metric",
                choices=list(METRIC_CHOICES.keys()),
                selected="Net Profit Margin",
            ),
            open="desktop",
        ),
        ui.page_fillable(
            ui.h2("US Corporate Profitability Analytics"),
            # Row 1: KPI Cards
            ui.layout_columns(
                ui.card(
                    ui.card_header("Avg Profit Margin"),
                    ui.tags.div(
                        ui.tags.h3(
                            ui.output_text("p1_avg_margin", inline=True),
                            class_="kpi-value",
                            style="display: inline;",
                        ),
                        ui.output_ui("p1_margin_trend", style="display: inline;"),
                    ),
                    ui.output_ui("p1_margin_badge"),
                ),
                ui.card(
                    ui.card_header("Top Sector"),
                    ui.tags.h3(
                        ui.output_text("p1_top_sector", inline=True),
                        class_="kpi-value",
                        style="display: inline;",
                    ),
                    ui.output_ui("p1_index_performance_display"),
                ),
                ui.card(
                    ui.card_header("Revenue Growth"),
                    ui.tags.div(
                        ui.output_ui("p1_revenue_growth_display"),
                        ui.output_ui("p1_revenue_trend", style="display: inline;"),
                    ),
                    ui.tags.p(
                        "YEAR OVER YEAR",
                        class_="kpi-label",
                        style="margin-top: 0.5rem;",
                    ),
                ),
                col_widths=[4, 4, 4],
            ),
            # Row 2: Charts
            ui.layout_columns(
                ui.card(
                    ui.card_header("Sector Profitability"),
                    output_widget("p1_chart_a"),
                    full_screen=True,  # allows users to expand the chart
                ),
                ui.card(
                    ui.card_header(ui.output_ui("trend_header")),
                    output_widget("p1_chart_b"),
                    full_screen=True,  # allows users to expand the chart
                ),
                col_widths=[6, 6],
            ),
            # Row 3: Peer + Table
            ui.layout_columns(
                ui.card(
                    ui.card_header("Peer Benchmarking"),
                    output_widget("p1_chart_c"),
                    full_screen=True,  # allows users to expand the chart
                ),
                ui.card(
                    ui.card_header("Company Details"),
                    ui.output_data_frame("p1_table_d"),
                ),
                col_widths=[6, 6],
            ),
        ),
    )


# Page 2: Company Financial Health
def page2_company_health():
    return ui.layout_sidebar(
        ui.sidebar(
            ui.h4("Analytics Filters"),
            ui.input_select(
                id="category",
                label="Industry",
                choices=ALL_CATEGORIES,
                selected=ALL_CATEGORIES[0],
            ),
            ui.input_select(
                id="company",
                label="Company",
                choices=[],
            ),
            ui.input_select(
                id="year",
                label="Year",
                choices=[str(y) for y in range(2023, 2008, -1)],
                selected="2022",
            ),
            open="desktop",
        ),
        ui.page_fillable(
            ui.h2("Financial Health Dashboard"),
            ui.p(
                "A comprehensive KPI dashboard highlighting key financial metrics of public companies."
            ),
            # Profitability Section
            ui.div(
                ui.div("PROFITABILITY", class_="section-label section-label-blue"),
                ui.layout_columns(
                    ui.div(
                        ui.card(
                            ui.card_header("Net Profit Margin"),
                            ui.tags.h3(
                                ui.output_text("p2_net_margin", inline=True),
                                class_="kpi-value",
                            ),
                            style="height: calc(50% - 0.5rem); margin-bottom: 1rem;",
                        ),
                        ui.card(
                            ui.card_header("Return on Equity (ROE)"),
                            ui.tags.h3(
                                ui.output_text("p2_roe", inline=True),
                                class_="kpi-value",
                            ),
                            style="height: calc(50% - 0.5rem);",
                        ),
                        style="height: 100%;",
                    ),
                    ui.card(
                        ui.card_header("Revenue & Net Income"),
                        ui.tags.span("REVENUE", class_="kpi-label"),
                        ui.tags.h3(
                            ui.output_text("p2_revenue", inline=True),
                            class_="kpi-value",
                        ),
                        ui.tags.span(
                            "NET INCOME",
                            class_="kpi-label",
                            style="display: block; margin-top: 1rem;",
                        ),
                        ui.tags.h3(
                            ui.output_text("p2_net_income", inline=True),
                            class_="kpi-value",
                        ),
                    ),
                    ui.card(
                        ui.card_header("Revenue Over Time"),
                        output_widget("p2_chart_revenue"),
                        full_screen=True,  # allows users to expand the chart
                    ),
                    col_widths=[3, 3, 6],
                ),
                class_="grid-section",
            ),
            # Financial Health Section
            ui.div(
                ui.div("FINANCIAL HEALTH", class_="section-label section-label-red"),
                ui.layout_columns(
                    ui.card(
                        ui.card_header("Current Ratio"),
                        output_widget("p2_chart_current_ratio"),
                        full_screen=True,  # allows users to expand the chart
                    ),
                    ui.card(
                        ui.card_header("Debt / Equity Ratio"),
                        output_widget("p2_chart_debt_equity"),
                        full_screen=True,  # allows users to expand the chart
                    ),
                    ui.card(
                        ui.card_header("Cash Flows"),
                        output_widget("p2_chart_cashflow"),
                        full_screen=True,  # allows users to expand the chart
                    ),
                    col_widths=[4, 4, 4],
                ),
                class_="grid-section",
            ),
        ),
    )


app_ui = ui.page_fluid(
    CUSTOM_CSS,
    ui.page_navbar(
        ui.nav_panel("Sector Analysis", page1_sector_analysis()),
        ui.nav_panel("Company Health", page2_company_health()),
        title="fin-health",
        id="main_nav",
        fillable=True,
    ),
    ui.tags.footer(
        ui.tags.div(
            ui.layout_columns(
                ui.tags.div(
                    ui.tags.strong("Financial Health Dashboard"),
                    ui.tags.p(
                        "A comprehensive tool for analyzing US corporate profitability and sector trends."
                    ),
                ),
                ui.tags.div(
                    ui.tags.p(
                        ui.tags.strong("Authors: "),
                        "Jiro Amato, Luke Ni, Seungmyun Park, Shruti Sasi",
                    ),
                    ui.tags.p(
                        ui.tags.strong("Source: "),
                        ui.tags.a(
                            "GitHub Repository",
                            href="https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health",
                            target="_blank",
                        ),
                    ),
                ),
                ui.tags.div(
                    ui.tags.p(ui.tags.strong("Last Updated:")),
                    ui.output_text("last_updated_date"),
                    style="text-align: right;",
                ),
                col_widths=[5, 4, 3],
            ),
            class_="footer-container",
        )
    ),
)


def server(input, output, session):

    # Page 1: Sector Analysis
    @reactive.calc
    def p1_filtered_data():
        """Filter dataset by selected year range and sector."""
        year_min, year_max = input.p1_year_range()
        sector = input.p1_sector()

        filtered = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]

        if sector != "All":
            filtered = filtered[filtered["Category"] == sector]

        return filtered

    # KPI outputs
    # ------------------ Avg Profit Margin --------------------
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

    # ------------------ Top Sector --------------------
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
            " NET MARGIN",
            class_="kpi-label",
        )

    # ------------------ Revenue growth --------------------
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
    # ------------------ Sector Profitability --------------------
    @render_altair
    def p1_chart_a():
        filtered = p1_filtered_data()
        metric = input.p1_metric()
        unit = METRIC_CHOICES[metric]

        avg_by_sector = filtered.groupby("Category")[metric].mean().reset_index()
        if avg_by_sector.empty:
            return (
                alt.Chart(
                    pd.DataFrame({"x": [0], "y": [0], "text": ["Data Unavailable"]})
                )
                .mark_text(size=18)
                .encode(
                    text="text:N",
                )
            )
        chart = (
            alt.Chart(avg_by_sector)
            .mark_bar()
            .encode(
                x=alt.X("Category:N", title="Sector", sort="-y"),
                y=alt.Y(f"{metric}:Q", title=f"{metric} {unit}"),
                color=alt.Color(
                    "Category:N",
                    scale=alt.Scale(scheme="viridis"),
                    legend=None,
                ),
                tooltip=["Category", alt.Tooltip(f"{metric}:Q", format=".2f")],
            )
            .properties(title=f"Average {metric} by Sector", width="container")
        )
        return chart

    # ------------------ Metric based Trend --------------------
    # Change p1_chart_b header based on metric filter selection
    @render.ui
    def trend_header():
        min_year, max_year = input.p1_year_range()
        return f"Trend - {input.p1_metric()}  ({min_year}-{max_year})"

    @render_altair
    def p1_chart_b():
        filtered = p1_filtered_data()
        metric = input.p1_metric()
        unit = METRIC_CHOICES[metric]

        observed_trend = filtered.groupby(["Year", "Category"], as_index=False)[
            metric
        ].mean()

        if observed_trend.empty:
            return (
                alt.Chart(
                    pd.DataFrame({"x": [0], "y": [0], "text": ["Data Unavailable"]})
                )
                .mark_text(size=18)
                .encode(
                    text="text:N",
                )
            )

        metric_trend = (
            alt.Chart(observed_trend)
            .mark_line(point=True)
            .encode(
                alt.X("Year:O", title="Year"),
                alt.Y(f"{metric}:Q", title=f"{metric} {unit}"),
                color=alt.Color("Category:N", scale=alt.Scale(scheme="viridis")),
                tooltip=["Year", "Category", alt.Tooltip(f"{metric}:Q", format=".2f")],
            )
        )
        return metric_trend

    # ------------------ Peer Benchmarking Scatter Plot --------------------
    @render_altair
    def p1_chart_c():
        filtered = p1_filtered_data()
        metric = input.p1_metric()
        unit = METRIC_CHOICES[metric]

        if filtered.empty:
            return (
                alt.Chart(
                    pd.DataFrame({"x": [0], "y": [0], "text": ["Data Unavailable"]})
                )
                .mark_text(size=18)
                .encode(
                    text="text:N",
                )
            )

        chart = (
            alt.Chart(filtered)
            .mark_circle(size=60)
            .encode(
                x=alt.X("Revenue:Q", title="Revenue ($)"),
                y=alt.Y(f"{metric}:Q", title=f"{metric} {unit}"),
                color=alt.Color("Category:N", scale=alt.Scale(scheme="viridis")),
                tooltip=[
                    "Company",
                    "Category",
                    "Year:O",
                    alt.Tooltip("Revenue:Q", format=",.0f"),
                    alt.Tooltip(f"{metric}:Q", format=",.2f"),
                ],
            )
            .properties(title=f"Revenue vs {metric}", width="container")
        )
        return chart

    # ------------------ Company Details --------------------
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
        ui.update_select("company", choices=companies, selected=companies[0])

    @reactive.calc
    def p2_filtered_data():
        """Filter dataset by selected company, category, and year."""
        company = input.company()
        year = int(input.year())

        filtered = df[(df["Company"] == company) & (df["Year"] == year)]
        return filtered

    # KPI Outputs for Page 2
    @render.text
    def p2_net_margin():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        margin = filtered["Net Profit Margin"].iloc[0]
        return f"{margin:.1f}%" if pd.notna(margin) else "Data Unavailable"

    @render.text
    def p2_roe():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        roe = filtered["ROE"].iloc[0]
        return f"{roe:.2f}%" if pd.notna(roe) else "Data Unavailable"

    @render.text
    def p2_revenue():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        revenue = filtered["Revenue"].iloc[0]
        return f"${revenue:,.0f}M" if pd.notna(revenue) else "Data Unavailable"

    @render.text
    def p2_net_income():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        income = filtered["Net Income"].iloc[0]
        return f"${income:,.0f}M" if pd.notna(income) else "Data Unavailable"

    @render.text
    def p2_current_ratio():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        ratio = filtered["Current Ratio"].iloc[0]
        return f"{ratio:.2f}" if pd.notna(ratio) else "Data Unavailable"

    @render.text
    def p2_debt_equity():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        ratio = filtered["Debt/Equity Ratio"].iloc[0]
        return f"{ratio:.2f}" if pd.notna(ratio) else "Data Unavailable"

    @render.text
    def p2_operating_cf():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Operating: Data Unavailable"
        cf = (
            filtered["Operating Cash Flow"].iloc[0]
            if "Operating Cash Flow" in filtered.columns
            else filtered["Revenue"].iloc[0] * 0.3
        )
        return (
            f"Operating: ${cf:,.0f}M" if pd.notna(cf) else "Operating: Data Unavailable"
        )

    @render.text
    def p2_investing_cf():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Investing: Data Unavailable"
        cf = (
            filtered["Investing Cash Flow"].iloc[0]
            if "Investing Cash Flow" in filtered.columns
            else -filtered["Revenue"].iloc[0] * 0.1
        )
        return (
            f"Investing: ${cf:,.0f}M" if pd.notna(cf) else "Investing: Data Unavailable"
        )

    @render.text
    def p2_financing_cf():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "Financing: Data Unavailable"
        cf = (
            filtered["Financing Cash Flow"].iloc[0]
            if "Financing Cash Flow" in filtered.columns
            else -filtered["Revenue"].iloc[0] * 0.2
        )
        return (
            f"Financing: ${cf:,.0f}M" if pd.notna(cf) else "Financing: Data Unavailable"
        )

    @render_altair
    def p2_chart_revenue():
        company = input.company()
        company_data = df[df["Company"] == company].sort_values("Year")

        if company_data.empty:
            return (
                alt.Chart(
                    pd.DataFrame({"x": [0], "y": [0], "text": ["Data Unavailable"]})
                )
                .mark_text(size=18)
                .encode(text="text:N")
            )

        chart = (
            alt.Chart(company_data)
            .mark_bar()
            .encode(
                x=alt.X("Year:O", title="Year"),
                y=alt.Y("Revenue:Q", title="Revenue ($M)"),
                color=alt.value("#4F81BD"),
                tooltip=["Year", alt.Tooltip("Revenue:Q", format=",.0f")],
            )
            .properties(width="container")
        )
        return chart

    @render_altair
    def p2_chart_current_ratio():
        company = input.company()
        company_data = df[df["Company"] == company].sort_values("Year")

        if company_data.empty:
            return (
                alt.Chart(
                    pd.DataFrame({"x": [0], "y": [0], "text": ["Data Unavailable"]})
                )
                .mark_text(size=18)
                .encode(text="text:N")
            )

        chart = (
            alt.Chart(company_data)
            .mark_line(point=True)
            .encode(
                x=alt.X("Year:O", title="Year"),
                y=alt.Y("Current Ratio:Q", title="Current Ratio"),
                color=alt.value("#70AD47"),
                tooltip=["Year", alt.Tooltip("Current Ratio:Q", format=".2f")],
            )
            .properties(width="container")
        )
        return chart

    @render_altair
    def p2_chart_debt_equity():
        company = input.company()
        company_data = df[df["Company"] == company].sort_values("Year")

        if company_data.empty:
            return (
                alt.Chart(
                    pd.DataFrame({"x": [0], "y": [0], "text": ["Data Unavailable"]})
                )
                .mark_text(size=18)
                .encode(text="text:N")
            )

        chart = (
            alt.Chart(company_data)
            .mark_line(point=True)
            .encode(
                x=alt.X("Year:O", title="Year"),
                y=alt.Y("Debt/Equity Ratio:Q", title="Debt/Equity Ratio"),
                color=alt.value("#FFC000"),
                tooltip=["Year", alt.Tooltip("Debt/Equity Ratio:Q", format=".2f")],
            )
            .properties(width="container")
        )
        return chart

    @render_altair
    def p2_chart_cashflow():
        company = input.company()
        company_data = df[df["Company"] == company].sort_values("Year")

        if company_data.empty:
            return (
                alt.Chart(
                    pd.DataFrame({"x": [0], "y": [0], "text": ["Data Unavailable"]})
                )
                .mark_text(size=18)
                .encode(text="text:N")
            )

        # Create a placeholder for cash flows until actual data is available
        chart = (
            alt.Chart(
                pd.DataFrame(
                    {
                        "Year": [2022, 2022, 2022],
                        "Type": ["Operating", "Investing", "Financing"],
                        "Amount": [100, -30, -60],
                    }
                )
            )
            .mark_bar()
            .encode(
                x=alt.X("Type:N", title="Cash Flow Type"),
                y=alt.Y("Amount:Q", title="Amount ($M)"),
                color=alt.Color(
                    "Type:N",
                    scale=alt.Scale(
                        domain=["Operating", "Investing", "Financing"],
                        range=["#70AD47", "#F79646", "#4F81BD"],
                    ),
                    legend=alt.Legend(orient="bottom", title=None),
                ),
                tooltip=["Type", alt.Tooltip("Amount:Q", format=",.0f")],
            )
            .properties(width="container")
        )
        return chart

    # footer date
    @render.text
    def last_updated_date():
        return datetime.now().strftime("%B %d, %Y")


# Create app
app = App(app_ui, server)
