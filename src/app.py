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

# Custon CSS
CSS_PATH = Path(__file__).parent.parent / "assets" / "custom_styles.css"
with open(CSS_PATH, "r") as css_file:
    CUSTOM_CSS = ui.tags.style(css_file.read())

# Navbar with page tabs
nav_sector = ui.nav_panel("Sector Analysis", sector_ui())
nav_company = ui.nav_panel("Company Health", company_ui())
nav_ai = ui.nav_panel("fin-chat", ai_explorer_ui())

# Dark theme toggle button (sun/moon icon, persists via localStorage)
theme_toggle = ui.nav_control(
    ui.tags.button(
        ui.HTML(
            '<svg id="theme-icon-moon" xmlns="http://www.w3.org/2000/svg" width="16" '
            'height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
            '<svg id="theme-icon-sun" xmlns="http://www.w3.org/2000/svg" width="16" '
            'height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            'style="display:none;">'
            '<circle cx="12" cy="12" r="5"/>'
            '<line x1="12" y1="1" x2="12" y2="3"/>'
            '<line x1="12" y1="21" x2="12" y2="23"/>'
            '<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>'
            '<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>'
            '<line x1="1" y1="12" x2="3" y2="12"/>'
            '<line x1="21" y1="12" x2="23" y2="12"/>'
            '<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>'
            '<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
        ),
        id="theme-toggle",
        class_="btn btn-sm btn-outline-secondary border-0",
        title="Toggle dark mode",
        onclick=(
            "document.body.classList.toggle('dark-theme');"
            "var isDark = document.body.classList.contains('dark-theme');"
            "localStorage.setItem('theme', isDark ? 'dark' : 'light');"
            "document.getElementById('theme-icon-moon').style.display = isDark ? 'none' : '';"
            "document.getElementById('theme-icon-sun').style.display = isDark ? '' : 'none';"
        ),
    )
)

# Restore saved theme on page load
theme_restore_script = ui.tags.script(
    "(function(){"
    "if(localStorage.getItem('theme')==='dark'){"
    "document.body.classList.add('dark-theme');"
    "var m=document.getElementById('theme-icon-moon');"
    "var s=document.getElementById('theme-icon-sun');"
    "if(m)m.style.display='none';"
    "if(s)s.style.display='';"
    "}"
    "})();"
)

navbar = ui.page_navbar(
    nav_sector,
    nav_company,
    nav_ai,
    ui.nav_spacer(),
    theme_toggle,
    title="fin-health",
    id="main_nav",
    fillable=True,
)

# Footer
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
            style="text-align: center; font-size: 0.85em; color: var(--slate-600);",
        ),
        class_="footer-container",
    )
)

app_ui = ui.page_fluid(CUSTOM_CSS, navbar, footer, theme_restore_script)


def server(input, output, session):
    sector_server(input, output, session)
    company_server(input, output, session)
    ai_explorer_server(input, output, session)


app = App(app_ui, server)
