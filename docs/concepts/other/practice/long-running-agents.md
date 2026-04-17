---
title: "构建长时间运行 Agent 的有效 Harness | Long Running Agents"
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anthropic]
sources: ["raw/articles/long-running-agents.md"]
notion_id: 34267b21-8207-8131-929e-fb39d34023b5
---

## 构建长时间运行 Agent 的有效 Harness

> 原文: Effective Harnesses for Long-Running Agents
> 作者: Justin Young（Anthropic 工程团队）
> 发布日期: 2025-11-26

### 核心挑战

长时间运行 Agent 的核心挑战在于：它们必须在离散的会话中工作，而每个新会话开始时对之前发生的事情没有任何记忆。Context Window 是有限的，而大多数复杂项目无法在单个窗口内完成。

### 解决方案：双重 Agent 架构

1. **Initializer Agent（初始化 Agent）**：首次运行时设置环境（init.sh 脚本、进度日志文件、git commit）
2. **Coding Agent（编码 Agent）**：每个会话中逐步推进，会话结束时保持环境干净状态（Clean State）

---

### 核心要点

**避免 Agent 一次性做太多事**
- Agent 倾向于"一枪搞定"整个应用，导致功能实现一半且没有文档记录
- 解决：要求每次只处理一个功能（增量推进）

**使用结构化文件（JSON > Markdown）跟踪功能状态**
- Feature List 文件最初全部标记为"passes: false"
- Coding Agent 只能通过更改 passes 字段来编辑文件

**每个会话结束时保持代码干净**
- 要求将进展提交到 git（附带描述性 commit message）
- 在进度文件（claude-progress.txt）中写入进展摘要
- 使用 git 来回退错误的代码更改并恢复代码库状态

**端到端测试不可或缺**
- 仅靠单元测试不够，需要像真实用户一样测试
- 使用 Browser Automation（Puppeteer）进行端到端验证

---

### 关键要点总结

1. **不要让 Agent 一次性做太多事** —— 增量推进是关键
2. **使用结构化文件（JSON > Markdown）** 来跟踪功能状态
3. **每个会话结束时保持代码干净** —— 就像优秀的工程师每天下班前做的那样
4. **使用 git 作为 Agent 的"记忆"** —— commit message + 进度文件
5. **端到端测试不可或缺** —— 仅靠单元测试不够
6. **Initializer Agent 和 Coding Agent 分工明确** —— 一个搭台，一个唱戏

## 相关链接

[tool-use](../../tool-use/core/tool-use.md)