"""Unit tests for health status classification and formatting helpers."""

from components.health_status import classify_health, format_currency


# --- classify_health tests (higher_is_better=True) ---


class TestClassifyHealthHigherIsBetter:
    """Tests for classify_health with higher_is_better=True (default)."""

    def test_healthy_above_threshold(self):
        """Values above the healthy threshold are classified as healthy, showing green status on KPI cards."""
        assert classify_health(15.0, healthy=10.0, warning=0.0) == "healthy"

    def test_healthy_at_threshold(self):
        """Values exactly at the healthy threshold are inclusive, ensuring boundary values render correctly."""
        assert classify_health(10.0, healthy=10.0, warning=0.0) == "healthy"

    def test_warning_between_thresholds(self):
        """Values between warning and healthy thresholds show amber status to alert users of moderate risk."""
        assert classify_health(5.0, healthy=10.0, warning=0.0) == "warning"

    def test_warning_at_threshold(self):
        """Values exactly at the warning threshold are inclusive, ensuring boundary values render correctly."""
        assert classify_health(0.0, healthy=10.0, warning=0.0) == "warning"

    def test_danger_below_warning(self):
        """Values below the warning threshold show red danger status to flag poor financial health."""
        assert classify_health(-5.0, healthy=10.0, warning=0.0) == "danger"

    def test_npm_healthy(self):
        """Net Profit Margin >= 10% is healthy."""
        assert classify_health(12.5, healthy=10.0, warning=0.0) == "healthy"

    def test_npm_warning(self):
        """Net Profit Margin 0-10% is warning."""
        assert classify_health(5.0, healthy=10.0, warning=0.0) == "warning"

    def test_npm_danger(self):
        """Net Profit Margin < 0% is danger."""
        assert classify_health(-3.0, healthy=10.0, warning=0.0) == "danger"

    def test_roe_healthy(self):
        """ROE >= 15% is healthy."""
        assert classify_health(20.0, healthy=15.0, warning=0.0) == "healthy"

    def test_current_ratio_healthy(self):
        """Current Ratio >= 1.5 is healthy."""
        assert classify_health(2.0, healthy=1.5, warning=1.0) == "healthy"

    def test_current_ratio_warning(self):
        """Current Ratio 1.0-1.5 is warning."""
        assert classify_health(1.2, healthy=1.5, warning=1.0) == "warning"

    def test_current_ratio_danger(self):
        """Current Ratio < 1.0 is danger."""
        assert classify_health(0.8, healthy=1.5, warning=1.0) == "danger"


# --- classify_health tests (higher_is_better=False) ---


class TestClassifyHealthLowerIsBetter:
    """Tests for classify_health with higher_is_better=False (e.g., Debt/Equity)."""

    def test_healthy_below_threshold(self):
        """Low values are healthy when lower is better (e.g., low debt is good), showing green status."""
        assert (
            classify_health(0.5, healthy=1.0, warning=2.0, higher_is_better=False)
            == "healthy"
        )

    def test_healthy_at_threshold(self):
        """Values exactly at the healthy threshold are inclusive for lower-is-better metrics."""
        assert (
            classify_health(1.0, healthy=1.0, warning=2.0, higher_is_better=False)
            == "healthy"
        )

    def test_warning_between_thresholds(self):
        """Values between thresholds show amber warning for lower-is-better metrics like Debt/Equity."""
        assert (
            classify_health(1.5, healthy=1.0, warning=2.0, higher_is_better=False)
            == "warning"
        )

    def test_warning_at_threshold(self):
        """Values exactly at the warning threshold are inclusive for lower-is-better metrics."""
        assert (
            classify_health(2.0, healthy=1.0, warning=2.0, higher_is_better=False)
            == "warning"
        )

    def test_danger_above_warning(self):
        """High values above warning are flagged as danger for lower-is-better metrics like Debt/Equity."""
        assert (
            classify_health(3.0, healthy=1.0, warning=2.0, higher_is_better=False)
            == "danger"
        )

    def test_debt_equity_healthy(self):
        """Debt/Equity <= 1.0 is healthy."""
        assert (
            classify_health(0.8, healthy=1.0, warning=2.0, higher_is_better=False)
            == "healthy"
        )

    def test_debt_equity_danger(self):
        """Debt/Equity > 2.0 is danger."""
        assert (
            classify_health(5.0, healthy=1.0, warning=2.0, higher_is_better=False)
            == "danger"
        )


# --- format_currency tests ---


class TestFormatCurrency:
    """Tests for format_currency."""

    def test_positive_value(self):
        """Positive values format with dollar sign and commas, ensuring readable KPI display."""
        assert format_currency(1234.0) == "$1,234M"

    def test_negative_value(self):
        """Negative values format with leading minus sign so users can spot losses immediately."""
        assert format_currency(-567.0) == "-$567M"

    def test_zero(self):
        """Zero formats as $0M rather than blank, so KPI cards always show a value."""
        assert format_currency(0.0) == "$0M"

    def test_large_value(self):
        """Large values include comma grouping for readability in the dashboard KPI cards."""
        assert format_currency(120000.0) == "$120,000M"

    def test_small_negative(self):
        """Sub-unit negative values round to $0M with minus sign, avoiding misleading precision."""
        assert format_currency(-0.5) == "-$0M"
