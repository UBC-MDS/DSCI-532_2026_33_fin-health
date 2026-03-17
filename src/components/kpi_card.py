"""Reusable KPI card factory for consistent card layouts."""

from shiny import ui


def kpi_card(
    header: str,
    value_id: str,
    trend_id: str = None,
    label_id: str = None,
    status_id: str = None,
    tooltip: str = None,
):
    """Build a KPI card with consistent structure.

    Parameters
    ----------
    header : str
        Card header text.
    value_id : str
        Output ID for the main KPI value (used with @render.text).
    trend_id : str, optional
        Output ID for the trend indicator (used with @render.ui).
    label_id : str, optional
        Output ID for the label row below the value (used with @render.ui).
    status_id : str, optional
        Output ID for a health status icon (used with @render.ui).
    tooltip : str, optional
        Hover text for an info icon beside the header.
    """
    value_children = [
        ui.tags.h3(
            ui.output_text(value_id, inline=True),
            class_="kpi-value",
            style="display: inline;",
        )
    ]
    if status_id:
        value_children.append(ui.output_ui(status_id, style="display: inline;"))
    if trend_id:
        value_children.append(ui.output_ui(trend_id, style="display: inline;"))

    label_row = ui.tags.div(
        ui.output_ui(label_id) if label_id else ui.tags.span(),
        class_="kpi-label-row",
    )

    if tooltip:
        card_hdr = ui.card_header(
            ui.tags.span(
                header,
                ui.tags.span(
                    " \u24d8",
                    title=tooltip,
                    style="cursor: help; opacity: 0.5; font-size: 0.85em;",
                ),
            )
        )
    else:
        card_hdr = ui.card_header(header)

    return ui.card(
        card_hdr,
        ui.tags.div(*value_children, class_="kpi-value-row"),
        label_row,
    )
