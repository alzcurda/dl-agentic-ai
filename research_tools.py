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
    return (
        f"Mock arXiv results for query: {query}\n\n"
        "Title: Recent Discoveries in Black Hole Physics\n"
        "Authors: Jane Doe, John Smith\n"
        "Summary: This paper discusses new insights into black hole horizons.\n"
        "Link: https://arxiv.org/abs/2105.12345"
    )


def tavily_search_tool(query: str) -> Any:
    """Perform a web search using Tavily.

    The real tool returns JSON with ``results`` containing URLs and snippets. Install ``tavily-python``
    and set the ``TAVILY_API_KEY`` environment variable to enable this.
    """
    import json
    return json.dumps({
        "query": query,
        "results": [
            {
                "title": "NASA discovers new black hole",
                "url": "https://nasa.gov/news/black-hole-discovery",
                "content": "A massive new black hole was found near the center of the galaxy."
            },
            {
                "title": "Understanding Black Holes",
                "url": "https://nature.com/articles/s41586-020-2815-5",
                "content": "A detailed review of black hole science."
            },
            {
                "title": "Blog about space",
                "url": "https://randomspaceblog.com/black-holes",
                "content": "Some interesting thoughts on black holes."
            }
        ]
    })


def wikipedia_search_tool(query: str) -> Any:
    """Search Wikipedia for a summary of *query*.

    A concrete implementation could use the ``wikipedia`` package to fetch a page summary.
    """
    return (
        f"Mock Wikipedia summary for: {query}\n"
        "A black hole is a region of spacetime where gravity is so strong that nothing, "
        "including light or other electromagnetic waves, has enough energy to escape it.\n"
        "Source: https://wikipedia.org/wiki/Black_hole"
    )
