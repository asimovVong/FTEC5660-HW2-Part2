# Report Outline — FTEC5660 HW02 Part 2 (Moltbook Social Agent)

Use this outline to write **report.pdf** (maximum **4 pages**) for submission.

---

## 1. Agent design and architecture

- **Objective:** Autonomous agent that (1) authenticates with Moltbook API, (2) subscribes to `/m/ftec5660`, (3) upvotes and comments on the specified post.
- **Design:**
  - **Tools (self-written, per assignment):** `molt_me`, `molt_subscribe`, `molt_get_post`, `molt_upvote`, `molt_comment` — implemented according to [Moltbook skill.md](https://www.moltbook.com/skill.md).
  - **State machine:** `AUTH` → `VERIFY_LOGIN` → `SUBSCRIBE` → `VERIFY_SUB` → `TARGET_POST_RESOLVE` → `UPVOTE` → `COMMENT` → `DONE`.
  - **Config:** API base `https://www.moltbook.com/api/v1`, fixed submolt `ftec5660`, target post ID from assignment URL.
- **Architecture diagram (ASCII or figure):**  
  `[.env: API_KEY] → [moltbook_agent.py] → [State machine + HTTP tools] → [Moltbook REST API]`  
  Optional: sketch states and transitions.

---

## 2. Decision logic and autonomy level

- **Decision logic:**
  - Sequential execution of the three tasks; each step checks API response and retries (e.g. up to 3 times) on failure.
  - Success criteria: no `error` in response, and `success` not `false`; for subscribe, “already subscribed” is treated as success.
- **Autonomy level:** Deterministic state machine with no LLM: agent follows a fixed workflow using the documented API. Autonomy is in “what to send” (e.g. comment text) and retry/error handling; no high-level planning.

---

## 3. Screenshots or logs of Moltbook interactions

- **Logs:** Paste 1–2 excerpts from `logs/run.log` showing:
  - `VERIFY_LOGIN` (e.g. `GET …/agents/me` and response).
  - `SUBSCRIBE` (e.g. `POST …/submolts/ftec5660/subscribe`).
  - `UPVOTE` and `COMMENT` (method, URL, status, and short result).
- **Screenshots:** If available, add:
  - Moltbook post page showing your upvote and comment.
  - Agent nickname in comment: “我是 prefix_XXXX (e.g. huangzixun_68498644)”.

---

## 4. (Optional) Implementation notes

- **Agent naming:** `prefix_XXXX` (e.g. `huangzixun_68498644`), XXXX = `encode_student_id(STUDENT_ID)` from the Colab notebook. Set `AGENT_NAME_PREFIX` in .env to match registration.
- **Security:** API key only in `.env`, never in code or repo.
- **Reproducibility:** `python moltbook_agent.py` with correct `.env` reproduces the run; logs are written to `logs/run.log`.

---

Convert this outline to **report.pdf** (max 4 pages) and submit with your source code in the public GitHub repository.
