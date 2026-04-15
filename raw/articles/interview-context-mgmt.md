---
title: "【面试专题】上下文管理：短期记忆与长期记忆"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, interview, memory, rag]
sources: []
notion_id: 34367b21-8207-81c6-8eed-f5368d5630dd
---

## 上下文管理：短期记忆与长期记忆

> 难度：⭐⭐⭐⭐ | 面试频率：极高 | 关联：👉 LangGraph 核心原理与 ReAct 对比 👉 RAG 检索增强生成：从分块到检索

---

### 一、为什么上下文管理是 Agent 的核心？

LLM 的 Context Window（上下文窗口）是有限的（如 GPT-4o 为 128K tokens，Claude 为 200K tokens）。Agent 在运行过程中会不断累积消息（用户输入、LLM 响应、工具执行结果），如果不加管理，很快就会超出窗口限制。

上下文管理的核心目标：在有限的窗口内，让 Agent 拥有尽可能多的有效信息。

---

### 二、短期记忆（Short-term Memory）

#### 2.1 定义

短期记忆指的是当前会话/任务中的上下文信息，通常存储在 messages 列表中，随着对话的进行不断累积。

#### 2.2 LangGraph 中的短期记忆实现

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    # 所有消息都在 State 中，随图的流转自动传递
```

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# SQLite（适合开发/单机）
checkpointer = SqliteSaver.from_conn_string("state.db")

# PostgreSQL（适合生产/分布式）
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/db"
)

app = graph.compile(checkpointer=checkpointer)

# 通过 thread_id 实现会话隔离
config = {"configurable": {"thread_id": "session_abc123"}}
result = app.invoke({"messages": [user_msg]}, config)
```

thread_id 的作用：

  - 每个用户/会话有唯一的 thread_id

  - 同一 thread_id 下的状态是连续的（可以跨请求恢复）

  - 不同 thread_id 之间完全隔离

#### 2.3 消息裁剪策略

当 messages 列表过长时，需要进行裁剪：

```python
def trim_messages(messages: list, max_messages: int = 20):
    """只保留最近 N 条消息"""
    return messages[-max_messages:]
```

```python
import tiktoken

def trim_by_tokens(messages: list, max_tokens: int = 100000):
    """按 Token 数量裁剪，保留 System Prompt"""
    encoder = tiktoken.encoding_for_model("gpt-4")

    system_msgs = [m for m in messages if m["role"] == "system"]
    other_msgs = [m for m in messages if m["role"] != "system"]

    total_tokens = sum(len(encoder.encode(m["content"])) for m in system_msgs)
    trimmed = list(system_msgs)

    for msg in reversed(other_msgs):
        msg_tokens = len(encoder.encode(msg["content"]))
        if total_tokens + msg_tokens > max_tokens:
            break
        trimmed.insert(len(system_msgs), msg)
        total_tokens += msg_tokens

    return trimmed
```

```python
def summarize_old_messages(messages: list, llm) -> list:
    """将旧消息摘要化，保留最近消息原文"""
    if len(messages) <= 10:
        return messages

    old_messages = messages[:-6]  # 旧消息
    recent_messages = messages[-6:]  # 最近消息

    # 用 LLM 将旧消息压缩为一条摘要
    summary_prompt = f"请将以下对话历史压缩为简洁的摘要：\n{format_messages(old_messages)}"
    summary = llm.invoke(summary_prompt).content

    return [
        SystemMessage(content=f"之前的对话摘要：{summary}"),
        *recent_messages
    ]
```

---

### 三、长期记忆（Long-term Memory）

#### 3.1 定义

长期记忆指的是跨会话、跨任务持久化存储的信息，如用户偏好、历史行为、知识库等。

#### 3.2 实现方案

```python
# 存储用户画像和偏好
import psycopg2

def save_user_preference(user_id: str, key: str, value: str):
    conn = psycopg2.connect("postgresql://...")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_preferences (user_id, key, value) "
        "VALUES (%s, %s, %s) "
        "ON CONFLICT (user_id, key) DO UPDATE SET value = %s",
        (user_id, key, value, value)
    )
    conn.commit()

def get_user_preferences(user_id: str) -> dict:
    conn = psycopg2.connect("postgresql://...")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT key, value FROM user_preferences WHERE user_id = %s",
        (user_id,)
    )
    return dict(cursor.fetchall())
```

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 存储历史交互的向量化表示
vectorstore = Chroma(
    persist_directory="./user_memory",
    embedding_function=OpenAIEmbeddings()
)

def save_interaction(user_id: str, query: str, response: str, metadata: dict):
    """将用户交互存入向量数据库"""
    vectorstore.add_texts(
        texts=[f"用户问：{query}\nAgent答：{response}"],
        metadatas=[{"user_id": user_id, **metadata}],
        ids=[f"{user_id}_{int(time.time())}"]
    )

def recall_relevant_history(user_id: str, query: str, k: int = 5):
    """检索与当前查询最相关的历史交互"""
    results = vectorstore.similarity_search(
        query, k=k, filter={"user_id": user_id}
    )
    return [doc.page_content for doc in results]
```

```python
import redis

# Redis 用于热数据快速访问
redis_client = redis.Redis(host='localhost', port=6379)

def get_cached_preference(user_id: str, key: str):
    cached = redis_client.get(f"pref:{user_id}:{key}")
    if cached:
        return cached.decode()
    # 缓存未命中，从数据库加载
    value = get_from_db(user_id, key)
    if value:
        redis_client.setex(f"pref:{user_id}:{key}", 3600, value)
    return value
```

#### 3.3 长期记忆在 Agent 中的应用模式

```javascript
用户输入
  ↓
[检索长期记忆] → 从向量数据库/Redis 获取相关历史
  ↓
[注入 System Prompt] → 将检索到的信息注入上下文
  ↓
[Agent 推理] → LLM 基于增强后的上下文进行推理
  ↓
[更新长期记忆] → 将本次交互存入长期记忆
```

---

### 四、面试高频追问

#### Q: Checkpointer 和普通数据库存储的区别？

A: Checkpointer 是 LangGraph 内置的状态快照机制，它保存的是图的完整状态（包括所有节点的中间结果），支持时间旅行（回到任意步骤）。普通数据库存储的是业务数据（如用户偏好、历史记录），是应用层面的持久化。两者互补：Checkpointer 管理 Agent 运行状态，数据库管理业务数据。

#### Q: 如何解决高并发下的上下文隔离？

A: 通过 thread_id 实现逻辑隔离。每个用户请求分配唯一的 thread_id，Checkpointer 根据 thread_id 存取对应的状态。在分布式环境中，可以使用 PostgreSQL 作为 Checkpointer 后端，配合连接池管理并发访问。

#### Q: 摘要化策略会不会丢失关键信息？

A: 会。这是摘要化的固有缺陷。缓解方案包括：1）保留最近 N 轮原文不摘要；2）使用结构化摘要（按主题分类）；3）将关键信息（如用户 ID、任务目标）始终保留在 System Prompt 中；4）结合向量检索，在需要时从长期记忆中找回细节。

#### Q: Context Window 溢出时 Agent 会怎样？

A: 会导致 API 调用失败（HTTP 400 错误）。预防措施：1）在每次 LLM 调用前计算 token 数；2）设置安全阈值（如窗口的 80%）；3）超过阈值时触发裁剪策略；4）使用支持更大窗口的模型作为备选。

## 相关链接

[[context-management]] | [[interview-qa-overview]]
