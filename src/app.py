from shiny import App, reactive, render, ui

CATEGORY_COMPANIES = {
    "Bank": ["AIG", "BCS"],
    "ELEC": ["INTC", "NVDA"],
    "Finance": ["SHLDQ"],
    "FinTech": ["PYPL"],
    "FOOD": ["MCD"],
    "IT": ["AAPL", "GOOG", "MSFT"],
    "LOGI": ["AMZN"],
    "Manufacturing": ["PCG"],
}
ALL_CATEGORIES = sorted(CATEGORY_COMPANIES.keys())
ALL_SECTORS = ["Bank", "ELEC", "Finance", "FinTech", "FOOD", "IT", "LOGI", "Manufacturing"]

METRIC_CHOICES = [
    "Net Profit Margin",
    "ROE",
    "ROA",
    "ROI",
    "Revenue",
    "Net Income",
    "EBITDA",
    "Current Ratio",
    "Debt/Equity Ratio",
]



# Page 1: Sector Analysis
def page1_sector_analysis():
    return ui.page_fillable(
        ui.tags.style("""
            .kpi-big { font-size: 2em; font-weight: bold; }
            .kpi-label { font-size: 0.9em; color: #666; }
        """),

        ui.h2("US Corporate Profitability Analytics"),


        ui.layout_columns(
            ui.card(
                ui.card_header("Avg Profit Margin"),
                ui.div(
                    ui.output_text("p1_avg_margin", inline=True),
                ),
            ),
            ui.card(
                ui.card_header("Top Sector"),
                ui.div(
                    ui.output_text("p1_top_sector", inline=True),
                ),
            ),
            ui.card(
                ui.card_header("Revenue Growth"),
                ui.div(
                    ui.output_text("p1_revenue_growth", inline=True),
                ),
            ),
            col_widths=[4, 4, 4],
        ),

        # Sidebar + Charts
        ui.layout_sidebar(
            ui.sidebar(
                ui.h4("Filters"),
                ui.input_slider(
                    id="p1_year_range",
                    label="Period",
                    min=2009,
                    max=2022,
                    value=[2009, 2022],
                    sep="",
                ),
                ui.input_select(
                    id="p1_sector",
                    label="Sector",
                    choices=["All"] + ALL_SECTORS,
                    selected="All",
                ),
                ui.input_select(
                    id="p1_metric",
                    label="Metric",
                    choices=METRIC_CHOICES,
                    selected="Net Profit Margin",
                ),
                open="desktop",
            ),
            # Row 1: bar + line
            ui.layout_columns(
                ui.card(
                    ui.card_header("A. Sector Profitability"),
                    ui.output_ui("p1_chart_a"),
                ),
                ui.card(
                    ui.card_header("B. Profitability Trend"),
                    ui.output_ui("p1_chart_b"),
                ),
                col_widths=[6, 6],
            ),
            # Row 2: scatter + table
            ui.layout_columns(
                ui.card(
                    ui.card_header("C. Peer Benchmarking"),
                    ui.output_ui("p1_chart_c"),
                ),
                ui.card(
                    ui.card_header("D. Company Detail"),
                    ui.output_data_frame("p1_table_d"),
                ),
                col_widths=[6, 6],
            ),
        ),
    )


# Page 2: Company Financial Health
def page2_company_health():
    return ui.page_fillable(
        ui.tags.style("""
            .section-label {
                writing-mode: vertical-rl;
                text-orientation: upright;
                color: white;
                font-weight: bold;
                padding: 10px 6px;
                border-radius: 6px;
                text-align: center;
                letter-spacing: 4px;
                font-size: 0.7em;
            }
            .label-wrapper {
                display: flex;
                align-items: stretch;
                height: 100%;
            }
            .section-label-blue { background-color: #2980b9; }
            .section-label-red { background-color: #c0392b; }
            .kpi-big { font-size: 2em; font-weight: bold; }
            .kpi-label { font-size: 0.9em; color: #666; }
        """),
        ui.h2("Financial Health Dashboard"),
        ui.p("A comprehensive KPI dashboard highlighting key financial metrics of public companies."),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h4("Filters"),
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
            # Profitability row
            ui.layout_columns(
                ui.div(
                    ui.div("PROFITABILITY", class_="section-label section-label-blue"),
                    class_="label-wrapper",
                ),
                ui.card(
                    ui.card_header("Net Profit Margin"),
                    ui.div(
                        ui.span("25.3%", class_="kpi-big"),
                        ui.br(),
                        ui.span("[Sparkline chart placeholder]", class_="kpi-label"),
                    ),
                ),
                ui.card(
                    ui.card_header("Return on Equity (ROE)"),
                    ui.div(
                        ui.span("196.96%", class_="kpi-big"),
                        ui.br(),
                        ui.span("[Sparkline chart placeholder]", class_="kpi-label"),
                    ),
                ),
                ui.card(
                    ui.card_header("Revenue & Net Income"),
                    ui.div(
                        ui.span("$394,328M", class_="kpi-big"),
                        ui.br(),
                        ui.span("Revenue", class_="kpi-label"),
                        ui.br(), ui.br(),
                        ui.span("$99,803M", class_="kpi-big"),
                        ui.br(),
                        ui.span("Net Income", class_="kpi-label"),
                    ),
                ),
                ui.card(
                    ui.card_header("Revenue Over Time"),
                    ui.p("[Bar chart placeholder — yearly revenue from 2009-2023]"),
                ),
                col_widths=[1, 2, 2, 3, 4],
            ),
            # Financial health row
            ui.layout_columns(
                ui.div(
                    ui.div("FINANCIAL HEALTH", class_="section-label section-label-red"),
                    class_="label-wrapper",
                ),
                ui.card(
                    ui.card_header("Current Ratio"),
                    ui.div(
                        ui.span("0.88", class_="kpi-big"),
                        ui.br(),
                        ui.span("Current Ratio over time", class_="kpi-label"),
                    ),
                    ui.p("[Line chart placeholder]"),
                ),
                ui.card(
                    ui.card_header("Debt / Equity Ratio"),
                    ui.div(
                        ui.span("2.37", class_="kpi-big"),
                        ui.br(),
                        ui.span("Debt/Equity over time", class_="kpi-label"),
                    ),
                    ui.p("[Line chart placeholder]"),
                ),
                ui.card(
                    ui.card_header("Cash Flows"),
                    ui.div(
                        ui.span("Operating: $122,151M", class_="kpi-label"),
                        ui.br(),
                        ui.span("Investing: -$22,354M", class_="kpi-label"),
                        ui.br(),
                        ui.span("Financing: -$110,749M", class_="kpi-label"),
                    ),
                    ui.p("[Grouped bar chart placeholder]"),
                ),
                col_widths=[1, 4, 4, 3],
            ),
        ),
    )


app_ui = ui.page_navbar(
    ui.nav_panel("Sector Analysis", page1_sector_analysis()),
    ui.nav_panel("Company Health", page2_company_health()),
    title="fin-health",
    id="main_nav",
    fillable=True,
)


def server(input, output, session):

    # Page 1: Sector Analysis
    @reactive.calc
    def p1_filtered_data():
        """Placeholder: will filter df by year range and sector."""
        return None

    @render.text
    def p1_avg_margin():
        p1_filtered_data()
        return "14.2%"

    @render.text
    def p1_top_sector():
        p1_filtered_data()
        return "Tech"

    @render.text
    def p1_revenue_growth():
        p1_filtered_data()
        return "+5.8%"

    @render.ui
    def p1_chart_a():
        p1_filtered_data()
        return ui.p("[Bar chart placeholder — comparing avg metric across sectors]")

    @render.ui
    def p1_chart_b():
        p1_filtered_data()
        return ui.p("[Line chart placeholder — metric trend over time by sector]")

    @render.ui
    def p1_chart_c():
        p1_filtered_data()
        return ui.p("[Scatter plot placeholder — Revenue vs Net Income]")

    @render.data_frame
    def p1_table_d():
        p1_filtered_data()
        return None

    # Page 2: Company Financial Health
    @reactive.effect
    @reactive.event(input.category)
    def _update_company_choices():
        companies = CATEGORY_COMPANIES.get(input.category(), [])
        ui.update_select("company", choices=companies, selected=companies[0])


# Create app
app = App(app_ui, server)
