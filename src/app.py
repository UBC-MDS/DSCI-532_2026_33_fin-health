"""fin-health dashboard — entry point."""

import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from shiny import App, ui  # noqa: E402

from pages.company import company_server, company_ui  # noqa: E402
from pages.sector import sector_server, sector_ui  # noqa: E402
from pages.ai_explorer import ai_explorer_server, ai_explorer_ui  # noqa: E402

CSS_PATH = Path(__file__).parent.parent / "assets" / "custom_styles.css"
with open(CSS_PATH, "r") as css_file:
    CUSTOM_CSS = ui.tags.style(css_file.read())


nav_sector = ui.nav_panel("Sector Analysis", sector_ui())
nav_company = ui.nav_panel("Company Health", company_ui())
nav_ai = ui.nav_panel("fin-chat", ai_explorer_ui())
navbar = ui.page_navbar(
    nav_sector,
    nav_company,
    nav_ai,
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
    sector_server(input, output, session)
    company_server(input, output, session)
    ai_explorer_server(input, output, session)


app = App(app_ui, server)
