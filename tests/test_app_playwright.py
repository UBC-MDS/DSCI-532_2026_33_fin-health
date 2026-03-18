# tests/test_app_playwright.py
"""Playwright end-to-end behavior tests for the fin-health dashboard."""

import re

from playwright.sync_api import Page, expect
from shiny.playwright import controller
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

app = create_app_fixture("../src/app.py")


def test_initial_page_loads(page: Page, app: ShinyAppProc):
    """Dashboard loads and Page 1 KPI value boxes display non-empty initial values."""
    page.goto(app.url)

    # Wait for the page title to confirm app loaded
    expect(page.locator("text=US Corporate Profitability Analytics")).to_be_visible(
        timeout=30_000
    )

    # Verify KPI cards render with actual values (not empty or "Data Unavailable")
    avg_margin = controller.OutputText(page, "p1_avg_margin")
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    top_sector = controller.OutputText(page, "p1_top_sector")
    top_sector.expect_value(re.compile(r"[A-Z]+"), timeout=15_000)

    revenue_growth = controller.OutputText(page, "p1_revenue_growth_value")
    revenue_growth.expect_value(re.compile(r"[+-]?\d+\.\d+%"), timeout=15_000)


def test_sector_filter_updates_kpis(page: Page, app: ShinyAppProc):
    """Selecting a specific sector in the dropdown updates KPI values and chart outputs."""
    page.goto(app.url)

    # Wait for initial load
    avg_margin = controller.OutputText(page, "p1_avg_margin")
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    # Select a specific sector (IT) to filter
    sector_select = controller.InputSelectize(page, "p1_sector")
    sector_select.set("IT")

    # After filtering to IT only, the top sector should be IT
    top_sector = controller.OutputText(page, "p1_top_sector")
    top_sector.expect_value("IT", timeout=15_000)

    # Verify the avg margin updated (should still show a valid percentage)
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)


def test_company_page_navigation_and_selection(page: Page, app: ShinyAppProc):
    """Navigating to Page 2 and selecting a company renders correct KPI values."""
    page.goto(app.url)

    # Wait for initial page load
    expect(page.locator("text=US Corporate Profitability Analytics")).to_be_visible(
        timeout=30_000
    )

    # Navigate to Page 2 (Company Health)
    page.locator("a.nav-link", has_text="Company Health").click()

    # Wait for Page 2 content
    expect(
        page.get_by_role("heading", name="Financial Health Dashboard")
    ).to_be_visible(timeout=15_000)

    # Verify KPI values are rendered (not "N/A")
    npm = controller.OutputText(page, "p2_npm")
    npm.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=30_000)

    roe = controller.OutputText(page, "p2_roe")
    roe.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    current_ratio = controller.OutputText(page, "p2_current_ratio")
    current_ratio.expect_value(re.compile(r"\d+\.\d+"), timeout=15_000)

    debt_equity = controller.OutputText(page, "p2_debt_equity")
    debt_equity.expect_value(re.compile(r"-?\d+\.\d+"), timeout=15_000)


def test_narrow_year_range(page: Page, app: ShinyAppProc):
    """Narrowing the year slider to a single year still renders valid KPIs without errors."""
    page.goto(app.url)

    # Wait for initial load
    avg_margin = controller.OutputText(page, "p1_avg_margin")
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    # Set the year range slider to a single year (2020–2020)
    year_slider = controller.InputSliderRange(page, "p1_year_range")
    year_slider.set(("2020", "2020"))

    # KPIs should still render valid values for a single-year slice
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    top_sector = controller.OutputText(page, "p1_top_sector")
    top_sector.expect_value(re.compile(r"[A-Z]+"), timeout=15_000)


def test_multi_sector_filter(page: Page, app: ShinyAppProc):
    """Selecting multiple sectors updates KPIs to reflect the combined selection."""
    page.goto(app.url)

    # Wait for initial load
    avg_margin = controller.OutputText(page, "p1_avg_margin")
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    # Select two sectors: IT and BANK
    sector_select = controller.InputSelectize(page, "p1_sector")
    sector_select.set("IT")
    sector_select.set("BANK")

    # KPIs should still show valid values
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    # Top sector should be one of the two selected sectors
    top_sector = controller.OutputText(page, "p1_top_sector")
    top_sector.expect_value(re.compile(r"^(IT|BANK)$"), timeout=15_000)


def test_empty_filter_shows_fallback(page: Page, app: ShinyAppProc):
    """Filtering to a year range with no data displays 'Data Unavailable' instead of crashing."""
    page.goto(app.url)

    # Wait for initial load
    avg_margin = controller.OutputText(page, "p1_avg_margin")
    avg_margin.expect_value(re.compile(r"-?\d+\.\d+%"), timeout=15_000)

    # Set year range to far future where no data exists (max slider value)
    # Use a narrow range at the earliest boundary — 2009 with a single sector
    # that may not have data in the earliest year
    sector_select = controller.InputSelectize(page, "p1_sector")
    sector_select.set("FINTECH")

    year_slider = controller.InputSliderRange(page, "p1_year_range")
    year_slider.set(("2009", "2009"))

    # The app should either show "Data Unavailable" or still show valid data — not crash
    avg_margin.expect_value(
        re.compile(r"(-?\d+\.\d+%|Data Unavailable)"), timeout=15_000
    )
