---
title: "AI Agent 的有效上下文工程 | Effective context engineering for AI agents"
created: 2025-09-29
updated: 2025-09-29
type: concept
tags: [agent, anthropic]
sources: ["raw/articles/effective-context-engineering.md"]
notion_id: 34267b21-8207-8199-9743-c072860e6ac1
---

## AI Agent 的有效上下文工程

> 原文：Anthropic Engineering | 发布日期：2025-09-29

---

### 核心概念

**Context（上下文）** = LLM 采样时包含的所有 Token 集合

**Context Engineering** = 在 LLM 固有约束下优化 Token 效用的策略，包括提示词、工具、示例、消息历史等。

### Context Rot（上下文衰减）

随着上下文窗口 Token 数量增加，模型准确回忆信息的能力下降。n² 的注意力关系意味着上下文越长，模型对单个信息的注意力越分散。

**注意力预算**：每个新 Token 都消耗一部分预算，需要精心策展。

### 上下文组件设计原则

**系统提示词**：足够具体以引导行为，又足够灵活提供启发式指导。避免 if-else 硬编码，也避免过于模糊。

**工具**：功能重叠最小、自包含、对错误鲁棒。最小可行工具集，避免臃肿的工具集。

**Few-shot 示例**：多样化、规范的示例集，描绘期望行为，而非堆砌边缘情况。

### 长期任务策略

1. **Compaction（压缩）**：接近上下文限制时摘要内容，用摘要重启新上下文
2. **结构化笔记**：Agent 定期将笔记持久化到外部记忆
3. **多 Agent 架构**：子 Agent 在干净上下文中处理聚焦任务，主 Agent 综合精简摘要

### 核心原则

**找到尽可能最小的、高信号 Token 集合，以最大化实现期望结果的可能性。**

## 相关链接

[context-engineering](../core/context-engineering.md)
