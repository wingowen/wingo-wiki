---
title: "RAG 检索增强生成：从分块到检索"
created: "2026-04-15"
updated: "2026-04-15T10:07:00.000Z"
type: concept
tags: [agent, interview, rag]
sources: ["notion:34367b21-8207-818e-a7de-d00cd93fab00"]
notion_id: "34367b21-8207-818e-a7de-d00cd93fab00"
---

> **难度**：⭐⭐⭐ | **面试频率**：高 | **关联**：[[interview-hyde]] [[context-management]]

---

# RAG 检索增强生成：从分块到检索

## 一、RAG 核心流程

```javascript
用户查询 → 编码查询 → 向量检索 → 文档排序 → 注入Prompt → LLM生成回答
     ↑                                                    ↓
     ←←←←←←←←←←←←←←← 检索结果 ←←←←←←←←←←←←←←←←←←←←←←←←←
```

---

## 二、文档分块（Chunking）

### 2.1 分块策略

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| 固定长度 | 按 token/字符数切分 | 通用场景 |
| 语义切分 | 按段落、句子边界切分 | 保留语义完整 |
| 递归切分 | 按层级递归切分 | 复杂文档结构 |
| 重叠切分 | 相邻块之间有重叠 | 减少上下文丢失 |

### 2.2 分块参数

```python
chunk_size = 500      # 每块 token 数
chunk_overlap = 50    # 重叠 token 数
separators = ["\n\n", "\n", ". ", "?"]  # 分割符优先级
```

### 2.3 语义切分代码

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", "?"],
    length_function=len
)

docs = text_splitter.split_text(long_document)
```

---

## 三、向量检索

### 3.1 Embedding 模型选择

```python
from langchain_openai import OpenAIEmbeddings

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 本地 Embeddings（如 BGE）
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-large-zh",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)
```

### 3.2 向量数据库

```python
from langchain_community.vectorstores import Chroma, Milvus, Pinecone

# Chroma（本地开发）
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Milvus（生产环境）
vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=embeddings,
    connection_args={"host": "localhost", "port": "19530"}
)
```

### 3.3 Top-K 检索

```python
# 基础检索
results = vectorstore.similarity_search(query="用户问题", k=5)

# 带分数阈值
results = vectorstore.similarity_search_with_score(
    query="用户问题",
    k=5,
    score_threshold=0.7  # 只返回相似度 > 0.7 的结果
)

# MMR（最大边际相关）检索
results = vectorstore.max_marginal_relevance_search(
    query="用户问题",
    k=5,
    fetch_k=20,  # 初始检索 20 个，再精选 5 个
    lambda_mult=0.5  # 多样性权重
)
```

---

## 四、超大文件处理

### 4.1 问题

单个文档可能超过 LLM 的 Context Window 或单次 embedding 上限。

### 4.2 解决方案

```python
# 方案一：层级检索
# L1: 按章节/页面粗粒度检索
# L2: 在选中章节内细粒度检索

# 方案二：摘要增强检索
from langchain.chains.summarize import load_summarize_chain

# 先对文档生成摘要，用摘要匹配
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
summary = summary_chain.run(docs)

# 方案三：HyDE（参考 HyDE 页面）
```

---

## 五、面试高频追问

### Q: 如何选择合适的 chunk_size？

A: 需要平衡**完整性**和**相关性**。过小会导致上下文碎片化，过大会引入噪声。经验值：500 tokens 适合大多数场景；复杂技术文档可用 800-1000 tokens；代码相关文档建议更小（200-300 tokens）。

### Q: 向量检索的分数没有意义？

A: 不同 embedding 模型、不同维度、不同相似度算法（cosine/dot product）的分数不可比较。生产环境中建议使用**相对排序**而非绝对分数，或通过实验确定阈值。

### Q: 如何处理多模态文档（PDF、图片）？

A: 1）PDF：先用 PyMuPDF 提取文本，按上述策略分块；2）图片：使用 OCR（pytesseract）或 Multimodal Embeddings（如 CLIP）提取特征；3）表格：可用 table-transformers 提取结构化数据。

## 相关链接

[[contextual-retrieval]] | [[hyde]]
