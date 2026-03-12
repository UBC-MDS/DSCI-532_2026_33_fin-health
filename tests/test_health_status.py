"""Unit tests for health status classification and formatting helpers."""

from components.health_status import classify_health, format_currency


# --- classify_health tests (higher_is_better=True) ---


class TestClassifyHealthHigherIsBetter:
    """Tests for classify_health with higher_is_better=True (default)."""

    def test_healthy_above_threshold(self):
        assert classify_health(15.0, healthy=10.0, warning=0.0) == "healthy"

    def test_healthy_at_threshold(self):
        assert classify_health(10.0, healthy=10.0, warning=0.0) == "healthy"

    def test_warning_between_thresholds(self):
        assert classify_health(5.0, healthy=10.0, warning=0.0) == "warning"

    def test_warning_at_threshold(self):
        assert classify_health(0.0, healthy=10.0, warning=0.0) == "warning"

    def test_danger_below_warning(self):
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
        assert (
            classify_health(0.5, healthy=1.0, warning=2.0, higher_is_better=False)
            == "healthy"
        )

    def test_healthy_at_threshold(self):
        assert (
            classify_health(1.0, healthy=1.0, warning=2.0, higher_is_better=False)
            == "healthy"
        )

    def test_warning_between_thresholds(self):
        assert (
            classify_health(1.5, healthy=1.0, warning=2.0, higher_is_better=False)
            == "warning"
        )

    def test_warning_at_threshold(self):
        assert (
            classify_health(2.0, healthy=1.0, warning=2.0, higher_is_better=False)
            == "warning"
        )

    def test_danger_above_warning(self):
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
        assert format_currency(1234.0) == "$1,234M"

    def test_negative_value(self):
        assert format_currency(-567.0) == "-$567M"

    def test_zero(self):
        assert format_currency(0.0) == "$0M"

    def test_large_value(self):
        assert format_currency(120000.0) == "$120,000M"

    def test_small_negative(self):
        assert format_currency(-0.5) == "-$0M"
