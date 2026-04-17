---
title: "Context Engineering | 上下文工程"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, architecture]
sources: []
---

# Context Engineering

## Overview

Context Engineering 是 Anthropic 提出的概念，指系统性地设计和管理 AI 系统的上下文输入，以优化模型表现。

## 核心要素

- **System Prompt**: 定义 Agent 角色和行为
- **User Input**: 任务描述和约束
- **Retrieved Context**: 从外部知识库检索的相关信息
- **Conversation History**: 多轮交互的记忆

## 上下文管理策略

1. **短期记忆**: 当前对话窗口内的信息
2. **长期记忆**: 持久化存储的用户偏好和历史
3. **检索增强**: 动态从外部源获取相关信息

## 相关链接

[[dual-memory-system]] | [[effective-context-engineering]] | [[rag]]
