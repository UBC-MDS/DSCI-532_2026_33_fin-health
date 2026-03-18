# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.4.0] - (2026-03-17)

### Added
- **Parquet + DuckDB Backend**: Migrated data loading to `ibis.duckdb.connect()` + `con.read_parquet()` for lazy query execution and improved performance.
- **RAG Finance Glossary**: Integrated a knowledge base (`knowledge/glossary.md`) into querychat for retrieval-augmented financial term definitions.
- **Playwright Behavior Tests**: Added 3 browser-based behavior tests covering distinct dashboard interactions.
- **Unit Tests**: Added pytest unit tests for refactored `classify_health()` and `format_currency()` helper functions.

### Changed
- **Data Pipeline**: Replaced CSV-based `pandas.read_csv()` with parquet-based `ibis` expressions; all filtering now happens at the database level before materializing to pandas.
- **Health Status Refactor**: Extracted repeated threshold-based health classification logic from `company.py` into a reusable, testable `classify_health()` pure function in `components/health_status.py`.
- **Currency Formatting**: Extracted inline `fmt()` closure into a standalone `format_currency()` helper for consistency and testability.
- **Dependencies**: Added `ibis-framework[duckdb]` and `playwright` to `requirements.txt` and `environment.yml`.

### Fixed

Fixed the following from feedback:

- Add tooltips for green check and yellow exclamation mark in Company Health page ([#94](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/94))
- Remove "All" option and defaulted to all sectors when no sectors are chosen ([#96](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/96))
- Make the top KPI cards 4 cards instead of 3 ([#97](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/97))
- Add transparency in the scatterplot for better readability ([#95](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/95))
- Clarify financial metrics with tooltips ([#94](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/94))
- Fixed Revenue vs Revenue plot for the Peer Benchmarking and now defaults to Revenue vs Net Profit Margin ([#95](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/95))

### Known Issues
- **fin-chat requires API token**: The fin-chat page requires a `GITHUB_TOKEN` environment variable; without it, a fallback message is displayed.
- **Querychat latency**: LLM-powered queries may take 2-5 seconds depending on API response time.

### Release Highlight: TF-IDF RAG Finance Glossary

We added per-query retrieval-augmented generation (RAG) to the fin-chat page so users unfamiliar with financial terminology get accurate, domain-grounded answers. A ~560-line glossary (`data/knowledge_base/finance_glossary.txt`) covering all 20+ metrics in the dataset—definitions, formulas, healthy ranges, and sector-specific benchmarks—is chunked by heading and indexed with a TF-IDF vectorizer. On every user question, the top-3 most relevant chunks are retrieved via cosine similarity and injected into the user message before it reaches the LLM. For example, asking "Is a current ratio of 0.7 concerning?" now returns a nuanced, sector-aware answer citing the glossary's thresholds instead of generic training-data knowledge.

- **Option chosen:** C — RAG-based contextual help
- **PR:** [#87](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/pull/87)
- **Why this option over the others:** Users without finance backgrounds need clear, consistent metric explanations when exploring the dashboard; a domain glossary with per-query TF-IDF retrieval ensures citation-backed answers without requiring an external embedding API or model download.
- **Feature prioritization issue link:** [#86](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/86)

### Collaboration

After M3 feedback highlighted blocking dependencies and slow PR reviews, we adopted a spec-first, scoped-PR workflow for M4. Specs and CONTRIBUTING.md were updated and merged before any feature branch was created, giving every team member written context on intent and scope. Work was split across separate files so all four members could code in parallel without merge conflicts: Jiro on `data.py` and page filtering, Seungmyun on `ai_explorer.py` and the knowledge base, Shruti on playwright tests, Luke on function refactoring and unit tests. Each team member resolved at least one feedback item, and PRs were kept atomic (one feature or fix per PR, with conventional-commit messages and documentation updated alongside the code).

- **CONTRIBUTING.md:** [#79](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/pull/79)
- **M3 retrospective:** Blocking PRs (env setup) delayed downstream work; review turnaround was too slow; PRs lacked tests. We committed to merging blockers within 2 days, a 24-hour review SLA, and requiring at least one test per feature PR.
- **M4:** Specs merged before code; environment and data-migration PRs landed first to unblock the team; contributions were spread across the milestone rather than concentrated at the deadline. Daily async Slack stand-ups tracked progress and surfaced blockers early.

### Reflection

The dashboard now handles data loading, domain-aware chat, and testing end-to-end. Parquet + DuckDB via ibis pushes all filtering to the database layer so only the rows and columns needed for each view are materialized into pandas which is an  improvement for scalability. The TF-IDF RAG glossary gives fin-chat accurate, sector-aware answers grounded in a curated knowledge base rather than relying on the LLM's general training data. Playwright and pytest suites cover page navigation, filter behaviour, and refactored pure functions, catching regressions before deploy. A current limitation is that TF-IDF retrieval relies on exact term overlap; queries with synonyms or paraphrases may miss relevant chunks. Upgrading to semantic embeddings would address this but adds an external dependency we chose to avoid.

We prioritised all critical feedback items and deferred only cosmetic suggestions — full rationale is in [#76](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues/76) and the Changed section of the CHANGELOG.

The lecture material on RAG and prompting shaped this milestone most directly.  It informed the chunk-and-retrieve architecture for the glossary and the decision to inject context into the user message rather than the system prompt. We would have benefited from earlier coverage of end-to-end testing with playwright as we mostly adopted a test-driven development from the start.

#### Tests

For each of the testing modules, we have laid out the test coverage, and what would break if behavior changed.

##### `test_data.py` — Data loading, constants, and KPI logic

| Test | Behavior verified | What breaks if it changes |
|------|-------------------|---------------------------|
| `test_connection_is_duckdb` | The ibis backend is DuckDB, not SQLite or another engine. | Queries that depend on DuckDB-specific behavior (e.g., parquet reads) would silently return wrong results or fail. |
| `test_tbl_is_ibis_table` | `tbl` is a lazy ibis Table expression, not an eagerly-loaded DataFrame. | All reactive calcs in `sector.py` and `company.py` that chain `.filter()` on `tbl` would raise `AttributeError`. |
| `test_df_is_pandas_dataframe` | `df` materializes to a non-empty pandas DataFrame. | Every chart builder and querychat module that consumes `df` directly would receive `None` or an empty frame. |
| `test_expected_columns_present` | Key columns (`Year`, `Company`, `Category`, all metrics) exist in the dataset. | Any page referencing a missing column (e.g., `filtered["Net Profit Margin"]`) would raise `KeyError` at runtime. |
| `test_ibis_filter_returns_subset` | Filtering by `Category == "IT"` returns only IT rows and fewer rows than the full table. | Sector filtering on Page 1 could return unfiltered data, making the sector dropdown appear broken. |
| `test_year_range_constants` | `YEAR_MIN` and `YEAR_MAX` match the actual data boundaries. | The year slider on Pages 1 and 2 would show an incorrect range, potentially hiding data or showing empty years. |
| `test_all_sectors_sorted` | `ALL_SECTORS` is alphabetically sorted and matches `CATEGORY_COMPANIES` keys. | The sector dropdown would display unsorted or mismatched entries, confusing users. |
| `test_metric_choices_non_empty` | `METRIC_CHOICES` contains `Net Profit Margin`, `Revenue`, and other expected metrics. | The metric dropdown on Page 1 would be empty or missing key options, breaking chart rendering. |
| `test_category_companies_has_entries` | Every sector in `CATEGORY_COMPANIES` maps to a non-empty list of company tickers. | The cascading company dropdown on Page 2 would show no options for some sectors. |
| `test_index_margin_weighted_differs_from_simple` | Weighted margin differs from simple average, confirming the formula accounts for company scale. | If someone replaces the formula with `.mean()`, the Index Margin KPI would silently show the wrong number. |
| `test_index_margin_matches_manual_calculation` | The formula `(Net Income sum / Revenue sum) * 100` is internally consistent. | A refactor that changes operator precedence or column names would produce a different value. |
| `test_index_margin_zero_revenue_returns_zero` | Zero total revenue yields `0.0%` instead of `ZeroDivisionError`. | Extreme filter combinations that exclude all revenue data would crash the KPI card. |
| `test_revenue_growth_matches_manual` | YoY growth matches a hand-computed value from the two most recent years. | A change in sort order or `.iloc` indexing would silently compare the wrong pair of years. |
| `test_revenue_growth_single_year_returns_none` | Single-year data returns `None` so the KPI card shows "Data Unavailable". | Narrowing the year slider to a single year would crash with an `IndexError` instead of showing a fallback. |
| `test_revenue_growth_two_year_subset` | A two-year slice produces valid growth matching the expected formula. | Filtering to a short range could return `None` unexpectedly, hiding real growth data. |
| `test_company_year_lookup_returns_one_row` | Each company's latest year returns exactly 1 row. | Page 2 KPI cards use `.iloc[0]` — zero rows causes `IndexError`; multiple rows picks an arbitrary value. |
| `test_company_year_lookup_has_required_columns` | Each company row contains all 9 metric columns needed by Page 2. | A renamed or dropped column in the parquet file would cause `KeyError` on the Company Health page. |

##### `test_health_status.py` — Health classification and currency formatting

| Test | Behavior verified | What breaks if it changes |
|------|-------------------|---------------------------|
| `test_healthy_above_threshold` | Values above the healthy threshold classify as "healthy". | KPI status icons would show warning/danger for strong metrics, alarming users unnecessarily. |
| `test_healthy_at_threshold` | Boundary values (exactly at threshold) are inclusive for "healthy". | A company at exactly 10% NPM could flip between healthy and warning across page refreshes. |
| `test_warning_between_thresholds` | Values between warning and healthy thresholds classify as "warning". | Moderate-risk metrics would incorrectly appear as healthy or danger, hiding the amber zone. |
| `test_warning_at_threshold` | Boundary values at the warning threshold are inclusive for "warning". | Edge-case values would inconsistently classify, making the health badges unreliable. |
| `test_danger_below_warning` | Values below the warning threshold classify as "danger". | Critically poor metrics would not trigger the red danger icon, giving false confidence. |
| `test_npm_healthy/warning/danger` | Net Profit Margin thresholds (≥10% healthy, ≥0% warning, <0% danger). | The NPM status badge on Page 2 would misclassify companies. |
| `test_roe_healthy` | ROE ≥ 15% is healthy. | Strong-performing companies would show incorrect ROE status. |
| `test_current_ratio_healthy/warning/danger` | Current Ratio thresholds (≥1.5 healthy, ≥1.0 warning, <1.0 danger). | Liquidity risk signals on Page 2 would be wrong, masking companies unable to cover short-term debt. |
| `test_healthy/warning/danger_below/above` (lower-is-better) | Debt/Equity uses inverted logic (≤1.0 healthy, ≤2.0 warning, >2.0 danger). | Heavily leveraged companies would appear "healthy", hiding significant debt risk. |
| `test_debt_equity_healthy/danger` | Debt/Equity specific values confirm the inverted classification. | Same as above — the only lower-is-better metric would break silently. |
| `test_positive_value` | `format_currency(1234)` → `"$1,234M"`. | Cash flow labels on Page 2 would display raw floats instead of formatted dollar amounts. |
| `test_negative_value` | `format_currency(-567)` → `"-$567M"`. | Negative cash flows would show malformed strings (e.g., `$-567M`). |
| `test_zero` | `format_currency(0)` → `"$0M"`. | Zero values would render as blank or `$M`, making KPI cards look broken. |
| `test_large_value` | Large values include comma grouping (`"$120,000M"`). | Revenue figures in the hundreds of billions would be unreadable without separators. |
| `test_small_negative` | `-0.5` rounds to `"-$0M"`. | Sub-unit negatives could show `-$-0M` or similar formatting artifacts. |

##### `test_charts.py` — Chart builder functions

| Test | Behavior verified | What breaks if it changes |
|------|-------------------|---------------------------|
| `test_build_sector_bar_returns_chart` | Sector bar chart returns a valid Altair Chart. | Page 1 Sector Comparison card would render blank or throw a JS error. |
| `test_build_sector_bar_empty_data` | Sector bar handles empty DataFrame gracefully. | Extreme filters that return no data would crash instead of showing the "Data Unavailable" fallback. |
| `test_build_metric_trend_returns_chart` | Metric trend line chart renders correctly. | Page 1 Historical Trend card would fail to display. |
| `test_build_metric_trend_empty_data` | Metric trend handles empty data. | Same crash-on-empty-filter risk. |
| `test_build_peer_scatter_returns_chart` | Peer scatter plot renders. | Page 1 Peer Benchmarking card would break. |
| `test_build_peer_scatter_empty_data` | Peer scatter handles empty data. | Empty filters would crash the scatter plot. |
| `test_build_revenue_over_time_returns_chart` | Revenue & Net Income grouped bar renders for a single company. | Page 2 Revenue & Net Income card would fail. |
| `test_build_ratio_over_time_returns_chart` | Ratio trend line + area chart renders. | Page 2 NPM, ROE, Current Ratio, and Debt/Equity trend charts would all break. |
| `test_build_cash_flows_returns_chart` | Cash flow grouped bar chart renders. | Page 2 Cash Flows card would fail to display. |
| `test_build_company_comparison_bar_returns_chart` | Company comparison bar chart renders. | fin-chat adaptive Chart A would break when showing single-sector data. |
| `test_build_company_comparison_bar_empty_data` | Company comparison handles empty data. | Chat filters that return no data would crash Chart A. |
| `test_build_single_company_summary_returns_chart` | Single company horizontal bar renders. | fin-chat Chart A for single-company queries would fail. |
| `test_build_single_company_summary_empty_data` | Single company summary handles empty data. | Same crash risk for chat-driven single-company views. |
| `test_build_company_trend_returns_chart` | Multi-company trend line renders. | fin-chat Chart B for multi-company comparisons would fail. |
| `test_build_company_trend_empty_data` | Company trend handles empty data. | Empty chat filters would crash Chart B. |

##### `test_components.py` — UI component factories

| Test | Behavior verified | What breaks if it changes |
|------|-------------------|---------------------------|
| `test_kpi_card_returns_ui_element` | `kpi_card()` with minimal args returns a valid UI element. | KPI cards on Pages 1 and 2 would fail to render, leaving blank spaces in the layout. |
| `test_kpi_card_with_trend_and_label` | `kpi_card()` with optional trend/label slots renders correctly. | Cards with trend arrows and sublabels (Avg Profit Margin, Index Margin, Revenue Growth) would break. |
| `test_empty_chart_returns_altair_chart` | `empty_chart()` returns a valid Altair Chart. | Every chart's empty-data fallback would itself crash, causing cascading failures. |
| `test_empty_chart_custom_message` | `empty_chart("custom msg")` renders with the custom message. | Specific empty-state messages would revert to generic text or fail entirely. |

##### `test_app.py` — App-level smoke tests

| Test | Behavior verified | What breaks if it changes |
|------|-------------------|---------------------------|
| `test_data_loaded_successfully` | `df` loads as a non-empty DataFrame at app startup. | The entire app would fail on import — no page would render. |
| `test_expected_columns_present` | All key columns exist in the loaded DataFrame. | Any page referencing missing columns would crash with `KeyError`. |

##### `test_querychat_behavior.py` — LLM tool selection (requires `GITHUB_TOKEN`)

| Test | Behavior verified | What breaks if it changes |
|------|-------------------|---------------------------|
| `test_filter_uses_update_dashboard` | A filter prompt ("Show only IT companies") invokes `querychat_update_dashboard`. | The chat would run a query instead of filtering, so the dashboard table and charts wouldn't update. |
| `test_stats_use_querychat_query` | An aggregate question ("Average revenue by sector?") invokes `querychat_query`. | The chat would try to filter instead of querying, returning no statistical answer. |
| `test_response_has_structured_format` | Responses include structured format keywords from `EXTRA_INSTRUCTIONS`. | Chat answers would lack the consistent structure (Filters Applied / Key Stats / Insight) that users expect. |

##### `test_app_playwright.py` — End-to-end browser tests

| Test | Behavior verified | What breaks if it changes |
|------|-------------------|---------------------------|
| `test_initial_page_loads` | Dashboard loads and Page 1 KPIs display non-empty initial values. | A broken import, missing parquet file, or CSS regression would leave users on a blank or error page. |
| `test_sector_filter_updates_kpis` | Selecting "IT" in the sector dropdown updates KPIs (top sector becomes IT). | The reactive wiring between sidebar inputs and KPI outputs would be broken — filters would have no effect. |
| `test_company_page_navigation_and_selection` | Navigating to Page 2 renders all four KPI values (NPM, ROE, Current Ratio, Debt/Equity). | Page 2 would fail to load or show "N/A" for all cards after navigation. |
| `test_narrow_year_range` | Setting the year slider to a single year (2020–2020) still renders valid KPIs. | A single-year edge case would crash the trend calculations or show "Data Unavailable" incorrectly. |
| `test_multi_sector_filter` | Selecting two sectors (IT + BANK) updates KPIs to reflect the combined selection. | Multi-select filtering logic would break, showing data for only one sector or all sectors. |
| `test_empty_filter_shows_fallback` | Filtering to FINTECH + year 2009 (likely no data) shows "Data Unavailable" instead of crashing. | An impossible filter combination would crash the app instead of degrading gracefully. |

## [v0.3.0] - (2026-03-08)

### Added
- **Natural Language Querying**: Integrated a new `fin-chat` page featuring `querychat` for intuitive, natural-language data filtering and exploration.
- **Interactive Data Grid**: Added a dedicated Dataframe output component to display granular filtered data.
- **Intelligent Visualization**: Implemented two adaptive charts that automatically adjust their visualization type based on the dimensions and shape of the data.
- **Data Portability**: Included a CSV download button to allow users to export their filtered datasets for external analysis.
- **Company Health Deep Dive (Page 2)**:
    - Realized full reactivity for key performance indicators including Net Profit Margin, ROE, Current Ratio, and Debt/Equity.
    - Added time-series visualizations for Revenue, Financial Ratios, and Cash Flows.
    - Visual health status indicators (Healthy/Warning/Danger) for immediate KPI assessment.
- **Quality Assurance**: Added an LLM behavior testing suite and an evaluation dataset to ensure chat reliability.

### Changed
- **Modular Refactor**: Reconstructed the application into a scalable directory structure, separating logic into `data.py`, `components/`, `charts/`, and `pages/`.
- **Streamlined Entry Point**: Reduced `app.py` to a clean, 60-line routing file to improve maintainability.
- **Data Schema Optimization**:
    - Transitioned `METRIC_CHOICES` from a list to a dictionary to map metrics to their respective units.
    - Standardized `CATEGORY_COMPANIES` keys to uppercase to ensure strict alignment with the source dataset.
- **UI/UX Refinement**:
    - Migrated all styles to an external CSS file utilizing 17 custom design tokens (CSS properties).
    - Updated typography to DM Sans and implemented a modern, flat-card aesthetic.

### Fixed
- **CSS Optimization**: Resolved duplicate `.kpi-label` and `.section-label` rules and cleaned up unused classes.
- Wildcard `*` transition scoped to interactive elements only.
- **Page 2 (Company Health) Logic**: Replaced all Milestone 2 placeholders with fully functional, reactive data outputs.

### Reflection
The primary focus of this milestone was technical debt reduction and extensibility. By refactoring the codebase into a modular architecture, the project has moved away from a monolithic script toward a professional software engineering pattern. This separation of concerns - where charts, data processing, and UI components live in independent modules - makes the dashboard significantly easier to debug and scale. Additionally, the integration of natural language filtering via the `fin-chat` page represents a shift toward more accessible, user-centric finance tools.

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
