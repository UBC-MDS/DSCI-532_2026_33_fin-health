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
                )
            )
        ),
    )
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
