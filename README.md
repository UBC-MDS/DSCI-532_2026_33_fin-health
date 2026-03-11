# fin-health

| | |
| --- | --- |
| CI/CD | [![CI](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/actions/workflows/ci.yml/badge.svg)](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/actions/workflows/ci.yml) [![Build/Deploy Docs](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/actions/workflows/docs-publish.yml/badge.svg)](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/actions/workflows/docs-publish.yml) <!--[![codecov](https://codecov.io/github/UBC-MDS/DSCI-532_2026_33_fin-health/graph/badge.svg?token=X0sTndIrUu)](https://codecov.io/github/UBC-MDS/DSCI-532_2026_33_fin-health)--> |
| Project | [![GitHub Release](https://img.shields.io/github/v/release/UBC-MDS/DSCI-532_2026_33_fin-health?color=green)](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/releases) [![Python Version](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/downloads/release/python-3120/) [![Repo Status](https://img.shields.io/badge/repo%20status-Active-brightgreen)](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health) |
| Meta | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) |

## Project Synopsis

`fin-health` is an interactive dashboard that visualizes the financial health of publicly traded companies. It allows users to explore key financial metrics such as revenue, profitability, debt ratios, and cash flow across companies and time periods. fin-health supports investors and analysts in making data-driven comparisons and evaluating corporate financial performance across sectors and time.

## Motivation
Investment analysts and portfolio managers often need to compare financial performance across sectors and individual companies to support data-driven investment decisions. However, extracting insights from financial statements typically requires manually compiling data and creating ad-hoc visualizations, a process that can be both time-consuming and prone to errors.

`fin-health` addresses this challenge by providing a centralized, interactive dashboard that enables users to explore financial performance efficiently. By allowing users to filter data by time period, sector, and financial metrics, the dashboard facilitates rapid analysis of profitability trends, peer benchmarking, and key financial indicators.

## Features and User Interface
- **Sector Analysis (Strategic Overview)**
    - **Peer Benchmarking**: Visualize sector profitability and revenue growth using reactive Altair scatter plots and bar charts.
    - **Trend Indicators**: Real-time KPI cards showing margin trends with visual directional cues (▲/▼).

- **Company Health (Operational Deep-Dive)**
    - **Reactive Financial Ratios**: Instant calculation of Liquidity (Current Ratio), Solvency (Debt/Equity), and Profitability (ROE) metrics.
    - **Automated Status Auditing**: Visual health icons (Healthy/Warning/Danger) based on industry-standard financial thresholds.

- **Fin-Chat: Natural Language Querying**
    - **Conversational Filtering**: Instead of manual sliders, use the fin-chat interface to ask questions like "Which companies in the Tech sector had a net profit margin above 15%?".
    - **LLM-Powered Insights**: Integrated querychat logic translates natural language into precise data filters, lowering the barrier for non-technical users.

## Demo

Below is a short preview of the dashboard interface.
![Dashboard demo](img/demo.gif)

## Deployment

| Build | URL |
|-------|-----|
| Stable (`main`) | [https://jiroamato-dsci-532-2026-33-fin-health-stable.share.connect.posit.cloud/](https://jiroamato-dsci-532-2026-33-fin-health-stable.share.connect.posit.cloud/) |
| Preview (`dev`) | [https://jiroamato-dsci-532-2026-33-fin-health-dev.share.connect.posit.cloud/](https://jiroamato-dsci-532-2026-33-fin-health-dev.share.connect.posit.cloud/) |

## Developer Setup

### Dependencies

-   `conda` (version 26.1.0 or higher)
-   `playwright` (for browser testing)
-   Python and packages listed in [`requirements.txt`](requirements.txt)

For a more comprehensive guide on development guidelines for this project, check out our contributing page [here](./CONTRIBUTING.md).

1. Install [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) as a prerequisite.

2. Open terminal and run the following commands.

3. Clone the repository:

```bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health.git
cd DSCI-532_2026_33_fin-health
```

4. Create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate fin-health
```

5. Install `chromium` via `playwright`:

```bash
playwright install chromium
```

6. Run fin-health Shiny dashboard locally:

```bash
shiny run --reload src/app.py
```

## Contributors

- Seungmyun Park
- Shruti Sasi
- Jiro Amato
- Luke Ni

## Contributing

Interested in contributing? Check out the contributing guidelines [here](./CONTRIBUTING.md). Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

- Copyright © 2026 Seungmyun Park, Shruti Sasi, Jiro Amato, Luke Ni

- Free software distributed under the [MIT License](./LICENSE.md).
- Documentation made available under **Creative Commons By 4.0 - Attribution 4.0 International** ([CC-BY-4.0](./LICENSE.md))
