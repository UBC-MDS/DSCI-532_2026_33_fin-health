# M4 App Specification

## Overview

Milestone 4 finalizes the fin-health dashboard into a production-ready product with three objectives:

1. **Parquet + DuckDB** — replace CSV-based data loading with lazy parquet queries via ibis + DuckDB so all filtering happens at the database level.
2. **RAG Finance Glossary** — add a domain-specific knowledge base of financial term definitions to querychat so users can understand the metrics in the dataset.
3. **Testing** — add 3 playwright end-to-end behavior tests and at least 1 pytest unit test for a refactored function.

Additional work: address instructor/TA/peer feedback, update CONTRIBUTING.md with M3 retrospective, and publish release v0.4.0.

---

## Changes from M3

| Area | M3 (current) | M4 (planned) |
|------|-------------|--------------|
| Data loading | `pd.read_csv()` in `data.py` → full DataFrame in memory | `ibis.duckdb.connect()` + `con.read_parquet()` → lazy expressions, `.execute()` at render time |
| Data format | `data/raw/financial_statement.csv` | `data/processed/financial_statement.parquet` (CSV kept for reference) |
| Filtering | pandas boolean indexing in `@reactive.calc` | ibis filter expressions in `@reactive.calc`, `.execute()` only at render |
| AI feature | querychat with ChatGithub, no domain knowledge | querychat + RAG finance glossary knowledge base |
| Testing | pytest unit tests only (`tests/test_data.py`, `tests/test_charts.py`) | Add 3 playwright behavior tests + keep existing pytest unit tests |
| Dependencies | `chatlas`, `querychat`, `shiny`, `altair`, etc. | Add `ibis-framework[duckdb]` |

---

## 1. File Structure (Updated)

```
src/
├── app.py                  # Entry point: wires navbar, pages, footer, CSS
├── data.py                 # Data loading via ibis + DuckDB (CHANGED)
├── components/
│   ├── __init__.py
│   ├── kpi_card.py         # Reusable KPI card factory
│   └── empty_chart.py      # Reusable "Data Unavailable" chart helper
├── pages/
│   ├── __init__.py
│   ├── sector.py           # Page 1 UI + server (updated for ibis)
│   ├── company.py          # Page 2 UI + server (updated for ibis)
│   └── ai_explorer.py      # Page 3 UI + server (updated with RAG)
└── charts/
    ├── __init__.py
    └── altair_charts.py    # Pure chart builder functions (unchanged)
data/
├── raw/
│   └── financial_statement.csv     # Original CSV (kept for reference)
├── processed/
│   └── financial_statement.parquet # Parquet file (NEW)
└── knowledge_base/
    └── finance_glossary.txt        # RAG glossary (NEW)
tests/
├── test_data.py                    # Unit tests for data loading
├── test_charts.py                  # Unit tests for chart builders
└── test_app_playwright.py          # Playwright behavior tests (NEW)
```

---

## 2. Parquet + DuckDB Migration

### 2.1 Data Conversion

A one-time script converts the CSV to parquet:

```python
import duckdb
from pathlib import Path

CSV = Path("data/raw/financial_statement.csv")
OUT = Path("data/processed/financial_statement.parquet")
OUT.parent.mkdir(exist_ok=True)

duckdb.execute(f"""
    COPY (SELECT * FROM read_csv_auto('{CSV}'))
    TO '{OUT}' (FORMAT PARQUET)
""")
```

### 2.2 Updated `data.py`

Replace `pd.read_csv()` with ibis + DuckDB lazy loading:

```python
from pathlib import Path
import ibis
from ibis import _

PARQUET_PATH = Path(__file__).parent.parent / "data" / "processed" / "financial_statement.parquet"

con = ibis.duckdb.connect()
financial_data = con.read_parquet(str(PARQUET_PATH))

# Constants derived at startup (small queries, executed once)
CATEGORY_COMPANIES = {
    "BANK": ["AIG", "BCS"],
    "ELEC": ["INTC", "NVDA"],
    "FINANCE": ["SHLDQ"],
    "FINTECH": ["PYPL"],
    "FOOD": ["MCD"],
    "IT": ["AAPL", "GOOG", "MSFT"],
    "LOGI": ["AMZN"],
    "MANUFACTURING": ["PCG"],
}
ALL_SECTORS = sorted(CATEGORY_COMPANIES.keys())

METRIC_CHOICES = {
    "Net Profit Margin": "%",
    "ROE": "%",
    "ROA": "%",
    "ROI": "%",
    "Revenue": "USD",
    "Net Income": "USD",
    "EBITDA": "USD",
    "Current Ratio": "",
    "Debt/Equity Ratio": "",
}
```

### 2.3 Updated Reactive Calcs

All page `@reactive.calc` functions switch from pandas boolean indexing to ibis filter expressions. `.execute()` is called only at render time.

**Page 1 example — `p1_filtered_data`:**

```python
@reactive.calc
def p1_filtered_data():
    expr = financial_data
    min_yr, max_yr = input.p1_year_range()
    expr = expr.filter(_.Year >= min_yr, _.Year <= max_yr)
    if input.p1_sector() != "All":
        expr = expr.filter(_.Category == input.p1_sector())
    return expr
```

Renderers call `.execute()` to materialize the DataFrame only when needed:

```python
@render.text
def p1_avg_margin():
    data = p1_filtered_data().execute()
    # ... compute and return
```

**Page 2 example — `p2_filtered_data`:**

```python
@reactive.calc
def p2_filtered_data():
    expr = financial_data
    expr = expr.filter(_.Category == input.category())
    expr = expr.filter(_.Company == input.company())
    expr = expr.filter(_.Year == int(input.year()))
    return expr
```

### 2.4 Impact on Charts

Chart builder functions in `charts/altair_charts.py` remain unchanged — they accept pandas DataFrames. The `.execute()` call at render time produces the DataFrame that gets passed to chart builders.

### 2.5 Impact on querychat

`querychat.QueryChat()` currently receives `df` (a pandas DataFrame). After the migration, we will pass the executed full DataFrame for querychat's internal SQL engine. querychat manages its own DuckDB connection internally, so we provide it with a DataFrame as before.

---

## 3. Advanced Feature — Option C: RAG Finance Glossary

### 3.1 Purpose

Users viewing the fin-health dashboard encounter financial metrics (ROE, EBITDA, Current Ratio, etc.) that may be unfamiliar. The RAG knowledge base provides a glossary of financial term definitions so that when users ask querychat questions like "What does ROE mean?" or "Explain current ratio", the LLM retrieves and cites the glossary entry.

### 3.2 Knowledge Base

A plain-text glossary file at `data/knowledge_base/finance_glossary.txt` (~570 lines) containing:

**Metric definitions** (with formulas, healthy ranges, dataset ranges, and per-sector industry benchmarks):
- Net Profit Margin, ROE, ROA, ROI
- Revenue, Net Income, EBITDA, Gross Profit, EPS
- Current Ratio, Debt/Equity Ratio, Shareholder Equity
- Cash Flow from Operating, Investing, Financing; Free Cash Flow per Share
- Market Cap, Return on Tangible Equity, Number of Employees, Inflation Rate

**Contextual sections:**
- Sector Definitions (8 sectors mapped to 12 tickers)
- How to Interpret Financial Health (7-point checklist with sector-aware caveats)
- Cross-Metric Relationships (e.g., high ROE + high D/E = leverage-driven returns)
- Company Context & Notable Outliers (SHLDQ bankruptcy, AAPL buyback strategy, etc.)
- Macroeconomic Events in the Dataset (2009 GFC recovery, 2020 COVID, 2022 inflation)

Each metric entry includes industry-specific context explaining *why* different sectors have different norms (e.g., SaaS companies run lower current ratios because of predictable receivables; banks carry high D/E because leverage IS their business model).

### 3.3 Integration with querychat — TF-IDF per-query retrieval

Rather than injecting the full glossary into the system prompt (context-stuffing), we use **TF-IDF retrieval** to inject only the most relevant chunks per query:

```
User question → TF-IDF cosine similarity → top-3 chunks → prepend to user message → LLM
```

**Architecture in `src/pages/ai_explorer.py`:**

1. **`_ensure_kb()`** — Lazily loads the glossary file and splits it into chunks by `###` headings (one chunk per metric) plus `##` sections (sector definitions, health interpretation, cross-metric relationships, company context, macro events). Builds a TF-IDF vocabulary index over all chunks.

2. **`_retrieve(query, top_k=3)`** — Transforms the user's question into a TF-IDF vector, computes cosine similarity against all chunks, and returns the top-k most relevant chunks.

3. **`_RAGChat(Chat)`** — A subclass of `chatlas.Chat` that overrides `stream_async`. For each user message, it retrieves relevant chunks and prepends them as "Relevant domain context:" before delegating to `super().stream_async()`. Since `ChatGithub` is a factory function (not a class), we subclass `Chat` directly and swap `__class__` on the factory-created instance. This survives querychat's internal `deepcopy` because deepcopy preserves `__class__`, unlike instance-level monkey-patches which would be lost.

4. **Rule 7 in `EXTRA_INSTRUCTIONS`** directs the LLM to use the domain context provided alongside each question, cite industry benchmarks, and compare values against sector averages.

**Why TF-IDF over embeddings:** The glossary uses exact financial terms (e.g., "current ratio", "debt equity") that match user queries well on term overlap alone. TF-IDF requires no API key, no model download, and adds minimal latency. For a structured domain glossary, this is sufficient; semantic embeddings would be warranted for free-form natural language with synonyms and paraphrases.

**Dependencies:** `scikit-learn` (TfidfVectorizer, cosine_similarity), `numpy` — both already in `requirements.txt`.

### 3.4 Documentation Requirements

- **GitHub Issue:** Document option choice (Option C) and motivation for choosing a finance glossary with per-query retrieval
- **Specification:** This section (reflected before code is written)
- **Demonstration:** At least one query where RAG context visibly improves the response compared to without it (see `notebooks/rag.ipynb` for side-by-side comparisons)

---

## 4. Testing

### 4.1 Playwright Behavior Tests (`tests/test_app_playwright.py`)

3 end-to-end tests using `shiny.playwright.controller`:

| Test | Behavior Verified |
|------|-------------------|
| `test_initial_page_loads` | Dashboard loads and Page 1 KPI value boxes display expected initial values |
| `test_sector_filter_updates_charts` | Selecting a specific sector in the dropdown updates the KPI values and chart outputs |
| `test_company_page_selection` | Navigating to Page 2 and selecting a company/year renders the correct KPI values |

Each test includes a one-sentence docstring describing what behavior is verified and why it matters.

### 4.2 Pytest Unit Tests (`tests/test_health_status.py`)

Refactored health-status classification logic from `company.py` into two pure functions in `src/components/health_status.py`:

- **`classify_health(value, healthy, warning, higher_is_better)`** — returns `"healthy"`, `"warning"`, or `"danger"` based on threshold comparison. Replaces 4 repeated if/elif/else blocks in `company.py`.
- **`format_currency(value)`** — formats dollar values as `"$1,234M"` or `"-$567M"`. Replaces inline `fmt()` closure in `p2_cash_flows`.

24 unit tests across 3 test classes:

| Class | Tests | Coverage |
|-------|-------|----------|
| `TestClassifyHealthHigherIsBetter` | 12 | Boundary values for NPM (healthy=10, warning=0), ROE (healthy=15, warning=0), Current Ratio (healthy=1.5, warning=1.0) |
| `TestClassifyHealthLowerIsBetter` | 7 | Boundary values for Debt/Equity (healthy=1.0, warning=2.0, `higher_is_better=False`) |
| `TestFormatCurrency` | 5 | Positive, negative, zero, large, and small-negative values |

---

## 5. Existing Spec (Unchanged from M3)

The following sections from M3 remain unchanged unless noted above.

### 5.1 Page 1 — Sector Analysis

18 components: 3 inputs, 3 reactive calcs, 12 outputs. Layout, component inventory, and reactivity diagram unchanged from M3 spec §2.5. Only change: `p1_filtered_data` switches from pandas to ibis expressions (see §2.3 above).

### 5.2 Page 2 — Company Health

3 inputs, 1 reactive calc, 7 KPI outputs, 4 chart outputs, 1 reactive effect. Layout, component inventory, and reactivity diagram unchanged from M3 spec §4. Only change: `p2_filtered_data` switches from pandas to ibis expressions (see §2.3 above).

### 5.3 Page 3 — fin-chat

9 components: 1 querychat instance, 4 outputs, 1 download handler. Layout and component inventory unchanged from M3 spec §3. Changes: querychat gains RAG glossary context (see §3 above).

### 5.4 Charts

All chart builder functions in `charts/altair_charts.py` unchanged. They continue to accept pandas DataFrames — the ibis `.execute()` call produces the DataFrame before passing to chart builders.

### 5.5 Components

`kpi_card.py` and `empty_chart.py` unchanged from M3.

---

## 6. Updated Dependencies

| Package | Purpose | Add to |
|---------|---------|--------|
| `ibis-framework[duckdb]` | Lazy parquet loading + DuckDB query engine | `requirements.txt`, `environment.yml` |

All other dependencies remain the same as M3.

---

## 7. Migration Checklist

- [ ] Update specification documents (this file) before writing code
- [ ] Update `CONTRIBUTING.md` with M3 retrospective and M4 norms (via PR)
- [ ] Convert CSV to parquet in `data/processed/`
- [ ] Update `data.py` to use ibis + DuckDB
- [ ] Update Page 1 reactive calcs for ibis expressions
- [ ] Update Page 2 reactive calcs for ibis expressions
- [ ] Update querychat data passing in `ai_explorer.py`
- [ ] Add `ibis-framework[duckdb]` to `requirements.txt` and `environment.yml`
- [ ] Create finance glossary knowledge base
- [ ] Integrate RAG with querychat
- [ ] Create GitHub Issue for Option C choice and motivation
- [ ] Write 3 playwright behavior tests
- [ ] Write at least 1 pytest unit test for a refactored function
- [ ] Document test command in README
- [ ] Create `M4 Feedback Prioritization` GitHub Issue
- [ ] Address all critical feedback items
- [ ] Update `CHANGELOG.md` with `[0.4.0]` entry
- [ ] Deploy to Posit Connect Cloud and verify
- [ ] Create GitHub Release `v0.4.0`
- [ ] Submit PDF to Gradescope
