---
title: "介绍上下文检索 | Introducing Contextual Retrieval"
created: 2024-09-19
updated: 2024-09-19
type: concept
tags: [anthropic, rag]
sources: ["raw/articles/contextual-retrieval.md"]
notion_id: 34267b21-8207-813f-b0e2-cae2d942f74c
---

## 介绍上下文检索 | Introducing Contextual Retrieval

> 原文：Introducing Contextual Retrieval
> 作者：Anthropic Engineering Team
> 发布日期：2024-09-19

### 什么是上下文检索？

传统 RAG 在编码信息时会丢失上下文，导致检索系统无法找到相关信息。上下文检索（Contextual Retrieval）通过两个子技术解决这一问题：

- **上下文嵌入（Contextual Embeddings）**：为每个文本块添加特定于该块的解释性上下文
- **上下文 BM25（Contextual BM25）**：在创建 BM25 索引时使用上下文化后的文本块

效果：将检索失败率降低 49%，结合 Reranking 后可降低 67%。

---

### 核心要点

**工作原理**

```python
original_chunk = "The company's revenue grew by 3% over the previous quarter."
contextualized_chunk = "This chunk is from an SEC filing on ACME corp's performance in Q2 2023; the previous quarter's revenue was $314 million. The company's revenue grew by 3% over the previous quarter."
```

使用 Claude 为每个文本块生成 50-100 token 的上下文说明，然后进行嵌入和索引。

**实现注意事项**
- 分块边界选择影响检索性能
- 某些嵌入模型（如 Gemini、Voyage）效果特别好
- 向上下文窗口传递 20 个文本块比 10 个或 5 个更有效

**结合 Reranking**
1. 执行初始检索获取排名前 150 的候选块
2. 使用 Reranking 模型重新评分
3. 选择排名前 20 的块传递给生成模型

**成本优化**
使用 Prompt Caching，只将文档加载到缓存一次，每个文本块的处理成本约为每百万文档 token $1.02。

---

### 结论

上下文检索的核心洞察：在嵌入前为每个文本块添加解释性上下文，可以显著提升检索质量。结合嵌入和 BM25、使用 Reranking、传递更多候选块，所有这些优势可以叠加。

## 相关链接

[[rag]] | [[hyde]]