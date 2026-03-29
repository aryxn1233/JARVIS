"""
OS Layer: Web Search
Performs web searches using DuckDuckGo's free Instant Answer API.
No API key required.
"""

import requests
from core.logger import log_event


DDGO_API = "https://api.duckduckgo.com/"


def search_web(query: str, max_results: int = 3) -> str:
    """
    Searches DuckDuckGo and returns a formatted text summary.
    Uses the Instant Answer API (no key, no rate limits).
    """
    if not query:
        return "No search query provided."

    try:
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }

        response = requests.get(DDGO_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []

        # Abstract (Wikipedia-style summary)
        abstract = data.get("AbstractText", "").strip()
        if abstract:
            source = data.get("AbstractSource", "")
            results.append(f"📖 {abstract}\n   — {source}")

        # Instant answer
        answer = data.get("Answer", "").strip()
        if answer:
            results.append(f"✅ {answer}")

        # Definition
        definition = data.get("Definition", "").strip()
        if definition:
            def_source = data.get("DefinitionSource", "")
            results.append(f"📝 {definition}\n   — {def_source}")

        # Related topics
        related = data.get("RelatedTopics", [])
        count = 0
        for topic in related:
            if count >= max_results:
                break
            text = topic.get("Text", "").strip()
            if text:
                results.append(f"• {text}")
                count += 1

        if not results:
            return (
                f"No instant answer found for '{query}'.\n"
                f"Try: https://duckduckgo.com/?q={requests.utils.quote(query)}"
            )

        log_event(f"Web search completed: {query}")
        return "\n\n".join(results)

    except requests.exceptions.ConnectionError:
        log_event("Web search failed: no internet connection.", level="warning")
        return "Web search failed: no internet connection."

    except Exception as e:
        log_event(f"Web search error: {e}", level="error")
        return f"Web search failed: {e}"
