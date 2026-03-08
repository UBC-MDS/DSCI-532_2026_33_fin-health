"""Page 1: Sector Analysis — UI layout and server logic."""

import pandas as pd
from shiny import reactive, render, ui
from shinywidgets import output_widget, render_altair
from data import ALL_SECTORS, METRIC_CHOICES, df
from components.kpi_card import kpi_card
from charts.altair_charts import (
    build_metric_trend,
    build_peer_scatter,
    build_sector_bar,
)


def sector_ui():
    """Return the full Page 1 layout (sidebar + KPI row + chart row + peer row)."""
    # Sidebar inputs
    year_slider = ui.input_slider(
        id="p1_year_range",
        label="Period",
        min=int(df["Year"].min()),
        max=int(df["Year"].max()),
        value=[int(df["Year"].min()), int(df["Year"].max())],
        sep="",
    )
    sector_select = ui.input_selectize(
        id="p1_sector",
        label="Sector",
        choices=["All"] + ALL_SECTORS,
        selected="All",
        multiple=True,
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
        open="desktop",
    )

    # KPI cards — using the reusable kpi_card() factory
    card_avg_margin = kpi_card(
        header="Avg Profit Margin",
        value_id="p1_avg_margin",
        trend_id="p1_margin_trend",
        label_id="p1_margin_badge",
    )
    card_top_sector = kpi_card(
        header="Top Sector",
        value_id="p1_top_sector",
        label_id="p1_index_performance_display",
    )
    card_revenue_growth = kpi_card(
        header="Revenue Growth",
        value_id="p1_revenue_growth_value",
        trend_id="p1_revenue_trend",
        label_id="p1_revenue_growth_label",
    )
    kpi_row = ui.div(
        ui.layout_columns(
            card_avg_margin,
            card_top_sector,
            card_revenue_growth,
            col_widths=[4, 4, 4],
        ),
        class_="kpi-card-row",
    )

    # Chart cards
    card_sector_profitability = ui.card(
        ui.card_header("Sector Comparison"),
        output_widget("p1_chart_a"),
        full_screen=True,
    )
    card_trend = ui.card(
        ui.card_header("Historical Trend"),
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
        ui.card_header("Peer Benchmarking"),
        output_widget("p1_chart_c"),
        full_screen=True,
    )
    card_details = ui.card(
        ui.card_header("Company Details"),
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
        ui.update_slider(
            "p1_year_range", value=[int(df["Year"].min()), int(df["Year"].max())]
        )
        # Update the sector select to "All"
        ui.update_selectize("p1_sector", selected="All")
        # Update the metric select to default
        ui.update_select("p1_metric", selected="Net Profit Margin")

    @reactive.calc
    def p1_filtered_data():
        """Filter dataset by selected year range and sector."""
        year_min, year_max = input.p1_year_range()
        sector = input.p1_sector()
        filtered = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]
        if sector and "All" not in sector:
            filtered = filtered[filtered["Category"].isin(sector)]
        return filtered

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

    @reactive.calc
    def p1_index_margin():
        """Calculate Index Performance for 'p1_index_performance_display'"""
        filtered_df = p1_filtered_data()
        if filtered_df.empty:
            return 0.0
        # Aggregated Index Formula: Total Income / Total Revenue
        total_revenue = filtered_df["Revenue"].sum()
        total_net_income = filtered_df["Net Income"].sum()
        if total_revenue == 0:
            return 0.0
        return (total_net_income / total_revenue) * 100

    @render.ui
    def p1_index_performance_display():
        """Render Index Performance of the Top sector"""
        margin = p1_index_margin()
        return ui.tags.p(
            "INDEX PERFORMANCE: ",
            ui.tags.strong(f"{margin:.1f}%"),
            " NET PROFIT MARGIN",
            class_="kpi-label",
        )

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
        return ui.tags.p(
            "YEAR OVER YEAR",
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
