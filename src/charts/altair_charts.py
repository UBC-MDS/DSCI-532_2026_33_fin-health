"""Pure Altair chart builder functions — no Shiny imports."""

import altair as alt
import pandas as pd

from components.empty_chart import empty_chart

# Custom warm palette for categorical data
PALETTE = [
    "#2563eb",
    "#c0392b",
    "#f59e0b",
    "#009e73",
    "#8e44ad",
    "#e67e22",
    "#1abc9c",
    "#334155",
]

def _register_theme():
    """Register and enable the fin-health Altair theme."""

    def _theme():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": "transparent"},
                "autosize": {"type": "fit", "contains": "padding"},
                "axis": {
                    "labelFont": "DM Sans, sans-serif",
                    "titleFont": "DM Sans, sans-serif",
                    "labelColor": "#475569",
                    "titleColor": "#0f172a",
                    "gridColor": "#e2e8f0",
                    "domainColor": "#e2e8f0",
                    "labelFontSize": 10,
                    "titleFontSize": 11,
                    "labelLimit": 80,
                    "titlePadding": 4,
                    "labelPadding": 3,
                },
                "axisX": {
                    "labelAngle": -45,
                    "labelAlign": "right",
                    "labelBaseline": "top",
                },
                "title": {
                    "font": "DM Sans, sans-serif",
                    "color": "#0f172a",
                    "fontSize": 12,
                    "fontWeight": 600,
                    "offset": 4,
                },
                "legend": {
                    "labelFont": "DM Sans, sans-serif",
                    "titleFont": "DM Sans, sans-serif",
                    "labelColor": "#475569",
                    "titleColor": "#0f172a",
                    "labelFontSize": 9,
                    "titleFontSize": 10,
                    "symbolSize": 40,
                    "columnPadding": 4,
                    "rowPadding": 1,
                },
                "padding": {"top": 5, "bottom": 5, "left": 5, "right": 5},
            }
        }

    if hasattr(alt, "theme") and hasattr(alt.theme, "register"):
        # Altair >= 5.5
        @alt.theme.register("fin_health", enable=True)
        def _fin_health_theme():
            return alt.theme.ThemeConfig(_theme())
    else:
        alt.themes.register("fin_health", _theme)
        alt.themes.enable("fin_health")


_register_theme()

def build_sector_bar(data: pd.DataFrame, metric: str, unit: str) -> alt.Chart:
    """Bar chart of average metric by sector."""
    if data.empty:
        return empty_chart()
    avg_by_sector = data.groupby("Category")[metric].mean().reset_index()
    if avg_by_sector.empty:
        return empty_chart()
    return (
        alt.Chart(avg_by_sector)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("Category:N", title="Sector", sort="-y"),
            y=alt.Y(f"{metric}:Q", title=f"{metric} {unit}"),
            color=alt.Color(
                "Category:N",
                scale=alt.Scale(range=PALETTE),
                legend=None,
            ),
            tooltip=["Category", alt.Tooltip(f"{metric}:Q", format=".2f")],
        )
        .properties(
            title=f"Average {metric} by Sector", width="container", height="container"
        )
    )


def build_metric_trend(data: pd.DataFrame, metric: str, unit: str) -> alt.Chart:
    """Line chart of metric trend over time by sector."""
    if data.empty:
        return empty_chart()
    observed_trend = data.groupby(["Year", "Category"], as_index=False)[metric].mean()
    if observed_trend.empty:
        return empty_chart()
    return (
        alt.Chart(observed_trend)
        .mark_line(point=True)
        .encode(
            alt.X("Year:O", title="Year"),
            alt.Y(f"{metric}:Q", title=f"{metric} {unit}"),
            color=alt.Color("Category:N", scale=alt.Scale(range=PALETTE)),
            tooltip=["Year", "Category", alt.Tooltip(f"{metric}:Q", format=".2f")],
        )
        .properties(width="container", height="container")
    )


def build_peer_scatter(data: pd.DataFrame, metric: str, unit: str) -> alt.Chart:
    """Scatter plot of Revenue vs selected metric."""
    if data.empty:
        return empty_chart()
    return (
        alt.Chart(data)
        .mark_circle(size=60)
        .encode(
            x=alt.X("Revenue:Q", title="Revenue ($)"),
            y=alt.Y(f"{metric}:Q", title=f"{metric} {unit}"),
            color=alt.Color("Category:N", scale=alt.Scale(range=PALETTE)),
            tooltip=[
                "Company",
                "Category",
                "Year:O",
                alt.Tooltip("Revenue:Q", format=",.0f"),
                alt.Tooltip(f"{metric}:Q", format=",.2f"),
            ],
        )
        .properties(title=f"Revenue vs {metric}", width="container", height="container")
    )