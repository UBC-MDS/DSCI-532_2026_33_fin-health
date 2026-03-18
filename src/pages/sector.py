"""Page 1: Sector Analysis — UI layout and server logic."""

import pandas as pd
from shiny import reactive, render, ui
from shinywidgets import output_widget, render_altair
from data import ALL_SECTORS, METRIC_CHOICES, YEAR_MIN, YEAR_MAX, tbl
from components.kpi_card import kpi_card
from charts.altair_charts import (
    build_metric_trend,
    build_peer_scatter,
    build_sector_bar,
)


_METRIC_DEFINITIONS = {
    "Avg Profit Margin": (
        "Average net profit margin across all filtered companies. Shows what"
        " percentage of revenue is retained as profit. A declining margin may"
        " signal rising costs or pricing pressure."
    ),
    "Top Sector": (
        "The sector with the highest average net profit margin for the selected"
        " period. Identifies which industry is most efficient at converting"
        " revenue into profit, useful for spotting sector-level opportunities."
    ),
    "Index Margin": (
        "Revenue-weighted profit margin across all filtered companies"
        " (Total Net Income \u00f7 Total Revenue). Unlike the simple average,"
        " larger companies carry more weight \u2014 reflecting the true economic"
        " margin of the market."
    ),
    "Revenue Growth": (
        "Year-over-year change in total aggregate revenue across all filtered"
        " companies. Positive growth indicates expanding market activity;"
        " negative growth may signal economic contraction or sector headwinds."
    ),
    "Peer Benchmarking": (
        "Scatter plot comparing each company\u2019s selected metric against revenue."
        " Revenue is used as a size baseline, making it easy to spot outliers"
        " \u2014 companies that outperform or underperform relative to their scale."
    ),
    "Company Details": (
        "Detailed financial data for all companies matching the current filters."
        " Drill down into individual metrics to compare performance across"
        " sectors and years."
    ),
    "Sector Comparison": (
        "Bar chart ranking sectors by the selected metric. Quickly compare"
        " which industries lead or lag, and how far apart they are."
    ),
    "Historical Trend": (
        "Line chart showing how the selected metric evolves over the chosen"
        " time period. Reveals long-term patterns, cyclical behavior, and"
        " inflection points across sectors."
    ),
}


def _card_header_with_tooltip(header: str):
    """Card header with an info icon that shows a metric definition on hover."""
    definition = _METRIC_DEFINITIONS.get(header, "")
    if not definition:
        return ui.card_header(header)
    return ui.card_header(
        ui.tags.span(
            header,
            ui.tags.span(
                " \u24d8",
                title=definition,
                style="cursor: help; opacity: 0.5; font-size: 0.85em;",
            ),
        )
    )


def sector_ui():
    """Return the full Page 1 layout (sidebar + KPI row + chart row + peer row)."""
    # Sidebar inputs
    year_slider = ui.input_slider(
        id="p1_year_range",
        label="Period",
        min=YEAR_MIN,
        max=YEAR_MAX,
        value=[YEAR_MIN, YEAR_MAX],
        sep="",
    )
    sector_select = ui.input_selectize(
        id="p1_sector",
        label="Sector",
        choices=ALL_SECTORS,
        selected=[],
        multiple=True,
        options={"placeholder": "All sectors (select to filter)"},
    )
    metric_select = ui.input_selectize(
        id="p1_metric",
        label="Metric",
        choices=list(METRIC_CHOICES.keys()),
        selected="Net Profit Margin",
    )
    reset = ui.input_action_button("p1_reset", "Reset Filters")
    sidebar = ui.sidebar(
        ui.h4("Analytics Filters"),
        year_slider,
        sector_select,
        metric_select,
        reset,
        ui.hr(),
        ui.tags.small(
            "Hover over the ",
            ui.tags.span("\u24d8", style="opacity:0.7;"),
            " icon on any card for an explanation.",
            style="color: var(--text-secondary, #6b7280); line-height: 1.4;",
        ),
        open="desktop",
    )

    # KPI cards — using the reusable kpi_card() factory
    card_avg_margin = kpi_card(
        header="Avg Profit Margin",
        value_id="p1_avg_margin",
        trend_id="p1_margin_trend",
        label_id="p1_margin_badge",
        tooltip=_METRIC_DEFINITIONS["Avg Profit Margin"],
    )
    card_top_sector = kpi_card(
        header="Top Sector",
        value_id="p1_top_sector",
        label_id="p1_top_sector_label",
        tooltip=_METRIC_DEFINITIONS["Top Sector"],
    )
    card_index_margin = kpi_card(
        header="Index Margin",
        value_id="p1_index_margin_value",
        trend_id="p1_index_margin_trend",
        label_id="p1_index_margin_label",
        tooltip=_METRIC_DEFINITIONS["Index Margin"],
    )
    card_revenue_growth = kpi_card(
        header="Revenue Growth",
        value_id="p1_revenue_growth_value",
        trend_id="p1_revenue_trend",
        label_id="p1_revenue_growth_label",
        tooltip=_METRIC_DEFINITIONS["Revenue Growth"],
    )
    kpi_row = ui.div(
        ui.layout_columns(
            card_avg_margin,
            card_top_sector,
            card_index_margin,
            card_revenue_growth,
            col_widths=[3, 3, 3, 3],
        ),
        class_="kpi-card-row",
    )

    # Chart cards
    card_sector_profitability = ui.card(
        _card_header_with_tooltip("Sector Comparison"),
        output_widget("p1_chart_a"),
        full_screen=True,
    )
    card_trend = ui.card(
        _card_header_with_tooltip("Historical Trend"),
        output_widget("p1_chart_b"),
        full_screen=True,
    )
    chart_row = ui.layout_columns(
        card_sector_profitability,
        card_trend,
        col_widths=[6, 6],
    )

    # Peer + Table cards
    card_peer = ui.card(
        _card_header_with_tooltip("Peer Benchmarking"),
        output_widget("p1_chart_c"),
        full_screen=True,
    )
    card_details = ui.card(
        _card_header_with_tooltip("Company Details"),
        ui.output_data_frame("p1_table_d"),
    )
    peer_row = ui.layout_columns(
        card_peer,
        card_details,
        col_widths=[6, 6],
    )

    return ui.layout_sidebar(
        sidebar,
        ui.page_fillable(
            ui.h2("US Corporate Profitability Analytics"),
            kpi_row,
            chart_row,
            peer_row,
        ),
    )


def sector_server(input, output, session):
    """All Page 1 reactive calcs and renderers."""

    @reactive.calc
    def p1_selected_metric():
        """Return the selected metric, falling back to default if cleared."""
        metric = input.p1_metric()
        if not metric or metric not in METRIC_CHOICES:
            return "Net Profit Margin"
        return metric

    @reactive.effect
    @reactive.event(input.p1_reset)
    def _():
        # Update the year range slider to full range
        ui.update_slider("p1_year_range", value=[YEAR_MIN, YEAR_MAX])
        # Update the sector select to "All"
        ui.update_selectize("p1_sector", selected=[])
        # Update the metric select to default
        ui.update_select("p1_metric", selected="Net Profit Margin")

    @reactive.calc
    def p1_filtered_data():
        """Filter dataset via ibis expressions, then materialize to pandas."""
        year_min, year_max = input.p1_year_range()
        sector = input.p1_sector()
        expr = tbl.filter(tbl["Year"] >= year_min, tbl["Year"] <= year_max)
        if sector:
            expr = expr.filter(tbl["Category"].isin(sector))
        return expr.to_pandas()

    # KPI outputs
    # ---------------Avg Profit Margin---------------
    @render.text
    def p1_avg_margin():
        """Calculate Average profit margin from filtered data.
        Return 'Data Unavailable' for empty dataset"""
        filtered = p1_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        avg = filtered["Net Profit Margin"].mean()
        return f"{avg:.1f}%"

    @render.ui
    def p1_margin_trend():
        """Render trend indicator for profit margin based on actual data."""
        filtered_df = p1_filtered_data()
        if filtered_df.empty:
            return ui.tags.span()
        # Get years sorted
        years = sorted(filtered_df["Year"].unique())
        if len(years) < 2:
            return ui.tags.span()  # No trend to show with single year
        # Compare most recent year to previous year
        current_year_margin = filtered_df[filtered_df["Year"] == years[-1]][
            "Net Profit Margin"
        ].mean()
        previous_year_margin = filtered_df[filtered_df["Year"] == years[-2]][
            "Net Profit Margin"
        ].mean()
        if pd.isna(current_year_margin) or pd.isna(previous_year_margin):
            return ui.tags.span()
        is_positive = current_year_margin >= previous_year_margin
        trend_char = "\u25b2" if is_positive else "\u25bc"
        trend_class = "up" if is_positive else "down"
        return ui.tags.span(trend_char, class_=f"trend-indicator {trend_class}")

    @render.ui
    def p1_margin_badge():
        """Render a badge to identify the number of companies being compared"""
        filtered = p1_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        n = filtered["Company"].nunique()
        return ui.tags.p(
            f"BASED ON {n} COMPANIES",
            class_="kpi-label",
            style="margin-top: 0.5rem;",
        )

    # ---------------Top Sector---------------
    @render.text
    def p1_top_sector():
        """Calculate Top sector based on Max Average profit margin from filtered data.
        Return 'Data Unavailable' for empty dataset"""
        filtered = p1_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        top = filtered.groupby("Category")["Net Profit Margin"].mean().idxmax()
        return top

    @render.ui
    def p1_top_sector_label():
        """Show the top sector's avg net profit margin as sublabel."""
        filtered = p1_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        sector_margins = filtered.groupby("Category")["Net Profit Margin"].mean()
        top_margin = sector_margins.max()
        return ui.tags.p(
            f"AVG NET PROFIT MARGIN FOR THE PERIOD: {top_margin:.1f}%",
            class_="kpi-label",
            style="margin-top: 0.5rem;",
        )

    @reactive.calc
    def p1_index_margin():
        """Calculate Index Performance for 'p1_index_margin_value'"""
        filtered_df = p1_filtered_data()
        if filtered_df.empty:
            return 0.0
        # Aggregated Index Formula: Total Income / Total Revenue
        total_revenue = filtered_df["Revenue"].sum()
        total_net_income = filtered_df["Net Income"].sum()
        if total_revenue == 0:
            return 0.0
        return (total_net_income / total_revenue) * 100

    @render.text
    def p1_index_margin_value():
        """Display the overall weighted profit margin."""
        filtered = p1_filtered_data()
        if filtered.empty:
            return "Data Unavailable"
        margin = p1_index_margin()
        return f"{margin:.1f}%"

    @render.ui
    def p1_index_margin_label():
        """Show 'OVERALL WEIGHTED MARGIN' sublabel with company count."""
        filtered = p1_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        n = filtered["Company"].nunique()
        return ui.tags.p(
            f"OVERALL WEIGHTED MARGIN \u00b7 {n} COMPANIES",
            class_="kpi-label",
            style="margin-top: 0.5rem;",
        )

    @render.ui
    def p1_index_margin_trend():
        """Render trend indicator for index margin based on YoY change."""
        filtered_df = p1_filtered_data()
        if filtered_df.empty:
            return ui.tags.span()
        years = sorted(filtered_df["Year"].unique())
        if len(years) < 2:
            return ui.tags.span()
        curr = filtered_df[filtered_df["Year"] == years[-1]]
        prev = filtered_df[filtered_df["Year"] == years[-2]]
        curr_rev = curr["Revenue"].sum()
        prev_rev = prev["Revenue"].sum()
        if curr_rev == 0 or prev_rev == 0:
            return ui.tags.span()
        curr_margin = curr["Net Income"].sum() / curr_rev * 100
        prev_margin = prev["Net Income"].sum() / prev_rev * 100
        is_positive = curr_margin >= prev_margin
        trend_char = "\u25b2" if is_positive else "\u25bc"
        trend_class = "up" if is_positive else "down"
        return ui.tags.span(trend_char, class_=f"trend-indicator {trend_class}")

    # ---------------Revenue Growth---------------
    @reactive.calc
    def p1_revenue_change():
        """Calculate revenue change value and direction (shared by display and trend)."""
        filtered_df = p1_filtered_data()
        yearly_revenue = (
            filtered_df.groupby("Year")["Revenue"].sum().sort_index(ascending=False)
        )
        if len(yearly_revenue) < 2:
            return None
        current = yearly_revenue.iloc[0]
        previous = yearly_revenue.iloc[1]
        if pd.isna(current) or pd.isna(previous) or previous == 0:
            return None
        revenue_growth = (current - previous) / previous * 100
        return {"value": revenue_growth, "is_positive": revenue_growth >= 0}

    @render.text
    def p1_revenue_growth_value():
        change = p1_revenue_change()
        if change is None:
            return "Data Unavailable"
        sign = "+" if change["is_positive"] else ""
        return f"{sign}{change['value']:.1f}%"

    @render.ui
    def p1_revenue_growth_label():
        filtered = p1_filtered_data()
        if filtered.empty:
            return ui.tags.span()
        n = filtered["Company"].nunique()
        return ui.tags.p(
            f"AGGREGATE YOY \u00b7 {n} COMPANIES",
            class_="kpi-label",
            style="margin-top: 0.5rem;",
        )

    @render.ui
    def p1_revenue_trend():
        """Render trend indicator for revenue growth based on actual data."""
        change = p1_revenue_change()
        if change is None:
            return ui.tags.span()
        trend_char = "\u25b2" if change["is_positive"] else "\u25bc"
        trend_class = "up" if change["is_positive"] else "down"
        return ui.tags.span(trend_char, class_=f"trend-indicator {trend_class}")

    # ---------------Chart outputs---------------

    # Sector Profitability
    @render_altair
    def p1_chart_a():
        """Render Chart A - Sector Profitability"""
        filtered = p1_filtered_data()
        metric = p1_selected_metric()
        unit = METRIC_CHOICES[metric]
        return build_sector_bar(filtered, metric, unit)

    @render.ui
    def p1_trend_header():
        min_year, max_year = input.p1_year_range()
        return f"Trend - {p1_selected_metric()}  ({min_year}-{max_year})"

    # Metric Based Trend
    @render_altair
    def p1_chart_b():
        """Render Chart B - Metric based Trend"""
        filtered = p1_filtered_data()
        metric = p1_selected_metric()
        unit = METRIC_CHOICES[metric]
        return build_metric_trend(filtered, metric, unit)

    # Peer Benchmarking Scatterplot
    @render_altair
    def p1_chart_c():
        """Render Chart C - Peer Benchmarking Scatterplot"""
        filtered = p1_filtered_data()
        metric = p1_selected_metric()
        unit = METRIC_CHOICES[metric]
        return build_peer_scatter(filtered, metric, unit)

    # Company Details
    @render.data_frame
    def p1_table_d():
        """Render Table D - Company Details"""
        filtered = p1_filtered_data()
        cols = [
            "Company",
            "Category",
            "Year",
            "Revenue",
            "Net Income",
            "Net Profit Margin",
        ]
        return filtered[cols]
