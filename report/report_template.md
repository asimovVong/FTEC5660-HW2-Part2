# FTEC5660 Homework 02 Part 2 — Report (max 4 pages)

**Student ID:** 1155244509  
**Agent name:** huangzixun_68498644（格式：nickname_XXXX）

---

## 1. Agent design and architecture

- **Objective:** Authenticate with Moltbook, subscribe to `/m/ftec5660`, upvote and comment on the specified post.
- **Design:** Deterministic state machine (no LLM planning): fixed sequence of REST calls.
- **Components:**
  - `config.py`: Base URL, submolt name, target post ID, encoded student ID and agent name.
  - `src/moltbook_tools.py`: REST wrappers (molt_me, molt_subscribe, molt_get_post, molt_upvote, molt_comment) based on https://www.moltbook.com/skill.md.
  - `src/agent.py`: Sequential execution with retries and file logging.

*(Insert a simple architecture diagram here if desired, e.g. State Machine: AUTH → VERIFY → SUBSCRIBE → UPVOTE → COMMENT → DONE.)*

---

## 2. Decision logic and autonomy level

- **Decision logic:** No dynamic planning; the assignment specifies the exact steps, so the agent follows a fixed pipeline. Each step is retried up to 3 times on failure.
- **Autonomy level:** Low autonomy — scripted workflow. The “agent” reads the skill document (used to implement the tool list) and then executes the required sequence.

---

## 3. Screenshots or logs of Moltbook interactions

- **Run log:** See `logs/run.log` (or paste a short excerpt below).
- **Moltbook evidence:** Add a screenshot of the target post on Moltbook showing your agent’s upvote and comment (with “huangzixun_68498644” visible).

*(Paste log excerpt or add: “See report/assets/run_log_excerpt.txt” and “See report/assets/moltbook_screenshot.png”.)*

---

## 4. Summary

The agent successfully authenticates, subscribes to `/m/ftec5660`, and performs upvote and comment on the required post. Comment text includes the required agent identifier for grading.

---

*Export this file to PDF (e.g. with Pandoc or “Print to PDF”) and submit as report.pdf (maximum 4 pages).*
