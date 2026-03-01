# FTEC5660 Homework 02 (Part 2) — Moltbook Social Agent

**Student ID:** 1155244509  
**Agent name:** huangzixun_68498644 (format: nickname_XXXX)  
**GitHub repository:** https://github.com/asimovVong/FTEC5660-HW2-Part2

Autonomous agent that (1) authenticates with the Moltbook API, (2) subscribes to `/m/ftec5660`, and (3) upvotes and comments on the specified post:  
https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c

API reference: [Moltbook skill.md](https://www.moltbook.com/skill.md)

---

## Setup and run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

- **MOLTBOOK_API_KEY** (required) — from [Moltbook](https://www.moltbook.com) after agent registration.
- **AGENT_NAME_PREFIX** (optional) — e.g. `huangzixun`; full name = `prefix_XXXX` with encoded student ID.
- **STUDENT_ID** (optional) — used to compute XXXX via Colab `encode_student_id()`.

Then run:

```bash
python run.py
```

Or the single-file entry point:

```bash
python moltbook_agent.py
```

Logs are written to `logs/run.log`.

---

## Submission (per assignment)

- **report.pdf** — max 4 pages (agent design, decision logic, screenshots or logs).
- **Source code** — this repository (`.py` and supporting files).
- **Public GitHub repo** — https://github.com/asimovVong/FTEC5660-HW2-Part2
