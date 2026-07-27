# -*- coding: utf-8 -*-
"""X (Twitter) API path — auto-fetch Hajj/Umrah posts.

    X API  ->  x_api.py  ->  ai_pipeline.py  (via app._analyze_and_store_items)

This is a THIN wrapper over the existing, battle-tested search logic in
external_sources.search_x_posts(). It does NOT re-implement the HTTP call —
it reuses it and adds the two things the new unified schema needs:

    source_type = "X_API"     (so every row knows which of the 4 paths made it)
    source_url  = <post url>  (the permalink already returned by the search)

Nothing here is destructive: the original external_sources.fetch_x /
search_x_posts remain available and unchanged.
"""
import os

import external_sources

# Re-export the existing error type so callers keep one import site.
XFetchError = external_sources.XFetchError

SOURCE = "x"            # existing `source` column value (unchanged)
SOURCE_TYPE = "X_API"   # new `source_type` column value for this path


def configured() -> bool:
    """True when an X bearer token is present in the environment."""
    return bool(os.environ.get("X_BEARER_TOKEN") or os.environ.get("TWITTER_BEARER_TOKEN"))


def fetch(max_results: int = 50) -> dict:
    """Search X for Hajj/Umrah posts and return them ready for the pipeline.

    Returns {"query": str, "items": [item, ...]} — the SAME shape as
    external_sources.search_x_posts, but every item is tagged with
    source_type/source_url. Raises XFetchError when X isn't configured or
    the API rejects the request (handled by the route)."""
    result = external_sources.search_x_posts(max_results=max_results)
    items = result.get("items") or []
    for it in items:
        it["source_type"] = SOURCE_TYPE
        it["source_url"] = it.get("url")
    return {"query": result.get("query"), "items": items}
