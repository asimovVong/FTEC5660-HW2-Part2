# FTEC5660 Homework 02 (Part 2) — Moltbook Social Agent

Autonomous agent that: **authenticates** with Moltbook API → **subscribes** to `/m/ftec5660` → **upvotes and comments** on the assigned post.

## Submission (per assignment)

- **Report:** `report.pdf` (max 4 pages): agent design/architecture, decision logic & autonomy, screenshots or logs of Moltbook interactions.
- **Source:** this folder (`.py` or `.ipynb`).
- **Repo:** Public GitHub repository.

## Quick run

```bash
cd hw2
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements_part2.txt
cp .env.example .env
# Edit .env: set MOLTBOOK_API_KEY and optionally STUDENT_ID
python moltbook_agent.py
```

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `MOLTBOOK_API_KEY` | Yes | API key from [Moltbook](https://www.moltbook.com) after agent registration (Colab or `agents/register`). |
| `AGENT_NAME_PREFIX` | No | Prefix for agent name (default `nickname`). Full name = `prefix_XXXX`, e.g. `huangzixun_68498644`. |
| `STUDENT_ID` | No | Your student ID; XXXX = encoded via Colab `encode_student_id`. |

## Agent naming

- Format: **prefix_XXXX** (e.g. huangzixun_68498644). Set `AGENT_NAME_PREFIX` in .env; XXXX = encoded student ID from Colab `encode_student_id()`.
- Comment text includes “我是 prefix_XXXX” for TA identification.

## Outputs

- **Logs:** `logs/run.log` — HTTP method/URL/status and step results (for report screenshots).

## API reference

Agent behaviour follows [Moltbook skill.md](https://www.moltbook.com/skill.md): auth (`GET /agents/me`), subscribe (`POST /submolts/ftec5660/subscribe`), upvote (`POST /posts/<id>/upvote`), comment (`POST /posts/<id>/comments`).
