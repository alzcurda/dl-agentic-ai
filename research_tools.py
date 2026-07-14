# Minimal tool wrappers for research steps.

"""Placeholder implementations for research tools used in the evaluation notebook.

The notebook expects three functions:
- ``arxiv_search_tool``
- ``tavily_search_tool``
- ``wikipedia_search_tool``

These stubs raise ``NotImplementedError`` and can be replaced with real API calls when the
necessary credentials and packages are available.
"""

from typing import Any


def arxiv_search_tool(query: str) -> Any:
    """Search arXiv for papers matching *query*.

    In a full implementation this would call the arXiv API (e.g., via ``arxiv`` package) and
    return a structured list of results.
    """
    raise NotImplementedError(
        "arxiv_search_tool is not implemented – install an arXiv client and provide any required API keys."
    )


def tavily_search_tool(query: str) -> Any:
    """Perform a web search using Tavily.

    The real tool returns JSON with ``results`` containing URLs and snippets. Install ``tavily-python``
    and set the ``TAVILY_API_KEY`` environment variable to enable this.
    """
    raise NotImplementedError(
        "tavily_search_tool is not implemented – install tavily-python and configure the API key."
    )


def wikipedia_search_tool(query: str) -> Any:
    """Search Wikipedia for a summary of *query*.

    A concrete implementation could use the ``wikipedia`` package to fetch a page summary.
    """
    raise NotImplementedError(
        "wikipedia_search_tool is not implemented – install the wikipedia package."
    )
