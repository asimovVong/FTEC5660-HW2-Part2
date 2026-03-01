# Part 2 提交到 GitHub 的文件清单

按作业要求：创建 **公开 GitHub 仓库**，上传 **report.pdf** 与 **源代码**（.ipynb 或 .py）。

---

## 需要提交的文件（请全部放入仓库）

### 必须

| 文件或目录 | 说明 |
|------------|------|
| **report.pdf** | 由 `report/report.md` 导出（≤4 页），需**您自行导出为 PDF** 后放入仓库根目录或 `report/`。 |
| **config.py** | 配置（API base、submolt、post ID、agent 命名）。 |
| **run.py** | 入口脚本。 |
| **moltbook_agent.py** | 单文件版 agent。 |
| **requirements.txt** | 依赖（或 requirements_part2.txt）。 |
| **.env.example** | 环境变量示例（**不要**提交 `.env`）。 |
| **src/__init__.py** | |
| **src/agent.py** | 状态机与执行逻辑。 |
| **src/moltbook_tools.py** | Moltbook REST 工具封装。 |
| **README.md** | 运行与提交说明。 |

### 可选（有助于复现与评分）

| 文件或目录 | 说明 |
|------------|------|
| **logs/run.log** | 运行日志（可脱敏后提交，或保留以证明运行成功）。 |
| **report/report.md** | 报告正文（导出 PDF 前可修改）。 |
| **report/report_template.md** | 报告模板。 |
| **REPORT_OUTLINE_PART2.md** | 报告提纲。 |
| **README_PART2.md** | Part 2 英文说明。 |
| **Moltbook.py** / **Moltbook.ipynb** | Colab 导出的 starter。 |
| **requirements_part2.txt** | 与 requirements.txt 二选一或同时保留。 |

---

## 一定不要提交

| 项 | 原因 |
|----|------|
| **.env** | 内含 MOLTBOOK_API_KEY，不能泄露。 |
| **__pycache__/** 、 **.venv/** | 本地缓存与虚拟环境。 |

已通过 `.gitignore` 排除上述项（见仓库根目录 `.gitignore`）。

---

## 您需要自行完成（中文）

1. **导出 report.pdf**：将 `report/report.md` 转为 PDF（≤4 页），并在第 3 节加入 Moltbook 截图（见 report.md 内说明）。
2. **确认 .env 未提交**：首次 push 前执行 `git status`，确保没有 `.env`。
3. **创建并推送仓库**：若未使用下面自动创建的仓库，可本地 `git init` 后添加 remote 并 push，或使用 GitHub 网页 “Upload files” 上传上述文件。
