# -*- coding: utf-8 -*-
"""
Moltbook REST API tools (from skill.md).
All requests use https://www.moltbook.com (with www) and Bearer token.
"""

import requests

BASE_URL = "https://www.moltbook.com/api/v1"
TIMEOUT = 15


def _headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def molt_me(api_key: str) -> dict:
    """GET /agents/me — verify authentication and get current agent profile."""
    r = requests.get(
        f"{BASE_URL}/agents/me",
        headers=_headers(api_key),
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def molt_agent_status(api_key: str) -> dict:
    """GET /agents/status — check claim status (pending_claim / claimed)."""
    r = requests.get(
        f"{BASE_URL}/agents/status",
        headers=_headers(api_key),
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def molt_subscribe(api_key: str, submolt_name: str) -> dict:
    """POST /submolts/{name}/subscribe — subscribe to a submolt (e.g. ftec5660)."""
    r = requests.post(
        f"{BASE_URL}/submolts/{submolt_name}/subscribe",
        headers=_headers(api_key),
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def molt_get_post(api_key: str, post_id: str) -> dict:
    """GET /posts/{post_id} — get a single post by ID."""
    r = requests.get(
        f"{BASE_URL}/posts/{post_id}",
        headers=_headers(api_key),
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def molt_upvote(api_key: str, post_id: str) -> dict:
    """POST /posts/{post_id}/upvote — upvote a post."""
    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/upvote",
        headers=_headers(api_key),
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


def molt_comment(api_key: str, post_id: str, content: str) -> dict:
    """POST /posts/{post_id}/comments — add a comment."""
    r = requests.post(
        f"{BASE_URL}/posts/{post_id}/comments",
        headers=_headers(api_key),
        json={"content": content},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()
