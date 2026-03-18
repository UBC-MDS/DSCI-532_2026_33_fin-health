import altair as alt
from components.kpi_card import kpi_card
from components.empty_chart import empty_chart


def test_kpi_card_returns_ui_element():
    """KPI card with minimal args renders a valid UI element, ensuring dashboard cards display correctly."""
    card = kpi_card(header="Test", value_id="test_value")
    assert card is not None


def test_kpi_card_with_trend_and_label():
    """KPI card with trend and label slots renders correctly, supporting the full card layout on both pages."""
    card = kpi_card(
        header="Test",
        value_id="test_value",
        trend_id="test_trend",
        label_id="test_label",
    )
    assert card is not None


def test_empty_chart_returns_altair_chart():
    """Empty chart placeholder renders a valid Altair chart, preventing blank spaces when no data matches."""
    chart = empty_chart()
    assert isinstance(chart, alt.Chart)


def test_empty_chart_custom_message():
    """Empty chart with a custom message renders correctly, giving users context about why data is missing."""
    chart = empty_chart("No data found")
    assert isinstance(chart, alt.Chart)
