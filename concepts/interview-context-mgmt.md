---
title: "【面试专题】上下文管理：短期记忆与长期记忆"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, interview, memory, rag]
sources: ["raw/articles/interview-context-mgmt.md"]
notion_id: 34367b21-8207-81c6-8eed-f5368d5630dd
---

## 上下文管理：短期记忆与长期记忆

> 难度：⭐⭐⭐⭐ | 面试频率：极高 | 关联：👉 LangGraph 核心原理与 ReAct 对比 👉 RAG 检索增强生成：从分块到检索

---

### 为什么上下文管理是 Agent 的核心？

LLM 的 Context Window 是有限的（如 GPT-4o 为 128K tokens，Claude 为 200K tokens）。Agent 在运行过程中会不断累积消息，如果不加管理，很快就会超出窗口限制。

上下文管理的核心目标：**在有限的窗口内，让 Agent 拥有尽可能多的有效信息**。

---

### 核心要点

**短期记忆（Short-term Memory）**
- 当前会话/任务中的上下文信息，存储在 messages 列表中
- LangGraph 通过 Checkpointer（SQLite/PostgreSQL）实现状态持久化
- 通过 thread_id 实现会话隔离，跨请求恢复状态

**消息裁剪策略**
- 按 Token 数量裁剪（保留 System Prompt）
- 摘要化旧消息：用 LLM 将旧消息压缩为一条摘要
- 保留最近 N 轮原文不摘要，避免关键信息丢失

**长期记忆（Long-term Memory）**
- 跨会话、跨任务持久化存储（用户偏好、历史行为、知识库）
- 实现方案：向量数据库（语义检索）、关系数据库（结构化数据）、Redis（热数据缓存）

**应用模式**：检索 → 注入 System Prompt → Agent 推理 → 更新长期记忆

---

### 面试高频追问

**Q: Checkpointer 和普通数据库存储的区别？**
A: Checkpointer 保存图的完整状态（含所有节点中间结果），支持时间旅行；普通数据库存业务数据。两者互补。

**Q: 如何解决高并发下的上下文隔离？**
A: 通过 thread_id 实现逻辑隔离，配合 PostgreSQL 作为 Checkpointer 后端。

**Q: Context Window 溢出时 Agent 会怎样？**
A: API 调用失败（HTTP 400）。预防：计算 token 数、设置安全阈值、触发裁剪策略。

## 相关链接

[[context-management]] | [[interview-qa-overview]]