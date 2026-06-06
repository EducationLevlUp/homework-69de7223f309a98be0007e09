"""Search tool module for the deep research agent."""

from __future__ import annotations

try:
    from langchain_community.tools import DuckDuckGoSearchResults
except ImportError:
    DuckDuckGoSearchResults = None  # type: ignore[misc,assignment]


def create_search_tool():
    """Create and return a DuckDuckGo search tool instance.

    DuckDuckGo is used because it requires no API key and is free.

    Returns:
        A LangChain-compatible search tool instance.

    Raises:
        ImportError: If langchain_community is not installed.
    """
    if DuckDuckGoSearchResults is None:
        raise ImportError(
            "langchain_community is not installed. "
            "Install it with: pip install langchain-community"
        )

    return DuckDuckGoSearchResults(
        name="internet_search",
        description="Search the internet for current information.",
    )
