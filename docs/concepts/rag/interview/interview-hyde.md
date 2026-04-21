---
title: "【面试专题】HyDE 假设文档嵌入与高级检索策略"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, hyde, interview, rag]
sources: ["raw/articles/interview-hyde.md"]
notion_id: 34367b21-8207-818d-9eb8-fb9c821dbd20
---

## HyDE 假设文档嵌入与高级检索策略

> 难度：⭐⭐⭐⭐ | 面试频率：高 | 关联：👉 RAG 检索增强生成：从分块到检索 👉 上下文管理：短期记忆与长期记忆

---

### 核心定义

HyDE（Hypothetical Document Embeddings，假设文档嵌入）：不直接用用户原始问题检索，而是先让 LLM 生成"假设答案文档"，用假答案的向量检索真实知识库。

**解决的核心问题**：用户查询（简短模糊、口语化）与知识库文档（正式详细、书面化）之间的语义鸿沟。

### 工作流程

用户查询 → LLM 生成假设答案 → 向量化假设答案 → 向量数据库检索 → 注入真实文档 → LLM 生成最终回答

### 面试要点

**Q: HyDE 和 Query Rewriting 有什么区别？**
A: 目标相同但方式不同。Query Rewriting 改写查询本身；HyDE 生成假答案文档，用假答案向量检索。HyDE 效果更好但成本更高。

**Q: 什么时候用 HyDE？**
A: 查询简短模糊、口语化时（如 C 端用户场景）效果显著。查询已足够精确（技术文档）直接检索即可。可设计路由机制根据查询特性自动决定。

**Q: HyDE 会不会让"幻觉"污染检索结果？**
A: 不会。假答案仅用于检索阶段（计算向量相似度），最终 Prompt 注入的是真实文档。

## 相关链接

[hyde](../core/hyde.md) | [interview-qa-overview](../../../queries/interview-qa-overview.md)
