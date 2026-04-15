---
title: "【面试专题】HyDE 假设文档嵌入与高级检索策略"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, hyde, interview, rag]
sources: []
notion_id: 34367b21-8207-818d-9eb8-fb9c821dbd20
---

## HyDE 假设文档嵌入与高级检索策略

> 难度：⭐⭐⭐⭐ | 面试频率：高 | 关联：👉 RAG 检索增强生成：从分块到检索 👉 上下文管理：短期记忆与长期记忆

---

### 一、HyDE 是什么？

HyDE（Hypothetical Document Embeddings，假设文档嵌入）是 Luyu Gao 等人于 2022 年提出的一种查询优化技术。核心思想是：不直接用用户的原始问题去检索，而是先让 LLM 生成一篇"假设的答案文档"，然后用这篇假答案的向量去检索真实知识库。

#### 1.1 解决什么问题？

用户的问题往往是简短、模糊、口语化的，而知识库中的文档是正式、详细、书面化的。这种"查询-文档"之间的语义鸿沟会导致检索质量下降。

举例：

  - 用户问："好玩吗？" → 向量与"好玩"接近，但知识库中是"该景区评分4.8分，游客反馈体验极佳"

  - HyDE：先让 LLM 生成假答案"这个景区非常好玩，有很多娱乐设施和自然景观" → 用这个假答案去检索 → 能匹配到真实文档

#### 1.2 HyDE 工作流程

```javascript
用户查询（"好玩吗"）
  ↓
[LLM 生成假设答案]
  → "这个景区非常好玩，有很多娱乐设施..."
  ↓
[对假设答案进行向量化]
  → embedding_vector
  ↓
[在向量数据库中检索]
  → 找到与假设答案最相似的真实文档
  ↓
[将真实文档注入 Prompt]
  ↓
[LLM 基于真实文档生成最终回答]
```

#### 1.3 代码实现

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()

# Step 1: 生成假设文档
hyde_prompt = ChatPromptTemplate.from_template(
    "请根据以下问题，写一段可能的答案（不需要完全准确，但要像真实文档一样详细）：\n\n问题：{question}\n\n答案："
)

hyde_chain = hyde_prompt | llm | StrOutputParser()

# Step 2: 用假设文档检索
def hyde_retriever(question: str, k: int = 5):
    # 生成假设答案
    hypothetical_doc = hyde_chain.invoke({"question": question})

    # 用假设答案的向量去检索
    results = vectorstore.similarity_search(hypothetical_doc, k=k)
    return results

# 使用
question = "这个景区好玩吗？"
docs = hyde_retriever(question)
```

---

### 二、HyDE 的适用场景与局限

#### 2.1 适用场景

#### 2.2 不适用场景

#### 2.3 HyDE 不是"反 RAG"

HyDE 是 RAG 的增强手段，不是替代。它优化的是 RAG 流程中的检索环节，目的是拉近查询与文档的语义距离。最终的回答仍然基于检索到的真实文档，而不是 LLM 生成的假答案。

---

### 三、其他高级检索策略

#### 3.1 Query Rewriting（查询重写）

将用户的原始查询改写为更适合检索的形式。

```python
rewrite_prompt = ChatPromptTemplate.from_template(
    "请将以下用户问题改写为一个更适合在知识库中检索的查询语句。"
    "保留核心意图，使用更正式、具体的表述：\n\n原始问题：{question}\n\n改写后："
)

rewrite_chain = rewrite_prompt | llm | StrOutputParser()

# "好玩吗" → "该景区有哪些娱乐设施和游客评价"
```

#### 3.2 RAG Fusion（多查询融合）

生成多个不同角度的查询，分别检索后合并去重。

```python
from langchain.retrievers import EnsembleRetriever

# 生成多个查询
multi_query_prompt = ChatPromptTemplate.from_template(
    "请根据以下问题，生成 3 个不同角度的检索查询：\n\n问题：{question}\n\n查询（每行一个）："
)

# 分别检索
queries = multi_query_chain.invoke({"question": question})
all_results = []
for q in queries:
    all_results.extend(vectorstore.similarity_search(q, k=3))

# 去重合并
unique_results = list({doc.page_content: doc for doc in all_results}.values())
```

#### 3.3 Reranker（重排序）

对初次检索的结果进行二次精排。

```python
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker

# 使用 Cross Encoder 进行精排
model = HuggingFaceCrossEncoder("BAAI/bge-reranker-large")
compressor = CrossEncoderReranker(model=model, top_n=3)

reranker = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
)

# 先检索 10 个，再精排到 3 个
results = reranker.invoke("如何预订机票？")
```

#### 3.4 策略对比

---

### 四、面试高频追问

#### Q: HyDE 和 Query Rewriting 有什么区别？

A: 目标相同（优化检索质量），但方式不同。Query Rewriting 是改写查询本身，使其更接近文档风格；HyDE 是生成一个假答案文档，用假答案的向量去检索。HyDE 通常比 Query Rewriting 效果更好（因为假答案比改写后的查询更接近真实文档），但成本也更高。

#### Q: 什么时候用 HyDE，什么时候不用？

A: 核心判断标准是查询-文档的语义距离。如果用户的查询已经足够精确和正式（如技术文档查询），直接检索即可。如果查询简短、模糊、口语化（如 C 端用户场景），使用 HyDE 能显著提升检索质量。也可以设计一个路由机制：根据查询长度和模糊度自动决定是否启用 HyDE。

#### Q: HyDE 会不会让 LLM 的"幻觉"污染检索结果？

A: 不会。因为 HyDE 生成的假答案只用于检索阶段（计算向量相似度），最终注入 Prompt 的是从知识库中检索到的真实文档。LLM 基于真实文档生成最终回答，假答案本身不会出现在最终输出中。

## 相关链接

[[hyde]] | [[interview-qa-overview]]
