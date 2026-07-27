# -*- coding: utf-8 -*-
"""Reddit API path — auto-fetch Hajj/Umrah posts + top comments.

    Reddit API  ->  reddit_api.py  ->  ai_pipeline.py

Thin wrapper over external_sources.search_reddit_posts() (OAuth2 client
credentials, subreddit/keyword search — already implemented and tested). It
adds the unified-schema tags:

    source_type = "Reddit_API"
    source_url  = <permalink>

The existing external_sources.fetch_reddit / search_reddit_posts stay intact.
"""
import os

import external_sources

RedditFetchError = external_sources.RedditFetchError

SOURCE = "reddit"
SOURCE_TYPE = "Reddit_API"


def configured() -> bool:
    """True when Reddit client credentials are present."""
    return bool(os.environ.get("REDDIT_CLIENT_ID") and os.environ.get("REDDIT_CLIENT_SECRET"))


def fetch(max_posts: int = 20, max_comments_per_post: int = 8) -> dict:
    """Search Reddit for Hajj/Umrah posts (+ a few top comments each) and
    return them ready for the pipeline.

    Returns {"query": str, "items": [item, ...]} with every item tagged
    source_type="Reddit_API" and source_url=<permalink>. Raises
    RedditFetchError when Reddit isn't configured or the API rejects the
    request."""
    result = external_sources.search_reddit_posts(
        max_posts=max_posts, max_comments_per_post=max_comments_per_post)
    items = result.get("items") or []
    for it in items:
        it["source_type"] = SOURCE_TYPE
        it["source_url"] = it.get("url")
    return {"query": result.get("query"), "items": items}
