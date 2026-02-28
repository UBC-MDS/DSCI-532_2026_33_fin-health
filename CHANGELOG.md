# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - (2026-03-08)

### Added
- Implementation of Page 2

## [v0.2.0] - (2026-02-28)

### Added
- **Analytics Filters**: Implemented slider for period (year), dropdowns for sector and metric within `ui.sidebar()`
- **Reactive Altair visualizations**: Sector profitability bar chart, Metric trend analysis over time, peer benchmarking scatter plot
- **Company detail table** displaying key financial indicators filtered by selected year range and sector
- **KPI summary cards**: Text outputs displayed in `ui.card()` including - Average profit margin, Top sector by margin, Year-over-year revenue growth
- **Trend indicators**: Added `p1_margin_trend` and `p1_revenue_trend` with `▲`/`▼` arrows comparing most recent year to previous year
- **Margin badge** (`p1_margin_badge`): Displays "BASED ON {n} COMPANIES" below average profit margin KPI
- **Data loading and core reactivity**: Implemented `p1_filtered_data` reactive calculation to filter `financial_statement.csv` based on selected year range and sector.
- **Deployment pipeline**: Configured deployment on Posit Connect Cloud with - Stable build from `main`, preview build from `dev`
- **Multi-page layout** (complexity enhancement): Page 1 (Sector Analysis) and Page 2 (Company Health) via `ui.page_navbar()`
- **Custom CSS stylesheet** (`assets/custom_styles.css`): Added external stylesheet with design tokens (CSS variables), card elevation and hover effects, KPI typography, trend indicators, table styling, sidebar and navbar theming
- **Footer Section**: Added dashboard metadata including project description, team members, repository link and last updated details
- **M2 spec document** (`reports/m2_spec.md`): Component inventory, reactivity diagram, and calculation details for all 18 Page 1 components

### Changed
- **Filter layout redesign**: Moved all dashboard filters to a collapsible sidebar to improve layout organization and maximize space for charts and tables.
- Added Index Performance: % Net Margin below Top Sector in the `ui.card()`

### Fixed
- **Data normalization issue**: Resolved inconsistencies caused by mixed-case sector categories (e.g., "BANK" vs "bank") in the source dataset.

### Known Issues
- **Page 2 (Company Health)**: Currently uses hardcoded placeholder values. Full company-level analysis will be implemented in Milestone 3 (M3).
- **Filter reset functionality**: A reset option for dashboard filters has not yet been implemented.

### Reflection
- **User stories implemented (M1)**: All three user stories defined in Milestone 1 have been implemented:
    <br>Sector comparison: Sector profitability visualization (Chart A) combined with the Top Sector KPI.
    <br>Peer benchmarking: Benchmarking scatter plot (Chart C) supported by the company-level detail table (Table D).
    <br>Crisis resilience analysis: Metric trend visualization (Chart B) with Revenue growth KPI.
- **Layout improvements**: Moving filters to a collapsible sidebar improves dashboard readability and creates more space for visualizations while maintaining a consistent location for controls. Additionally, the Index Performance: % Net Margin below Top Sector KPI strengthens the dashboard’s summary layer by providing a quick benchmark comparison between the overall index and the best-performing sector.
- **Planned for M3**: Full implementation of Page 2 (Company Health) with company-level deep dive analytics and additional financial indicators.

## [v0.1.0] - (2026-02-14)

### Added

- **Dashboard application**: Multi-page Dash app with company/sector financial metrics (NPM, ROE, D/E ratio, cash flows, revenue trends) and a US Corporate Profitability page
- **Data and analysis**: Raw financial statement dataset, EDA notebook, and milestone 1 proposal
- **Project documentation**: README, CONTRIBUTING, CODE_OF_CONDUCT, and LICENSE (CC BY 4.0)
- **CI/CD and tooling**: GitHub Actions workflows for testing and docs, conda environment with lock file, and Quarto site config
- **GitHub templates**: PR, bug report, peer review, and milestone issue templates
- **Testing**: Placeholder test file
