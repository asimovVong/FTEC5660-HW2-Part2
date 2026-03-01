# FTEC5660 Homework 02 — Part 2: Moltbook Social Agent

**Student ID:** 1155244509  
**Agent name (encoded):** `huangzixun_68498644`（格式：prefix_XXXX）

## 任务 (Task)

Agent 需完成：

1. 使用 API key 认证 (Authenticate)
2. 订阅 `/m/ftec5660` (Subscribe)
3. 对指定帖子 Upvote + Comment  
   - 帖子 URL: https://www.moltbook.com/post/47ff50f3-8255-4dee-87f4-2c3637c7351c

API 说明见：https://www.moltbook.com/skill.md

## 先注册 Agent（取得 API Key）

在 Moltbook 上用 **agent 名称** `huangzixun_68498644` 注册一次（Colab 或本地执行一次即可）：

```bash
curl -X POST https://www.moltbook.com/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "huangzixun_68498644", "description": "FTEC5660 HW2 Part2 Social Agent"}'
```

响应中的 `api_key` 保存到环境变量或 `.env`；按邮件/claim_url 完成 claim 后即可用该 key 调用 API。

## 运行 (Run)

```bash
cd part2
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

配置 API Key（二选一）：

- 环境变量：`export MOLTBOOK_API_KEY=你的key`
- 或复制 `.env.example` 为 `.env` 并填入 `MOLTBOOK_API_KEY=...`

执行：

```bash
python run.py
```

运行日志写入 `logs/run.log`，可用于 report 截图/证据。

## 提交 (Submission)

- **report.pdf**（最多 4 页）：Agent 设计、决策逻辑、自治程度、Moltbook 操作截图或日志
- **源代码**：本目录下的 `.py` 文件（或 .ipynb）
- **GitHub**：公开仓库，按要求上传上述文件

## 目录结构

```
part2/
├── config.py              # 配置：BASE_URL, submolt, post URL, 学号编码与 agent 名
├── run.py                 # 入口：加载 .env，调用 agent，写日志（推荐）
├── moltbook_agent.py      # 单文件版 agent，可直接 python moltbook_agent.py
├── requirements.txt       # 依赖（同 requirements_part2.txt）
├── .env.example
├── Moltbook.py            # Colab 导出的 starter（参考）
├── Moltbook.ipynb         # Colab 原始 notebook
├── README_PART2.md        # Part 2 英文说明
├── REPORT_OUTLINE_PART2.md # report 提纲（写 report.pdf 用）
├── src/
│   ├── __init__.py
│   ├── moltbook_tools.py   # REST 封装：me, subscribe, get_post, upvote, comment
│   └── agent.py            # 状态机执行：AUTH → SUBSCRIBE → UPVOTE → COMMENT → DONE
├── logs/
│   └── run.log             # 运行日志（运行后生成）
└── report/                 # 存放 report 素材（截图、日志片段）
```

## Agent 命名

命名格式为 **prefix_XXXX**（下划线），XXXX 为 Colab 中 `encode_student_id(1155244509) = "68498644"`。本例为 **huangzixun_68498644**。Comment 中会包含「我是 huangzixun_68498644」以便助教识别。在 `.env` 中设置 `AGENT_NAME_PREFIX=huangzixun` 与注册名一致。
