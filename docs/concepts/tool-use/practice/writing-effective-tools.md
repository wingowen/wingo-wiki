---
title: "用 Agent 为 Agent 编写高效工具 | Writing effective tools for agents"
created: 2025-09-11
updated: 2025-09-11
type: concept
tags: [agent, anthropic]
sources: ["raw/articles/writing-effective-tools.md"]
notion_id: 34267b21-8207-813f-9e2a-fe299323ddce
---

## 用 Agent 为 Agent 编写高效工具

> 原文：Writing effective tools for agents — with agents
> 作者：Ken Aizawa（Anthropic）
> 发布日期：2025-09-11

### 什么是工具？

工具是确定性系统与非确定性 Agent 之间的契约。传统软件（确定性）和 Agent（非确定性）的核心区别：给定相同输入，确定性系统每次产生相同输出，而 Agent 可能产生不同响应。

为 Agent 编写工具需要从根本上重新思考方法：不为其他开发者编写函数和 API，而是为 Agent 来设计工具。

---

### 核心要点

**选择正确的工具**
- 更多工具并不总是带来更好的结果
- 避免只包装现有软件功能或 API 端点的工具
- LLM Agent 的"上下文"有限，而计算机内存充足且便宜
- 构建少量精心设计的工具，针对特定高影响工作流

**为工具添加命名空间（Namespace）**
- MCP 服务器可能暴露数百个工具
- 按服务（asana_search、jira_search）或按资源（asana_projects_search、asana_users_search）添加命名空间
- 帮助 Agent 在正确的时间选择正确的工具

**从工具返回有意义的上下文**
- 优先返回高信号信息，而非低级技术标识符（UUID、mime_type）
- 使用 name、image_url、file_type 等语义字段
- 可通过 response_format 枚举参数控制详细程度（concise/detailed）
- 响应结构（XML、JSON、Markdown）会影响性能，需要根据评估选择

**优化工具响应的 Token 效率**
- 避免返回大量无关信息浪费上下文空间
- 提供 search_* 工具而非 list_* 工具，直接返回最相关结果
- Agent 在处理自然语言名称时比处理晦涩标识符更成功

---

### 编写和评估工具的工作流

1. **快速构建原型**：使用 Claude Code 编写工具，在本地 MCP 服务器或 DXT 中测试
2. **运行全面评估**：使用真实使用场景生成评估任务，让 Agent 分析结果并确定如何改进
3. **与 Agent 协作改进工具**：将评估记录拼接并让 Claude Code 分析和改进工具

## 相关链接

[tool-use](../core/tool-use.md) | [claude-code](../../entities/claude-code.md)