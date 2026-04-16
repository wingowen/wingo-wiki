---
title: "上下文管理：短期记忆与长期记忆"
created: "2026-04-15"
updated: "2026-04-15T10:08:00.000Z"
type: concept
tags: [agent, interview, memory, rag]
sources: [raw/articles/context-management.md]
notion_id: "34367b21-8207-81c6-8eed-f5368d5630dd"
---

## 上下文管理：短期记忆与长期记忆

上下文管理是 Agent 的核心能力。LLM 的 Context Window 有限（GPT-4o 128K，Claude 200K tokens），Agent 运行中会不断累积消息，必须通过管理策略在有限窗口内塞入最多有效信息。

短期记忆管理当前会话/任务中的上下文，通常存储在 messages 列表中。LangGraph 通过 Checkpointer 实现状态持久化，thread_id 实现会话隔离。消息过多时需裁剪，策略包括滑动窗口（保留最近 N 轮）、Token 计数裁剪和摘要化（LLM 压缩历史）。

## 核心要点

- **短期记忆**：当前会话上下文，messages 列表累积，需裁剪防止溢出
- **Checkpointer**：LangGraph 状态快照机制，支持时间旅行，thread_id 实现会话隔离
- **裁剪策略**：滑动窗口（简单但可能丢失中间信息）、Token 计数（保留 System Prompt）、摘要化（LLM 压缩但可能丢失细节）
- **长期记忆**：跨会话持久化，存储用户偏好、历史行为、知识库
- **向量数据库**：推荐方案，存储历史交互的向量化表示，支持语义检索

## 相关链接

[[langgraph]] | [[rag]]
