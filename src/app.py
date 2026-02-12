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

# UI
app_ui = ui.page_fillable(
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
        .section-label-blue { background-color: #2980b9; }
        .section-label-red { background-color: #c0392b; }
        .kpi-big { font-size: 2em; font-weight: bold; }
        .kpi-label { font-size: 0.9em; color: #666; }
    """),

    # Title
    ui.h2("Financial Health Dashboard"),
    ui.p("A comprehensive KPI dashboard highlighting key financial metrics across public companies."),

    ui.layout_sidebar(
        # ---- Sidebar with filters ----
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
            # Vertical label
            ui.div(ui.div("PROFITABILITY", class_="section-label"), style="display:flex; align-items:stretch;"),

            # Net Profit Margin card
            ui.card(
                ui.card_header("Net Profit Margin"),
                ui.div(
                    ui.span("25.3%", class_="kpi-big"),
                    ui.br(),
                    ui.span("[Sparkline chart placeholder — margin trend over years]", class_="kpi-label"),
                ),
            ),

            # ROE card
            ui.card(
                ui.card_header("Return on Equity (ROE)"),
                ui.div(
                    ui.span("196.96%", class_="kpi-big"),
                    ui.br(),
                    ui.span("[Sparkline chart placeholder — ROE trend over years]", class_="kpi-label"),
                ),
            ),

            # Revenue & Net Income card
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

            # Revenue over time chart
            ui.card(
                ui.card_header("Revenue Over Time"),
                ui.p("[Bar chart placeholder — yearly revenue from 2009-2023]"),
            ),
        ),

        # Financial health row
        ui.layout_columns(
            # Vertical label
            ui.div(ui.div("FINANCIAL HEALTH", class_="section-label"), style="display:flex; align-items:stretch;"),

            # Current Ratio card
            ui.card(
                ui.card_header("Current Ratio"),
                ui.div(
                    ui.span("0.88", class_="kpi-big"),
                    ui.br(),
                    ui.span("Current Ratio over time", class_="kpi-label"),
                ),
                ui.p("[Line chart placeholder — current ratio by year]"),
            ),
        ),     
    ),
)

# Server
def server(input, output, session):
    @reactive.effect
    @reactive.event(input.category)
    def _update_company_choices():
        companies = CATEGORY_COMPANIES.get(input.category(), [])
        ui.update_select("company", choices=companies, selected=companies[0])


# Create app
app = App(app_ui, server)
