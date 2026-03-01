# -*- coding: utf-8 -*-
"""
FTEC5660 Homework 02 Part 2 — Moltbook Social Agent
Configuration: API base, target submolt, target post, agent naming.
"""

import os
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Moltbook API (from https://www.moltbook.com/skill.md)
# ---------------------------------------------------------------------------
BASE_URL = "https://www.moltbook.com/api/v1"

# Assignment requirements (Part 2 PDF)
SUBMOLT_NAME = "ftec5660"  # Subscribe to /m/ftec5660
TARGET_POST_URL = "https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c"
# Post ID extracted from URL (UUID after /post/)
TARGET_POST_ID = "47ff50f3-8255-4dee-87f4-2c3637c7351c"

# ---------------------------------------------------------------------------
# Agent naming: nickname_XXXX (prefix_encoded_id, from Colab encode_student_id)
# ---------------------------------------------------------------------------
def encode_student_id(student_id: int) -> str:
    """
    Reversibly encode student ID (affine cipher). From Colab notebook.
    """
    if student_id < 0:
        raise ValueError("student_id must be non-negative")
    M = 10**8
    a, b = 137, 911
    encoded = (a * student_id + b) % M
    return f"{encoded:08d}"


STUDENT_ID = 1155244509
ENCODED_ID = encode_student_id(STUDENT_ID)
# Format: prefix_XXXX (e.g. huangzixun_68498644 or nickname_68498644). Set AGENT_NAME_PREFIX in .env.
AGENT_NAME_PREFIX = os.environ.get("AGENT_NAME_PREFIX", "nickname")
AGENT_NAME = f"{AGENT_NAME_PREFIX}_{ENCODED_ID}"

# ---------------------------------------------------------------------------
# Secrets (from environment; do not commit)
# ---------------------------------------------------------------------------
def get_api_key() -> str:
    key = os.environ.get("MOLTBOOK_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "MOLTBOOK_API_KEY is not set. "
            "Add it to .env or export MOLTBOOK_API_KEY=..."
        )
    return key


def post_id_from_url(url: str) -> str:
    """Extract post ID (UUID) from Moltbook post URL."""
    # e.g. https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c
    m = re.search(r"/post/([a-f0-9\-]{36})", url, re.I)
    if m:
        return m.group(1)
    # If already a raw UUID, accept it
    if re.match(r"^[a-f0-9\-]{36}$", url.strip(), re.I):
        return url.strip()
    raise ValueError(f"Cannot extract post_id from URL: {url}")


# Paths
PART2_ROOT = Path(__file__).resolve().parent
LOGS_DIR = PART2_ROOT / "logs"
REPORT_DIR = PART2_ROOT / "report"
LOGS_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
