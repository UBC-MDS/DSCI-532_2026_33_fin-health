import altair as alt
from components.kpi_card import kpi_card
from components.empty_chart import empty_chart


def test_kpi_card_returns_ui_element():
    """Verify kpi_card() returns a valid Shiny UI element."""
    card = kpi_card(header="Test", value_id="test_value")
    assert card is not None


def test_kpi_card_with_trend_and_label():
    """Verify kpi_card() with all optional parameters."""
    card = kpi_card(
        header="Test",
        value_id="test_value",
        trend_id="test_trend",
        label_id="test_label",
    )
    assert card is not None


def test_empty_chart_returns_altair_chart():
    """Verify empty_chart() returns an alt.Chart object."""
    chart = empty_chart()
    assert isinstance(chart, alt.Chart)


def test_empty_chart_custom_message():
    """Verify empty_chart() accepts a custom message."""
    chart = empty_chart("No data found")
    assert isinstance(chart, alt.Chart)
