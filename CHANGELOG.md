# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.4.0] - (2026-03-18)

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
- (Items from feedback prioritization will go here — TBD based on M4 Feedback Issue)

### Known Issues
- **fin-chat requires API token**: The fin-chat page requires a `GITHUB_TOKEN` environment variable; without it, a fallback message is displayed.
- **Querychat latency**: LLM-powered queries may take 2-5 seconds depending on API response time.

### Release Highlight: TF-IDF RAG Finance Glossary

We added per-query retrieval-augmented generation (RAG) to the fin-chat page so users
unfamiliar with financial terminology get accurate, domain-grounded answers. A ~560-line
glossary (`data/knowledge_base/finance_glossary.txt`) covering all 20+ metrics in the
dataset—definitions, formulas, healthy ranges, and sector-specific benchmarks—is chunked
by heading and indexed with a TF-IDF vectorizer. On every user question, the top-3 most
relevant chunks are retrieved via cosine similarity and injected into the user message
before it reaches the LLM. For example, asking "Is a current ratio of 0.7 concerning?"
now returns a nuanced, sector-aware answer citing the glossary's thresholds instead of
generic training-data knowledge.

- **Option chosen:** C — RAG-based contextual help
- **PR:** #87
- **Why this option over the others:** Users without finance backgrounds need clear,
  consistent metric explanations when exploring the dashboard; a domain glossary with
  per-query TF-IDF retrieval ensures citation-backed answers without requiring an
  external embedding API or model download.
- **Feature prioritization issue link:** #91

### Collaboration

After M3 feedback highlighted blocking dependencies and slow PR reviews, we adopted
a spec-first, scoped-PR workflow for M4. Specs and CONTRIBUTING.md were updated and
merged before any feature branch was created, giving every team member written context
on intent and scope. Work was split across separate files so all four members could
code in parallel without merge conflicts: Jiro on `data.py` and page filtering, Seungmyun
on `ai_explorer.py` and the knowledge base, Shruti on playwright tests, Luke on
function refactoring and unit tests. Each team member resolved at least one feedback
item, and PRs were kept atomic (one feature or fix per PR, with conventional-commit
messages and documentation updated alongside the code).

- **CONTRIBUTING.md:** #79
- **M3 retrospective:** Blocking PRs (env setup) delayed downstream work; review
  turnaround was too slow; PRs lacked tests. We committed to merging blockers within
  2 days, a 24-hour review SLA, and requiring at least one test per feature PR.
- **M4:** Specs merged before code; environment and data-migration PRs landed first
  to unblock the team; contributions were spread across the milestone rather than
  concentrated at the deadline. Daily async Slack stand-ups tracked progress and
  surfaced blockers early.

### Reflection

The dashboard now handles data loading, domain-aware chat, and testing end-to-end.
Parquet + DuckDB via ibis pushes all filtering to the database layer so only the
rows and columns needed for each view are materialized into pandas which is an 
improvement for scalability. The TF-IDF RAG glossary gives fin-chat accurate,
sector-aware answers grounded in a curated knowledge base rather than relying on the
LLM's general training data. Playwright and pytest suites cover page navigation,
filter behaviour, and refactored pure functions, catching regressions before deploy.
A current limitation is that TF-IDF retrieval relies on exact term overlap; queries
with synonyms or paraphrases may miss relevant chunks. Upgrading to semantic
embeddings would address this but adds an external dependency we chose to avoid.

We prioritised all critical feedback items and deferred only cosmetic suggestions —
full rationale is in #<feedback-issue-number> and the Changed section of the CHANGELOG.

The lecture material on RAG and prompting shaped this milestone most directly. 
It informed the chunk-and-retrieve architecture for the glossary and the decision to inject
context into the user message rather than the system prompt. We would have benefited from
earlier coverage of end-to-end testing with playwright as we mostly adopted a test-driven
development from the start.

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
