---
title: "HyDE 假设文档嵌入与高级检索策略 | HyDE"
created: "2026-04-15"
updated: "2026-04-15T10:08:00.000Z"
type: concept
tags: [agent, hyde, interview, rag]
sources: ["raw/articles/hyde.md"]
notion_id: "34367b21-8207-818d-9eb8-fb9c821dbd20"
---

> **难度**：⭐⭐⭐⭐ | **面试频率**：高 | **关联**：[rag](rag.md) [context-management](../../context-engineering/core/context-management.md)

---

# HyDE 假设文档嵌入与高级检索策略

## 核心概念

HyDE（Hypothetical Document Embeddings）是 Luyu Gao 等人于 2022 年提出的查询优化技术。核心思想：**不直接用用户的原始问题去检索，而是先让 LLM 生成一篇"假设的答案文档"，然后用这篇假答案的向量去检索真实知识库。**

解决的是用户查询（简短、模糊、口语化）与知识库文档（正式、详细、书面化）之间的**语义鸿沟**问题。

## 工作流程

用户查询 → LLM 生成假设答案 → 对假设答案向量化 → 向量数据库检索 → 注入真实文档到 Prompt → LLM 生成最终回答

**注意**：假答案只用于检索阶段，最终回答基于真实文档，不会被"幻觉"污染。

## 适用场景

| 场景 | 说明 |
|------|------|
| 查询简短模糊 | "好玩吗"、"怎么办" |
| 口语化表达 | 口语与书面语差异大 |
| 零样本检索 | 无明确关键词可匹配 |

**不适用**：查询已足够精确（如技术文档）、高度领域专用、实时性要求高（额外 LLM 调用）。

## 高级检索策略对比

| 策略 | 原理 | 优势 | 劣势 |
|------|------|------|------|
| Query Rewriting | 改写查询本身 | 成本低 | 效果有限 |
| **HyDE** | 生成假答案检索 | 效果最好 | 多一次 LLM 调用 |
| RAG Fusion | 多查询融合 | 覆盖全面 | 检索量大 |
| Reranker | 二次精排 | 精度高 | 需要额外模型 |

## 相关链接

[contextual-retrieval](contextual-retrieval.md)
