---
title: "【面试专题】RAG 检索增强生成：从分块到检索"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, interview, rag]
sources: []
notion_id: 34367b21-8207-818e-a7de-d00cd93fab00
---

## RAG 检索增强生成：从分块到检索

> 难度：⭐⭐⭐⭐ | 面试频率：极高 | 关联：👉 上下文管理：短期记忆与长期记忆 👉 HyDE 假设文档嵌入与高级检索策略

---

### 一、RAG 是什么？

RAG（Retrieval-Augmented Generation，检索增强生成）是一种将外部知识检索与 LLM 生成结合的技术架构。核心思想是：不让 LLM "凭空想象"，而是先从知识库中检索相关信息，再基于检索结果生成回答。

#### 1.1 为什么需要 RAG？

#### 1.2 RAG 的基本流程

```javascript
用户提问 → 查询向量化 → 向量数据库检索 Top-K 文档片段 → 将检索结果注入 Prompt → LLM 生成回答
```

---

### 二、文档分块（Chunking）策略

分块是 RAG 的第一步，也是影响检索质量的关键环节。

#### 2.1 为什么需要分块？

  - LLM 的 Context Window 有限，无法一次性加载整个文档

  - 向量检索是基于语义相似度的，粒度太粗（整篇文档）会导致检索不精准

  - 分块后可以实现细粒度检索，只返回最相关的片段

#### 2.2 分块策略对比

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 每块最大 500 字符
    chunk_overlap=50,    # 块间重叠 50 字符
    separators=["\n\n", "\n", "。", ".", " ", ""]
)
chunks = splitter.split_text(long_document)
```

优点：简单、可控

缺点：可能在句子中间截断，破坏语义完整性

```python
from langchain.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# 基于语义相似度动态切分
splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95
)
chunks = splitter.split_text(long_document)
```

原理：计算相邻句子的嵌入向量相似度，当相似度低于阈值时在此处切分。

优点：保持语义完整性

缺点：计算成本高（需要对每个句子计算嵌入）

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

# 按 Markdown 标题层级分块
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
)
chunks = splitter.split_text(markdown_document)
```

优点：保留文档结构信息

缺点：仅适用于结构化文档

#### 2.3 分块参数调优

---

### 三、向量存储与检索

#### 3.1 Embedding（嵌入）

将文本转换为高维向量（如 1536 维），语义相似的文本在向量空间中距离更近。

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector = embeddings.embed_query("什么是人工智能？")
# 输出：[0.0023, -0.0145, 0.0321, ...] (1536维)
```

#### 3.2 向量数据库选择

#### 3.3 Top-K 检索

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 检索与问题最相关的 5 个文档片段
results = vectorstore.similarity_search("如何预订机票？", k=5)

for doc in results:
    print(f"相似度分数: {doc.metadata['score']}")
    print(f"内容: {doc.page_content[:100]}...")
```

---

### 四、超大文件处理

#### 4.1 问题挑战

  - 文件可能达到数十MB甚至数GB

  - 无法一次性加载到内存

  - 直接分块会丢失文档的整体结构

#### 4.2 解决方案

```python
def process_large_file(file_path: str, chunk_size: int = 1000):
    """流式读取大文件并分块"""
    buffer = ""
    chunks = []

    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                if buffer:
                    chunks.append(buffer)
                break
            buffer += line
            if len(buffer) >= chunk_size:
                # 在段落边界处切分
                split_point = buffer.rfind('\n\n')
                if split_point == -1:
                    split_point = buffer.rfind('\n')
                if split_point == -1:
                    split_point = chunk_size

                chunks.append(buffer[:split_point])
                buffer = buffer[split_point:]

    return chunks
```

```javascript
文档 → 父块（大块，用于上下文）→ 子块（小块，用于精准检索）

检索流程：
1. 在子块中检索 Top-K
2. 获取这些子块对应的父块
3. 将父块（包含更多上下文）注入 Prompt
```

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# 子块用于检索（小块）
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)
# 父块用于上下文（大块）
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=InMemoryStore(),
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
```

```javascript
Map 阶段：将文档分块，每块独立检索
Reduce 阶段：合并各块的检索结果，去重排序
```

---

### 五、RAG 评估指标

---

### 六、面试高频追问

#### Q: chunk_size 和 chunk_overlap 如何选择？

A: 没有万能值，取决于场景。一般建议：chunk_size 300-1000 tokens，overlap 为 chunk_size 的 10-20%。QA 场景用小 chunk（300-500），摘要场景用大 chunk（800-1000）。关键是 overlap 不能为 0，否则跨块边界的语义会断裂。

#### Q: 向量检索和关键词检索（如 BM25）哪个好？

A: 各有优劣。向量检索擅长语义匹配（"汽车"能匹配"车辆"），但对精确术语匹配不如关键词检索。生产环境推荐混合检索（Hybrid Search）：向量检索 + BM25 加权融合。

#### Q: RAG 的检索结果不够相关怎么办？

A: 多层优化：1）优化分块策略（语义分块）；2）使用 Query Rewriting 改写用户查询；3）使用 HyDE 生成假设答案来引导检索；4）使用 Reranker 对检索结果二次排序；5）调整 Top-K 值和相似度阈值。

## 相关链接

[[rag]] | [[interview-qa-overview]]
