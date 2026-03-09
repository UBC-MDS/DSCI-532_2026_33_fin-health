"""Page 2: Company Financial Health — UI layout and server logic."""

from shiny import reactive, render, ui
from shinywidgets import output_widget, render_altair

from charts.altair_charts import (
    build_cash_flows,
    build_ratio_over_time,
    build_revenue_over_time,
)
from components.empty_chart import empty_chart
from data import ALL_SECTORS, CATEGORY_COMPANIES, df


def company_ui():
    """Return the full Page 2 layout."""
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
    year_select = ui.output_ui("p2_year_slider")
    sidebar = ui.sidebar(
        ui.h4("Analytics Filters"),
        category_select,
        company_select,
        year_select,
        open="desktop",
    )

    # Profitability cards — mirror Financial Health layout (KPI + status + chart)
    card_npm = ui.card(
        ui.card_header("Net Profit Margin"),
        ui.div(
            ui.tags.h3(
                ui.output_text("p2_npm", inline=True),
                class_="kpi-value",
                style="display: inline;",
            ),
            ui.output_ui("p2_npm_status", style="display: inline;"),
            class_="kpi-value-row",
        ),
        output_widget("p2_npm_chart"),
        full_screen=True,
    )
    card_roe = ui.card(
        ui.card_header("Return on Equity (ROE)"),
        ui.div(
            ui.tags.h3(
                ui.output_text("p2_roe", inline=True),
                class_="kpi-value",
                style="display: inline;",
            ),
            ui.output_ui("p2_roe_status", style="display: inline;"),
            class_="kpi-value-row",
        ),
        output_widget("p2_roe_chart"),
        full_screen=True,
    )
    card_rev_income = ui.card(
        ui.card_header("Revenue & Net Income"),
        ui.output_ui("p2_rev_income_summary"),
        output_widget("p2_revenue_chart"),
        full_screen=True,
    )
    profitability_section = ui.div(
        ui.div("PROFITABILITY", class_="section-label section-label-blue"),
        ui.layout_columns(
            card_npm,
            card_roe,
            card_rev_income,
            col_widths=[4, 4, 4],
        ),
        class_="grid-section grid-section-blue",
    )

    # Financial Health cards (reactive outputs)
    card_current_ratio = ui.card(
        ui.card_header("Current Ratio"),
        ui.div(
            ui.tags.h3(
                ui.output_text("p2_current_ratio", inline=True),
                class_="kpi-value",
                style="display: inline;",
            ),
            ui.output_ui("p2_current_ratio_status", style="display: inline;"),
            class_="kpi-value-row",
        ),
        output_widget("p2_current_ratio_chart"),
        full_screen=True,
    )
    card_debt_equity = ui.card(
        ui.card_header("Debt / Equity Ratio"),
        ui.div(
            ui.tags.h3(
                ui.output_text("p2_debt_equity", inline=True),
                class_="kpi-value",
                style="display: inline;",
            ),
            ui.output_ui("p2_debt_equity_status", style="display: inline;"),
            class_="kpi-value-row",
        ),
        output_widget("p2_debt_equity_chart"),
        full_screen=True,
    )
    card_cash_flows = ui.card(
        ui.card_header("Cash Flows"),
        ui.output_ui("p2_cash_flows"),
        output_widget("p2_cash_flow_chart"),
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
        class_="grid-section grid-section-red",
    )

    return ui.layout_sidebar(
        sidebar,
        ui.page_fillable(
            ui.h2("Financial Health Dashboard"),
            profitability_section,
            health_section,
        ),
    )


def company_server(input, output, session):
    """Page 2 reactive logic."""

    @reactive.effect
    @reactive.event(input.category)
    def _update_company_choices():
        companies = CATEGORY_COMPANIES.get(input.category(), [])
        selected = companies[0] if companies else None
        ui.update_select("company", choices=companies, selected=selected)

    @render.ui
    def p2_year_slider():
        company = input.company()
        company_data = df[df["Company"] == company]
        if company_data.empty:
            year_min = int(df["Year"].min())
            year_max = int(df["Year"].max())
        else:
            year_min = int(company_data["Year"].min())
            year_max = int(company_data["Year"].max())
        if year_min == year_max:
            return ui.div(
                ui.tags.label("Year", class_="control-label"),
                ui.tags.p(str(year_max), style="font-weight: 600; font-size: 1.1rem;"),
                ui.input_slider(
                    id="year", label="", min=year_min, max=year_max,
                    value=year_max, sep="",
                ),
                ui.tags.style("#year-label { display: none; } #year .irs { display: none; }"),
            )
        return ui.input_slider(
            id="year", label="Year", min=year_min, max=year_max,
            value=year_max, sep="",
        )

    @reactive.calc
    def p2_filtered_data():
        category = input.category()
        company = input.company()
        year = input.year()
        return df[
            (df["Category"] == category)
            & (df["Company"] == company)
            & (df["Year"] == year)
        ]

    # --- Profitability KPIs ---

    @render.text
    def p2_npm():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "N/A"
        value = filtered["Net Profit Margin"].iloc[0]
        return f"{value:.1f}%"

    @render.text
    def p2_roe():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "N/A"
        value = filtered["ROE"].iloc[0]
        return f"{value:.2f}%"

    @render.ui
    def p2_npm_status():
        filtered = p2_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        value = filtered["Net Profit Margin"].iloc[0]
        if value >= 10:
            return ui.tags.span("\u2713", class_="kpi-status healthy")
        elif value >= 0:
            return ui.tags.span("!", class_="kpi-status warning")
        else:
            return ui.tags.span("\u2717", class_="kpi-status danger")

    @render_altair
    def p2_npm_chart():
        company = input.company()
        company_data = df[df["Company"] == company]
        if company_data.empty:
            return empty_chart()
        return build_ratio_over_time(company_data, company, "Net Profit Margin")

    @render.ui
    def p2_roe_status():
        filtered = p2_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        value = filtered["ROE"].iloc[0]
        if value >= 15:
            return ui.tags.span("\u2713", class_="kpi-status healthy")
        elif value >= 0:
            return ui.tags.span("!", class_="kpi-status warning")
        else:
            return ui.tags.span("\u2717", class_="kpi-status danger")

    @render_altair
    def p2_roe_chart():
        company = input.company()
        company_data = df[df["Company"] == company]
        if company_data.empty:
            return empty_chart()
        return build_ratio_over_time(company_data, company, "ROE")

    @render.ui
    def p2_rev_income_summary():
        filtered = p2_filtered_data()
        if filtered.empty:
            return ui.div("N/A")
        rev = filtered["Revenue"].iloc[0]
        ni = filtered["Net Income"].iloc[0]
        return ui.div(
            ui.span(f"Revenue: ${rev:,.0f}M", class_="kpi-label"),
            ui.span(" | ", style="color: var(--slate-400);"),
            ui.span(f"Net Income: ${ni:,.0f}M", class_="kpi-label"),
            style="padding: 0.25rem 0; text-align: center;",
        )

    @render_altair
    def p2_revenue_chart():
        company = input.company()
        company_data = df[df["Company"] == company]
        if company_data.empty:
            return empty_chart()
        return build_revenue_over_time(company_data, company)

    # --- Financial Health KPIs ---

    @render.text
    def p2_current_ratio():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "N/A"
        value = filtered["Current Ratio"].iloc[0]
        return f"{value:.2f}"

    @render_altair
    def p2_current_ratio_chart():
        company = input.company()
        company_data = df[df["Company"] == company]
        if company_data.empty:
            return empty_chart()
        return build_ratio_over_time(company_data, company, "Current Ratio")

    @render.text
    def p2_debt_equity():
        filtered = p2_filtered_data()
        if filtered.empty:
            return "N/A"
        value = filtered["Debt/Equity Ratio"].iloc[0]
        return f"{value:.2f}"

    @render_altair
    def p2_debt_equity_chart():
        company = input.company()
        company_data = df[df["Company"] == company]
        if company_data.empty:
            return empty_chart()
        return build_ratio_over_time(company_data, company, "Debt/Equity Ratio")

    @render.ui
    def p2_cash_flows():
        filtered = p2_filtered_data()
        if filtered.empty:
            return ui.div("N/A")
        row = filtered.iloc[0]
        op = row["Cash Flow from Operating"]
        inv = row["Cash Flow from Investing"]
        fin = row["Cash Flow from Financial Activities"]
        def fmt(v):
            return f"-${abs(v):,.0f}M" if v < 0 else f"${v:,.0f}M"
        return ui.div(
            ui.span(f"Operating: {fmt(op)}", class_="kpi-label"),
            ui.br(),
            ui.span(f"Investing: {fmt(inv)}", class_="kpi-label"),
            ui.br(),
            ui.span(f"Financing: {fmt(fin)}", class_="kpi-label"),
            style="text-align: center;",
        )

    @render.ui
    def p2_current_ratio_status():
        filtered = p2_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        value = filtered["Current Ratio"].iloc[0]
        if value >= 1.5:
            return ui.tags.span("\u2713", class_="kpi-status healthy")
        elif value >= 1.0:
            return ui.tags.span("!", class_="kpi-status warning")
        else:
            return ui.tags.span("\u2717", class_="kpi-status danger")

    @render.ui
    def p2_debt_equity_status():
        filtered = p2_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        value = filtered["Debt/Equity Ratio"].iloc[0]
        if value <= 1.0:
            return ui.tags.span("\u2713", class_="kpi-status healthy")
        elif value <= 2.0:
            return ui.tags.span("!", class_="kpi-status warning")
        else:
            return ui.tags.span("\u2717", class_="kpi-status danger")

    @render_altair
    def p2_cash_flow_chart():
        company = input.company()
        company_data = df[df["Company"] == company]
        if company_data.empty:
            return empty_chart()
        return build_cash_flows(company_data, company)
