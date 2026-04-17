---
title: "RAG 检索增强生成：从分块到检索 | RAG"
created: "2026-04-15"
updated: "2026-04-15T10:07:00.000Z"
type: concept
tags: [agent, interview, rag]
sources: ["raw/articles/rag.md"]
notion_id: "34367b21-8207-818e-a7de-d00cd93fab00"
---

> **难度**：⭐⭐⭐ | **面试频率**：高 | **关联**：[interview-hyde](../interview/interview-hyde.md) [context-management](../../context-engineering/core/context-management.md)

---

# RAG 检索增强生成

## 核心流程

用户查询 → 编码查询 → 向量检索 → 文档排序 → 注入 Prompt → LLM 生成回答

## 文档分块策略

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| 固定长度 | 按 token/字符数切分 | 通用场景 |
| 语义切分 | 按段落、句子边界切分 | 保留语义完整 |
| 递归切分 | 按层级递归切分 | 复杂文档结构 |
| 重叠切分 | 相邻块之间有重叠 | 减少上下文丢失 |

**chunk_size 经验值**：500 tokens（大多数场景），800-1000 tokens（复杂技术文档），200-300 tokens（代码）。

## 向量检索要点

- **Embedding 模型**：OpenAI text-embedding-3-small 或本地 BGE
- **向量数据库**：Chroma（开发）、Milvus/Pinecone（生产）
- **Top-K 检索**：基础检索 + 分数阈值过滤 + MMR 多样性检索

## 面试要点

**Q: 如何选择 chunk_size？**
A: 平衡完整性和相关性。过小导致碎片化，过大引入噪声。

**Q: 向量检索分数的意义？**
A: 不同模型/维度/算法的分数不可比较。使用相对排序或实验确定阈值。

**Q: 如何处理超大文档？**
A: 层级检索（粗粒度→细粒度）、摘要增强检索、HyDE 等方案。

## 相关链接

[contextual-retrieval](contextual-retrieval.md) | [hyde](hyde.md)
