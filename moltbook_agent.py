# -*- coding: utf-8 -*-
"""
FTEC5660 Homework 02 (Part 2) — Moltbook Social Agent
Autonomous agent: authenticate → subscribe /m/ftec5660 → upvote & comment on target post.
Run: python moltbook_agent.py (requires .env with MOLTBOOK_API_KEY, optional STUDENT_ID)
"""

import os
import re
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config & Constants (per assignment)
# ---------------------------------------------------------------------------
load_dotenv()

BASE_URL = "https://www.moltbook.com/api/v1"
SUBMOLT_NAME = "ftec5660"  # /m/ftec5660
TARGET_POST_URL = "https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c"
TARGET_POST_ID = "47ff50f3-8255-4dee-87f4-2c3637c7351c"

# Agent naming: nickname_XXXX (prefix_encoded_id). Set AGENT_NAME_PREFIX in .env (e.g. huangzixun).
STUDENT_ID = int(os.environ.get("STUDENT_ID", "0"))
AGENT_NAME_PREFIX = os.environ.get("AGENT_NAME_PREFIX", "nickname")
MOLTBOOK_API_KEY = os.environ.get("MOLTBOOK_API_KEY", "").strip()

# Logging
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
RUN_LOG = LOG_DIR / "run.log"

# ---------------------------------------------------------------------------
# Encode student ID (from Colab notebook)
# ---------------------------------------------------------------------------
def encode_student_id(student_id: int) -> str:
    """Reversibly encode student ID for agent name. Format: prefix_XXXX (e.g. nickname_68498644)."""
    if student_id < 0:
        raise ValueError("student_id must be non-negative")
    M = 10**8
    a, b = 137, 911
    encoded = (a * student_id + b) % M
    return f"{encoded:08d}"


def get_agent_nickname() -> str:
    """Return agent display name: prefix_XXXX (e.g. huangzixun_68498644)."""
    if STUDENT_ID <= 0:
        return f"{AGENT_NAME_PREFIX}_00000000"
    return f"{AGENT_NAME_PREFIX}_{encode_student_id(STUDENT_ID)}"


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
def setup_logging():
    """Write to run.log and optionally stdout."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(RUN_LOG, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def log_http(logger: logging.Logger, method: str, url: str, status: int, summary: str = ""):
    """Log HTTP request summary for run.log."""
    logger.info("HTTP %s %s -> %s %s", method, url, status, summary)


# ---------------------------------------------------------------------------
# Moltbook API tools (aligned with https://www.moltbook.com/skill.md)
# ---------------------------------------------------------------------------
def _headers() -> dict:
    if not MOLTBOOK_API_KEY:
        raise ValueError("MOLTBOOK_API_KEY is not set (check .env)")
    return {
        "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
        "Content-Type": "application/json",
    }


def molt_me(logger: logging.Logger) -> dict:
    """Verify authentication. GET /agents/me."""
    url = f"{BASE_URL}/agents/me"
    try:
        r = requests.get(url, headers=_headers(), timeout=15)
        log_http(logger, "GET", url, r.status_code, r.text[:200] if r.text else "")
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.exception("molt_me failed")
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}


def molt_subscribe(submolt_name: str, logger: logging.Logger) -> dict:
    """Subscribe to a submolt. POST /submolts/{name}/subscribe."""
    url = f"{BASE_URL}/submolts/{submolt_name}/subscribe"
    try:
        r = requests.post(url, headers=_headers(), timeout=15)
        log_http(logger, "POST", url, r.status_code, r.text[:200] if r.text else "")
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.exception("molt_subscribe failed")
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}


def molt_get_post(post_id: str, logger: logging.Logger) -> dict:
    """Get a single post. GET /posts/{post_id}."""
    url = f"{BASE_URL}/posts/{post_id}"
    try:
        r = requests.get(url, headers=_headers(), timeout=15)
        log_http(logger, "GET", url, r.status_code, r.text[:200] if r.text else "")
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.exception("molt_get_post failed")
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}


def molt_upvote(post_id: str, logger: logging.Logger) -> dict:
    """Upvote a post. POST /posts/{post_id}/upvote."""
    url = f"{BASE_URL}/posts/{post_id}/upvote"
    try:
        r = requests.post(url, headers=_headers(), timeout=15)
        log_http(logger, "POST", url, r.status_code, r.text[:200] if r.text else "")
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.exception("molt_upvote failed")
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}


def molt_comment(post_id: str, content: str, logger: logging.Logger) -> dict:
    """Comment on a post. POST /posts/{post_id}/comments."""
    url = f"{BASE_URL}/posts/{post_id}/comments"
    try:
        r = requests.post(
            url,
            headers=_headers(),
            json={"content": content},
            timeout=15,
        )
        log_http(logger, "POST", url, r.status_code, r.text[:200] if r.text else "")
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.exception("molt_comment failed")
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------
class State:
    AUTH = "AUTH"
    VERIFY_LOGIN = "VERIFY_LOGIN"
    SUBSCRIBE = "SUBSCRIBE"
    VERIFY_SUB = "VERIFY_SUB"
    TARGET_POST_RESOLVE = "TARGET_POST_RESOLVE"
    UPVOTE = "UPVOTE"
    COMMENT = "COMMENT"
    DONE = "DONE"


def is_ok(result: dict) -> bool:
    """True if API result indicates success (no 'error' key)."""
    if not result:
        return False
    if "error" in result:
        return False
    if result.get("success") is False:
        return False
    return True


def run_agent(max_retries: int = 3) -> bool:
    """Run the Moltbook agent: auth → subscribe → upvote → comment. Returns True if all steps succeeded."""
    logger = setup_logging()
    logger.info("========== Moltbook Agent Run Start ==========")
    logger.info("Agent nickname: %s", get_agent_nickname())
    logger.info("Submolt: /m/%s | Post: %s", SUBMOLT_NAME, TARGET_POST_ID)

    current = State.AUTH
    success = True

    # ----- AUTH / VERIFY -----
    for attempt in range(1, max_retries + 1):
        logger.info("[%s] Attempt %d/%d", State.VERIFY_LOGIN, attempt, max_retries)
        me = molt_me(logger)
        if is_ok(me):
            logger.info("Verified agent: %s", me.get("agent", me).get("name", me))
            break
        logger.warning("Verify login failed: %s", me)
        if attempt == max_retries:
            logger.error("AUTH failed after %d retries", max_retries)
            return False
        time.sleep(2)

    # ----- SUBSCRIBE -----
    for attempt in range(1, max_retries + 1):
        logger.info("[%s] Subscribe /m/%s Attempt %d/%d", State.SUBSCRIBE, SUBMOLT_NAME, attempt, max_retries)
        sub = molt_subscribe(SUBMOLT_NAME, logger)
        if is_ok(sub) or (isinstance(sub, dict) and sub.get("error", "").lower().find("already") >= 0):
            logger.info("Subscribe /m/%s OK", SUBMOLT_NAME)
            break
        logger.warning("Subscribe failed: %s", sub)
        if attempt == max_retries:
            logger.error("SUBSCRIBE failed after %d retries", max_retries)
            success = False
        else:
            time.sleep(2)

    # ----- TARGET POST (optional verify) -----
    logger.info("[%s] Resolve post %s", State.TARGET_POST_RESOLVE, TARGET_POST_ID)
    post = molt_get_post(TARGET_POST_ID, logger)
    if not is_ok(post):
        logger.warning("Get post failed (continuing anyway): %s", post)

    # ----- UPVOTE -----
    for attempt in range(1, max_retries + 1):
        logger.info("[%s] Attempt %d/%d", State.UPVOTE, attempt, max_retries)
        up = molt_upvote(TARGET_POST_ID, logger)
        if is_ok(up):
            logger.info("Upvote success: %s", up.get("message", up))
            break
        logger.warning("Upvote failed: %s", up)
        if attempt == max_retries:
            logger.error("UPVOTE failed after %d retries", max_retries)
            success = False
        else:
            time.sleep(2)

    # ----- COMMENT -----
    nickname = get_agent_nickname()
    comment_text = (
        f"Hello from FTEC5660 agent. 我是{nickname}，已完成作业 Part 2：订阅 submolt、点赞并评论。"
    )
    for attempt in range(1, max_retries + 1):
        logger.info("[%s] Attempt %d/%d | content: %s", State.COMMENT, attempt, max_retries, comment_text[:80])
        cmt = molt_comment(TARGET_POST_ID, comment_text, logger)
        if is_ok(cmt):
            logger.info("Comment success: %s", cmt.get("comment", cmt))
            break
        logger.warning("Comment failed: %s", cmt)
        if attempt == max_retries:
            logger.error("COMMENT failed after %d retries", max_retries)
            success = False
        else:
            time.sleep(2)

    logger.info("========== Moltbook Agent Run End | success=%s ==========", success)
    return success


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not MOLTBOOK_API_KEY:
        print("Error: Set MOLTBOOK_API_KEY in .env (and optionally AGENT_NAME_PREFIX, STUDENT_ID).")
        sys.exit(1)
    ok = run_agent()
    sys.exit(0 if ok else 1)
