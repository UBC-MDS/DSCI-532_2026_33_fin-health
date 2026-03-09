"""Standalone QueryChat behavior tests using qc.client() outside Shiny."""

import os

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("GITHUB_TOKEN"),
    reason="GITHUB_TOKEN not set — skipping LLM-backed tests",
)

from pages.ai_explorer import DATA_DESCRIPTION, EXTRA_INSTRUCTIONS, GREETING  # noqa: E402
from data import df  # noqa: E402

import querychat  # noqa: E402
from chatlas import ChatGithub  # noqa: E402


@pytest.fixture(scope="module")
def chat():
    """Create a standalone chatlas.Chat from QueryChat.client()."""
    qc = querychat.QueryChat(
        df,
        "financial_data",
        data_description=DATA_DESCRIPTION,
        extra_instructions=EXTRA_INSTRUCTIONS,
        greeting=GREETING,
        client=ChatGithub(model="gpt-4.1-mini"),
    )
    return qc.client()


def _tool_names(chat_instance):
    """Extract tool-call function names from the last assistant turn."""
    turns = chat_instance.get_turns()
    names = []
    for turn in reversed(turns):
        if turn.role == "assistant":
            for part in turn.contents:
                if hasattr(part, "name"):
                    names.append(part.name)
            break
    return names


def test_filter_uses_update_dashboard(chat):
    """A filter prompt should invoke the querychat_update_dashboard tool."""
    chat.chat("Show only IT companies")
    names = _tool_names(chat)
    assert "querychat_update_dashboard" in names, (
        f"Expected update_dashboard, got {names}"
    )


def test_stats_use_querychat_query(chat):
    """An aggregate question should invoke the querychat_query tool."""
    chat.chat("What is the average revenue by sector?")
    names = _tool_names(chat)
    assert "querychat_query" in names, f"Expected querychat_query, got {names}"


def test_response_has_structured_format(chat):
    """Response should follow the structured format from EXTRA_INSTRUCTIONS."""
    response = chat.chat("Which company had the highest ROE in 2022?")
    text = str(response).lower()
    assert any(
        keyword in text for keyword in ["filters applied", "key stats", "insight"]
    ), f"Response missing structured format keywords: {text[:300]}"
