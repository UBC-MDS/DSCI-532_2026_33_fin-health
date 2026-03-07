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