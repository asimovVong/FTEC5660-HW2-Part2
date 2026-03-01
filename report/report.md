# FTEC5660 Homework 02 (Part 2) — Moltbook Social Agent Report

**Student ID:** 1155244509  
**Agent name:** huangzixun_68498644 (format: nickname_XXXX)  
**Maximum 4 pages** — export this document to **report.pdf** for submission.

---

## 1. Agent design and architecture

**Objective.** The agent must (1) authenticate with the Moltbook API using an API key, (2) subscribe to `/m/ftec5660`, and (3) upvote and comment on the specified post:  
https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c  

**Design.** A deterministic state machine (no LLM) drives a fixed sequence of REST calls. The tool list is implemented according to [Moltbook skill.md](https://www.moltbook.com/skill.md), as required.

**Components.**

| Component | Role |
|-----------|------|
| `config.py` | Base URL, submolt name, target post ID, agent naming (prefix + encoded student ID from Colab). |
| `src/moltbook_tools.py` | REST wrappers: `molt_me`, `molt_subscribe`, `molt_get_post`, `molt_upvote`, `molt_comment`. |
| `src/agent.py` | State machine: sequential execution with retries and file logging. |
| `run.py` / `moltbook_agent.py` | Entry points; load `.env` and invoke the agent. |

**Architecture (high level).**

```
[.env: MOLTBOOK_API_KEY, AGENT_NAME_PREFIX, STUDENT_ID]
        → [run.py / moltbook_agent.py]
        → [State machine: VERIFY_LOGIN → SUBSCRIBE → UPVOTE → COMMENT]
        → [moltbook_tools: HTTP calls]
        → [Moltbook REST API: https://www.moltbook.com/api/v1]
        → [logs/run.log]
```

**State flow.** AUTH → VERIFY_LOGIN → SUBSCRIBE → VERIFY_SUB → TARGET_POST_RESOLVE → UPVOTE → COMMENT → DONE. Each step is retried up to 3 times on failure.

---

## 2. Decision logic and autonomy level

**Decision logic.** There is no dynamic planning. The assignment specifies the exact steps, so the agent follows a fixed pipeline. For each step:

- Success: response has no `error` and `success` is not `false` (for subscribe, “already subscribed” is treated as success).
- Failure: retry up to 3 times with short delay, then log and continue or exit as appropriate.

**Autonomy level.** Low autonomy — scripted workflow. The agent does not use an LLM for planning; it executes the required sequence using the documented API. Autonomy is limited to (1) the comment text (which includes the agent identifier for grading) and (2) retry and error handling.

---

## 3. Screenshots or logs of Moltbook interactions

**Run log excerpt.** The following is taken from `logs/run.log` after a successful run:

```
2026-03-01 18:24:03 | INFO | ========== Moltbook Agent Run Start ==========
2026-03-01 18:24:03 | INFO | Agent nickname: huangzixun_68498644
2026-03-01 18:24:03 | INFO | Submolt: /m/ftec5660 | Post: 47ff50f3-8255-4dee-87f4-2c3637c7351c
2026-03-01 18:24:03 | INFO | [VERIFY_LOGIN] Attempt 1/3
2026-03-01 18:24:04 | INFO | HTTP GET https://www.moltbook.com/api/v1/agents/me -> 200 {"success":true,"agent":{...}}
2026-03-01 18:24:04 | INFO | Verified agent: huangzixun_68498644
2026-03-01 18:24:04 | INFO | [SUBSCRIBE] Subscribe /m/ftec5660 Attempt 1/3
2026-03-01 18:24:05 | INFO | HTTP POST https://www.moltbook.com/api/v1/submolts/ftec5660/subscribe -> 201 {"success":true,"message":"Subscribed to m/ftec5660! 🦞","action":"subscribed"}
2026-03-01 18:24:05 | INFO | Subscribe /m/ftec5660 OK
2026-03-01 18:24:06 | INFO | [UPVOTE] Attempt 1/3
2026-03-01 18:24:07 | INFO | HTTP POST .../posts/47ff50f3-8255-4dee-87f4-2c3637c7351c/upvote -> 200 {"success":true,"message":"Upvoted! 🦞"}
2026-03-01 18:24:07 | INFO | [COMMENT] Attempt 1/3 | content: Hello from FTEC5660 agent. 我是huangzixun_68498644，已完成作业 Part 2：...
2026-03-01 18:24:08 | INFO | HTTP POST .../comments -> 201 {"success":true,"message":"Comment added! 🦞",...}
2026-03-01 18:24:08 | INFO | ========== Moltbook Agent Run End | success=True ==========
```

**Moltbook evidence (screenshot).**

<!-- [您需要自行添加] 请在此处插入一张 Moltbook 帖子页面的截图：打开 https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c ，截图中需能清晰看到你的 upvote 以及你的评论（评论中可见 huangzixun_68498644）。可将截图保存为 report/moltbook_screenshot.png 并在此处引用，或直接粘贴到导出后的 PDF 中。 -->

*[PLACEHOLDER — YOU MUST ADD]* Insert a screenshot of the Moltbook post page (https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c) showing your agent’s upvote and your comment with “huangzixun_68498644” visible. Save as e.g. `report/moltbook_screenshot.png` and include it in the exported PDF.

---

## 4. Summary

The agent successfully authenticates with the Moltbook API, subscribes to `/m/ftec5660`, and performs upvote and comment on the required post. The comment includes the required agent identifier (huangzixun_68498644) for grading. Logs are written to `logs/run.log` for reproducibility.

---

## 您需要自行完成 / 提交的内容（中文）

1. **Moltbook 截图**  
   在报告第 3 节中插入一张截图：打开作业指定帖子，截图中能看出你的 upvote 和评论（评论里可见 huangzixun_68498644）。可保存为 `report/moltbook_screenshot.png` 或在 Word/排版软件中直接粘贴。

2. **导出为 report.pdf**  
   将本报告导出为 **report.pdf**，总页数不超过 **4 页**。可用 VS Code/Cursor 的 Markdown PDF 插件、Pandoc、或复制到 Word/Pages 后另存为 PDF。

3. **上传到 GitHub**  
   将 **report.pdf** 与 Part 2 的**源代码**一起放入你的**公开 GitHub 仓库**。不要提交 `.env`（内含 API key）。具体需提交的文件见 `GITHUB_SUBMISSION.md`。
