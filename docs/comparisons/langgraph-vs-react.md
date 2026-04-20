---
title: "LangGraph 核心原理与 ReAct 对比"
created: "2026-04-15"
updated: "2026-04-15T10:07:00.000Z"
type: comparison
tags: [agent, interview, react]
sources: ["notion:34367b21-8207-81b2-9f8b-c1218f7b3104"]
notion_id: "34367b21-8207-81b2-9f8b-c1218f7b3104"
---

> **难度**：⭐⭐⭐⭐ | **面试频率**：极高 | **关联**：[context-management](../concepts/context-engineering/core/context-management.md) [agent-architecture](../concepts/agent-architecture/core/agent-architecture.md)

---

# LangGraph 核心原理与 ReAct 对比

## 一、ReAct 范式

### 1.1 ReAct 循环

```python
# ReAct = Reasoning + Acting
while True:
    thought = llm.think(state["messages"])  # 思考
    action = llm.act(thought)               # 决定行动
    result = execute_tool(action)           # 执行工具
    state["messages"].append(result)       # 添加结果
    
    if is_finished(result):
        break
```

### 1.2 ReAct 的局限性

| 问题 | 说明 |
|------|------|
| 线性循环 | 只能顺序执行，难以表达复杂流程 |
| 状态分散 | 状态分散在 messages 列表中 |
| 难以持久化 | 中断后难以恢复执行状态 |
| 分支困难 | 难以表达条件分支和并行 |

---

## 二、LangGraph 核心概念

### 2.1 三大核心组件

```python
from langgraph.graph import StateGraph, END

# 1. State：全局状态
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    current_node: str
    intermediate_values: dict

# 2. Nodes：节点（函数）
def node_a(state: AgentState) -> AgentState:
    # 处理逻辑
    return {"current_node": "node_b"}

def node_b(state: AgentState) -> AgentState:
    return {"current_node": END}

# 3. Edges：边（流转关系）
graph = StateGraph(AgentState)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)
```

### 2.2 add_messages 注解

```python
from operator import add
from typing import Annotated

class AgentState(TypedDict):
    # 使用 add_messages 注解，自动合并消息列表
    messages: Annotated[list, add_messages]
```

**作用**：保证消息列表的累积而非覆盖，每次返回时自动将新消息追加到列表。

### 2.3 条件路由

```python
from langgraph.graph import ConditionalEdges

# 条件边：根据状态决定下一个节点
def route_after_node_a(state: AgentState) -> str:
    last_msg = state["messages"][-1]
    if "error" in last_msg.content.lower():
        return "error_handler"
    elif "complete" in last_msg.content.lower():
        return END
    else:
        return "node_b"

# 添加条件边
graph.add_conditional_edges(
    "node_a",
    route_after_node_a,
    {
        "error_handler": "error_handler_node",
        "node_b": "node_b",
        END: END
    }
)
```

---

## 三、LangGraph vs ReAct

| 维度 | ReAct | LangGraph |
|------|-------|-----------|
| 执行模型 | 线性循环 | 有向图 |
| 状态管理 | messages 列表 | 全局 State + 注解 |
| 流程控制 | 硬编码 if-else | 边/条件边 |
| 多步分支 | 困难 | 天然支持 |
| 中断恢复 | 难 | Checkpointer 原生支持 |
| 并行执行 | 不支持 | 支持分支并行 |

---

## 四、面试高频追问

### Q: LangGraph 怎么实现中断恢复？

A: 通过 Checkpointer。当 Agent 执行中断时，Checkpointer 会保存当前 State 到持久化存储（SQLite/PostgreSQL）。恢复时，通过 thread_id 加载状态，继续执行。

```python
app = graph.compile(checkpointer=PostgresSaver.from_conn_string("..."))

# 中断点
interrupted_state = app.invoke(input, config={"configurable": {"thread_id": "123"}})

# 恢复执行
resume_state = app.invoke(None, config={"configurable": {"thread_id": "123"}})
```

### Q: add_messages 和普通列表有什么区别？

A: add_messages 是一个**累加注解**。普通列表赋值会覆盖，而 add_messages 保证了节点返回的新消息会**累积**到现有列表，而不是替换。

### Q: 为什么需要条件边？

A: 真实场景中，Agent 的下一步不是固定的。需要根据中间结果动态决定：成功时进入下一节点，失败时进入错误处理，无事发生时结束。这种动态路由用 if-else 难以表达，但用条件边可以清晰建模。
