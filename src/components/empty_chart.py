"""Reusable empty-state Altair chart for fallback display."""

import altair as alt
import pandas as pd


def empty_chart(message: str = "Data Unavailable") -> alt.Chart:
    """Return a text-only Altair chart for empty-state fallback."""
    return (
        alt.Chart(pd.DataFrame({"text": [message]}))
        .mark_text(size=18)
        .encode(text="text:N")
    )
