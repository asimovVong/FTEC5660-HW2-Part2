# -*- coding: utf-8 -*-
"""
Moltbook Social Agent — state machine: AUTH → VERIFY → SUBSCRIBE → UPVOTE → COMMENT → DONE.
Logs every step (HTTP summary, status, errors) for report evidence.
"""

from datetime import datetime
from enum import Enum
from typing import Callable

# When run from part2/ (e.g. python run.py or python -m src.agent), config is in parent.
from config import (
    get_api_key,
    SUBMOLT_NAME,
    TARGET_POST_ID,
    AGENT_NAME,
    post_id_from_url,
)
from src.moltbook_tools import (
    molt_me,
    molt_subscribe,
    molt_get_post,
    molt_upvote,
    molt_comment,
)


class State(str, Enum):
    AUTH = "AUTH"
    VERIFY_LOGIN = "VERIFY_LOGIN"
    SUBSCRIBE = "SUBSCRIBE"
    VERIFY_SUB = "VERIFY_SUB"
    TARGET_POST_RESOLVE = "TARGET_POST_RESOLVE"
    UPVOTE = "UPVOTE"
    COMMENT = "COMMENT"
    DONE = "DONE"


MAX_RETRIES = 3


def log(section: str, message: str, file=None):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{section}] {message}"
    print(line)
    if file:
        file.write(line + "\n")
        file.flush()


def run_step(
    name: str,
    step_fn: Callable[[], dict],
    log_file,
) -> dict:
    """Run one step with retries; log request/response summary."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log("STEP", f"{name} (attempt {attempt}/{MAX_RETRIES})", log_file)
            result = step_fn()
            log("RESULT", f"{name} OK: {str(result)[:300]}", log_file)
            return result
        except Exception as e:
            last_error = e
            log("ERROR", f"{name} attempt {attempt}: {e}", log_file)
    raise last_error


def run_agent(log_path: str | None = None):
    """
    Execute the required sequence: auth → subscribe /m/ftec5660 → upvote + comment on target post.
    Comment includes agent name for grader: "我是 prefix_XXXX" (e.g. 我是 huangzixun_68498644).
    """
    log_file = None
    if log_path:
        from pathlib import Path
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        log_file = open(log_path, "w", encoding="utf-8")

    try:
        log("INIT", "Moltbook Social Agent — Part 2 FTEC5660", log_file)
        log("CONFIG", f"SUBMOLT={SUBMOLT_NAME}, POST_ID={TARGET_POST_ID}, AGENT_NAME={AGENT_NAME}", log_file)

        api_key = get_api_key()
        log("AUTH", "Using MOLTBOOK_API_KEY (length hidden)", log_file)

        # 1) Verify login
        run_step(
            "VERIFY_LOGIN (GET /agents/me)",
            lambda: molt_me(api_key),
            log_file,
        )

        # 2) Subscribe to /m/ftec5660
        run_step(
            f"SUBSCRIBE (POST /submolts/{SUBMOLT_NAME}/subscribe)",
            lambda: molt_subscribe(api_key, SUBMOLT_NAME),
            log_file,
        )

        # 3) Resolve target post (optional get to verify it exists)
        run_step(
            "TARGET_POST_RESOLVE (GET /posts/{id})",
            lambda: molt_get_post(api_key, TARGET_POST_ID),
            log_file,
        )

        # 4) Upvote
        run_step(
            "UPVOTE (POST /posts/{id}/upvote)",
            lambda: molt_upvote(api_key, TARGET_POST_ID),
            log_file,
        )

        # 5) Comment — must include agent identity for grading (prefix_XXXX)
        comment_text = (
            f"Hello from FTEC5660 HW2 Part2 agent. 我是 {AGENT_NAME}，已完成作业要求的 upvote 与 comment。"
        )
        log("COMMENT", f"Posting comment: {comment_text}", log_file)
        run_step(
            "COMMENT (POST /posts/{id}/comments)",
            lambda: molt_comment(api_key, TARGET_POST_ID, comment_text),
            log_file,
        )

        log("DONE", "All steps completed successfully.", log_file)
        return True
    except Exception as e:
        log("FAIL", str(e), log_file)
        raise
    finally:
        if log_file:
            log_file.close()


if __name__ == "__main__":
    from config import LOGS_DIR
    run_agent(log_path=str(LOGS_DIR / "run.log"))
