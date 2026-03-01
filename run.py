# -*- coding: utf-8 -*-
"""
FTEC5660 HW2 Part 2 — Run Moltbook Social Agent.
Usage (from part2/):
  pip install -r requirements.txt
  export MOLTBOOK_API_KEY=your_key   # or use .env
  python run.py
Logs written to logs/run.log.
"""

import os
import sys

# Ensure part2 is on path so "import config" and "from src.agent" work
PART2_DIR = os.path.dirname(os.path.abspath(__file__))
if PART2_DIR not in sys.path:
    sys.path.insert(0, PART2_DIR)

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PART2_DIR, ".env"))
except ImportError:
    pass

from config import LOGS_DIR
from src.agent import run_agent


def main():
    log_path = os.path.join(LOGS_DIR, "run.log")
    print("Log file:", log_path)
    run_agent(log_path=log_path)
    print("Done. Check Moltbook for upvote and comment.")


if __name__ == "__main__":
    main()
