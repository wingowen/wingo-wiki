---
title: "使用 Claude Agent SDK 构建 Agent | Building agents with the Claude Agent SDK"
created: 2025-09-29
updated: 2025-09-29
type: translation
tags: [agent, anthropic]
sources: []
notion_id: 34267b21-8207-8141-8638-c436b190d370
---

## 使用 Claude Agent SDK 构建 Agent

> 原文: Building agents with the Claude Agent SDK

> 作者: Thariq Shihipar（Anthropic）

> 发布日期: 2025-09-29

> 翻译日期: 2026-04-14

---

### 概述

Claude Agent SDK 是一组帮助开发者基于 Claude Code 构建强大 Agent 的工具集。Claude Code 最初是我们为支持 Anthropic 内部开发者生产力而构建的 Agent 编程解决方案，但如今它已远不止是一个编码工具——它几乎驱动了我们所有主要的 Agent 循环。

为了反映这一更广阔的愿景，我们将 Claude Code SDK 重命名为 Claude Agent SDK。

---

### 给 Claude 一台电脑

Claude Code 背后的核心设计原则是：Claude 需要和程序员每天使用的相同工具。它需要能够在代码库中查找文件、编写和编辑文件、lint 代码、运行、调试、编辑，有时需要迭代执行这些操作直到代码成功。

我们发现，通过让 Claude 访问用户的电脑（通过终端），它就拥有了像程序员一样编写代码所需的一切。

> 💡 核心洞察: 这也使 Claude 在非编码任务上同样有效。通过给它运行 bash 命令、编辑文件、创建文件和搜索文件的工具，Claude 可以读取 CSV 文件、搜索网页、构建可视化、解读指标——简而言之，创建具有电脑访问能力的通用 Agent。

---

### 创建新型 Agent

我们相信，给 Claude 一台电脑能够构建出比以前更有效的 Agent。例如：

  - 金融 Agent：理解你的投资组合和目标，通过访问外部 API、存储数据和运行代码进行计算来帮助评估投资

  - 个人助理 Agent：通过连接内部数据源和跨应用跟踪上下文，帮助预订旅行、管理日历、安排约会、整理简报

  - 客户支持 Agent：通过收集和审查用户数据、连接外部 API、回复用户消息、在需要时升级给人类，处理高模糊性的用户请求

  - 深度研究 Agent：通过搜索文件系统、分析和综合多源信息、交叉引用数据，对大型文档集合进行全面研究

---

### 构建 Agent 循环

在 Claude Code 中，Claude 通常在一个特定的反馈循环中运行：收集上下文 → 执行操作 → 验证工作 → 重复。

#### 收集上下文（Gather Context）

开发 Agent 时，你需要给它的不只是一个提示词——它需要能够获取和更新自己的上下文。

文件系统代表了可以被拉入模型上下文的信息。当 Claude 遇到大文件（如日志或用户上传的文件）时，它会使用 grep 和 tail 等 bash 脚本来决定如何加载这些内容。

> 💡 术语解释 - Context Engineering（上下文工程）:

> 文件夹和文件结构本身成为了一种上下文工程的形式。就像一个组织良好的办公室——文件按类别归档，需要时可以快速找到，而不是把所有东西堆在一起。

语义搜索通常比 Agent 搜索更快，但准确性较低、维护更困难、透明度也更低。它涉及将相关上下文"分块"、将这些块嵌入为向量，然后通过查询这些向量来搜索概念。

> 🔑 建议: 先从 Agent 搜索开始，只有在需要更快结果或更多变体时才添加语义搜索。

Claude Agent SDK 默认支持 Subagents。Subagents 有两个主要用途：

  1. 并行化：可以启动多个 Subagent 同时处理不同任务

  2. 上下文管理：Subagent 使用自己隔离的 Context Window，只将相关信息发送回编排者，而不是完整上下文

> 💡 举例说明:

> 就像一个研究团队——项目经理（编排者）把研究任务分配给多个研究员（Subagent），每个研究员独立工作后只提交精简的研究报告，而不是把所有原始数据都交给经理。

当 Agent 长时间运行时，上下文维护变得至关重要。Claude Agent SDK 的 compact 功能会在上下文接近限制时自动总结之前的消息，确保 Agent 不会耗尽上下文。

#### 执行操作（Take Action）

工具是 Agent 执行的主要构建模块。工具在 Claude 的 Context Window 中很突出，使其成为 Claude 在决定如何完成任务时考虑的主要操作。

> 🔑 建议: 你的工具应该是你希望 Agent 采取的主要操作。工具设计应最大化上下文效率。

Bash 作为通用工具，允许 Agent 使用电脑进行灵活工作。例如，Claude 可以编写代码来下载 PDF、转换为文本并搜索有用信息。

Claude Agent SDK 擅长代码生成——这是有充分理由的。代码是精确的、可组合的、无限可复用的，使其成为需要可靠执行复杂操作的 Agent 的理想输出。

> 💡 举例说明:

> Claude 最近在 Claude.AI 中推出的文件创建功能完全依赖代码生成——Claude 编写 Python 脚本来创建 Excel 电子表格、PowerPoint 演示文稿和 Word 文档，确保一致的格式和复杂的功能。

MCP 提供了与外部服务的标准化集成，自动处理认证和 API 调用。这意味着你可以将 Agent 连接到 Slack、GitHub、Google Drive 或 Asana 等工具，而无需编写自定义集成代码或管理 OAuth 流程。

> 💡 术语解释 - MCP（Model Context Protocol，模型上下文协议）:

> Anthropic 推出的开放标准，让 AI 模型能够以标准化方式连接外部工具和数据源。就像给 Agent 提供了一个"万能插头"，可以即插即用地接入各种服务。

#### 验证工作（Verify Your Work）

能够检查和改进自身输出的 Agent 本质上更可靠——它们在错误复合之前就能发现错误，在偏离时自我纠正，并在迭代中不断改进。

最好的反馈形式是为输出提供明确定义的规则，然后解释哪些规则失败以及为什么。

> 💡 举例说明:

> Code Linting 是基于规则的反馈的绝佳形式。例如，生成 TypeScript 并进行 lint 通常比生成纯 JavaScript 更好，因为它提供了多层额外的反馈。

当使用 Agent 完成视觉任务（如 UI 生成或测试）时，视觉反馈（截图或渲染）会很有帮助。例如，如果发送带有 HTML 格式的电子邮件，你可以截图生成的邮件并提供给模型进行视觉验证和迭代改进。

你可以让另一个语言模型基于模糊规则"评判"Agent 的输出。这通常不是非常稳健的方法，且有较重的延迟代价，但对于任何性能提升都值得付出成本的应用，它可能是有帮助的。

---

### 测试和改进你的 Agent

改进 Agent 的最佳方法是仔细查看其输出，特别是失败的情况，并设身处地地思考：

  - 如果 Agent 误解了任务，它可能缺少关键信息——你能改变搜索 API 的结构使其更容易找到所需信息吗？

  - 如果 Agent 反复在某项任务上失败，你能在工具调用中添加正式规则来识别和修复失败吗？

  - 如果 Agent 无法修复错误，你能给它更有用或更有创意的工具来以不同方式处理问题吗？

  - 如果 Agent 的性能随功能增加而变化，基于客户使用情况构建代表性测试集进行程序化评估

---

### 开始使用

Claude Agent SDK 通过让 Claude 访问一台可以编写文件、运行命令和迭代工作的电脑，使构建自主 Agent 变得更容易。

牢记 Agent 循环（收集上下文、执行操作、验证工作），你可以构建易于部署和迭代的可靠 Agent。

---

> 📝 译者注: 本文的核心框架是 Agent Loop（Agent 循环）= Gather Context → Take Action → Verify Work → Repeat。这个循环简洁而实用，可以作为设计任何 Agent 系统的参考模板。Claude Agent SDK 的关键设计理念是"给 Claude 一台电脑"——通过终端访问让 Agent 获得与人类程序员相同的工作环境。

## 相关链接

[[claude-code]] | [[anthropic]]
