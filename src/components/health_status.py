"""Pure helper functions for financial health classification and formatting."""


def classify_health(value: float, healthy: float, warning: float, higher_is_better: bool = True) -> str:
    """Classify a financial metric value into a health status.

    Parameters
    ----------
    value : float
        The metric value to classify.
    healthy : float
        Threshold for "healthy" status.
    warning : float
        Threshold for "warning" status (between healthy and danger).
    higher_is_better : bool
        If True, values >= healthy are healthy. If False, values <= healthy are healthy.

    Returns
    -------
    str
        One of "healthy", "warning", or "danger".
    """
    if higher_is_better:
        if value >= healthy:
            return "healthy"
        elif value >= warning:
            return "warning"
        else:
            return "danger"
    else:
        if value <= healthy:
            return "healthy"
        elif value <= warning:
            return "warning"
        else:
            return "danger"


def format_currency(value: float) -> str:
    """Format a dollar value in millions with sign.

    Parameters
    ----------
    value : float
        Dollar amount in millions.

    Returns
    -------
    str
        Formatted string like "$1,234M" or "-$567M".
    """
    if value < 0:
        return f"-${abs(value):,.0f}M"
    return f"${value:,.0f}M"