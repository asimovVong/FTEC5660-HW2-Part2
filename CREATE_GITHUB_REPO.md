# 创建 GitHub 仓库并推送 Part 2 提交

本地 Git 已初始化并完成首次提交。按下面步骤在 GitHub 上创建**公开仓库**并推送代码。

---

## 步骤 1：在 GitHub 上新建仓库

1. 打开 https://github.com/new  
2. **Repository name**：例如 `FTEC5660-HW02-Part2` 或 `moltbook-agent`  
3. **Public**  
4. **不要**勾选 “Add a README” / “Initialize with .gitignore”（本地已有）  
5. 点击 **Create repository**

---

## 步骤 2：关联远程并推送

在终端执行（把 `YOUR_USERNAME` 和 `YOUR_REPO` 换成你的 GitHub 用户名和仓库名）：

```bash
cd /Users/asimov/project/5660/hw2/part2
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

若使用 SSH：

```bash
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## 步骤 3：提交 report.pdf（您需要自行完成）

1. 将 `report/report.md` 导出为 **report.pdf**（≤4 页），并在报告中加入 Moltbook 截图（见 report.md 内说明）。  
2. 把 **report.pdf** 放到 `part2/report/` 或仓库根目录。  
3. 在 part2 目录执行：

```bash
git add report/report.pdf
git commit -m "Add report.pdf"
git push
```

---

## 已提交到本地的文件（当前 commit）

- 源代码：config.py, run.py, moltbook_agent.py, src/, requirements.txt, .env.example 等  
- 报告正文：report/report.md, report/report_template.md  
- 说明与清单：README.md, GITHUB_SUBMISSION.md, REPORT_OUTLINE_PART2.md  
- 运行日志：logs/run.log  
- **未**提交：.env（已由 .gitignore 排除）

**您仍需**：导出 report.pdf、加入截图、将 report.pdf 加入仓库并 push。
