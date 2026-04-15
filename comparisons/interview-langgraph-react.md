---
title: "【面试专题】LangGraph 核心原理与 ReAct 对比"
created: 2026-04-15
updated: 2026-04-15
type: comparison
tags: [agent, interview, react]
sources: []
notion_id: 34367b21-8207-81b2-9f8b-c1218f7b3104
---

## LangGraph 核心原理与 ReAct 对比

> 难度：⭐⭐⭐⭐ | 面试频率：极高 | 关联：👉 上下文管理：短期记忆与长期记忆 👉 Agent 架构设计：从传统开发到智能体

---

### 一、ReAct 模式回顾

#### 1.1 什么是 ReAct？

ReAct（Reasoning + Acting）是 Yao 等人于 2022 年提出的 Agent 范式，核心思想是将推理（Reasoning）和行动（Acting）结合在一个循环中。

#### 1.2 ReAct 的工作流程

```javascript
用户输入 → LLM 推理（Thought）→ 执行工具（Action）→ 观察结果（Observation）→ 再次推理 → ... → 最终回答
```

这是一个线性单循环：每次迭代都是"思考→行动→观察"的固定模式。

#### 1.3 ReAct 的局限性

  - 线性流程：只能按固定顺序执行，无法实现条件分支

  - 状态管理弱：缺乏结构化的全局状态管理

  - 难以中断恢复：循环一旦开始，不容易在中间暂停和恢复

  - 多 Agent 协作困难：不支持多个 Agent 之间的复杂交互

---

### 二、LangGraph 核心概念

#### 2.1 LangGraph 是什么？

LangGraph 是 LangChain 团队开发的基于图（Graph）的 Agent 框架，它将 Agent 的执行流程建模为一个有向图，通过节点（Nodes）和边（Edges）定义 Agent 的行为。

#### 2.2 三大核心要素

State 是 LangGraph 的核心，它是一个全局共享的数据结构，所有节点都可以读取和修改。

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # messages 使用 add_messages 注解，自动处理消息追加（而非覆盖）
    messages: Annotated[list, add_messages]
    # 自定义状态字段
    current_tool: str | None
    iteration_count: int
```

关键点：

  - Annotated[list, add_messages] 是 LangGraph 的核心注解，告诉框架这个字段是累加型的（新消息追加到列表，而非替换整个列表）

  - State 在图的每个节点之间传递，形成数据流

  - 可以自定义 Reducer 函数来控制状态更新逻辑

每个 Node 是一个独立的处理单元，接收 State 作为输入，返回 State 的更新。

```python
def llm_node(state: AgentState):
    """LLM 推理节点：调用大模型生成响应"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state: AgentState):
    """工具执行节点：解析并执行工具调用"""
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    results = []
    for call in tool_calls:
        result = tools[call["name"]].invoke(call["args"])
        results.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    return {"messages": results}
```

Edges 定义节点之间的流转逻辑，支持两种类型：

  - 普通边：固定从 A 到 B

  - 条件边（Conditional Edges）：根据 State 动态决定下一个节点

```python
def should_continue(state: AgentState):
    """路由函数：决定下一步是调用工具还是结束"""
    last_message = state["messages"][-1]

    # 如果 LLM 返回了 tool_calls，则进入工具节点
    if last_message.tool_calls:
        return "tools"
    # 否则结束
    return "end"
```

#### 2.3 完整的 LangGraph Agent 构建

```python
from langgraph.graph import StateGraph, END

# 1. 创建图
graph = StateGraph(AgentState)

# 2. 添加节点
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

# 3. 设置入口
graph.set_entry_point("llm")

# 4. 添加条件边
graph.add_conditional_edges(
    "llm",           # 从 llm 节点出发
    should_continue,  # 路由函数
    {
        "tools": "tools",  # 返回 "tools" 则进入工具节点
        "end": END,        # 返回 "end" 则结束
    }
)

# 5. 工具执行后回到 LLM
graph.add_edge("tools", "llm")

# 6. 编译
app = graph.compile()
```

---

### 三、LangGraph vs ReAct：核心区别

---

### 四、LangGraph 高级特性

#### 4.1 Checkpointer（检查点持久化）

LangGraph 内置了状态持久化机制，可以将 Agent 的每一步状态保存到数据库中。

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# 使用 SQLite 作为检查点存储
with SqliteSaver.from_conn_string("agent_state.db") as checkpointer:
    app = graph.compile(checkpointer=checkpointer)

    # 使用 thread_id 隔离不同会话
    config = {"configurable": {"thread_id": "user_session_1"}}
    result = app.invoke({"messages": [("user", "你好")]}, config)
```

应用场景：

  - 会话恢复：用户关闭页面后重新打开，可以继续之前的对话

  - 多轮对话隔离：通过 thread_id 区分不同用户/会话

  - 调试回溯：可以查看任意步骤的状态

#### 4.2 Human-in-the-loop（人机协作）

LangGraph 支持在图的任意节点中断，等待人类确认后再继续。

```python
# 在工具执行前中断，等待人类确认
graph.add_node("tools", tool_node)
graph.add_edge("tools", "llm")

# 编译时启用中断
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["tools"]  # 在执行 tools 节点前中断
)
```

#### 4.3 多 Agent 协作

LangGraph 支持将多个 Agent 图组合成一个更大的系统：

```python
# Agent A：负责规划
planner = create_planner_graph()

# Agent B：负责执行
executor = create_executor_graph()

# 组合成多 Agent 系统
super_graph = StateGraph(SuperState)
super_graph.add_node("planner", planner)
super_graph.add_node("executor", executor)
super_graph.add_edge("planner", "executor")
super_graph.add_edge("executor", "planner")  # 反馈循环
```

---

### 五、面试高频追问

#### Q: LangGraph 的 add_messages 注解底层做了什么？

A: add_messages 是一个 Reducer 函数，它的逻辑是：当新消息到来时，不是替换整个 messages 列表，而是将新消息追加到现有列表中。如果新消息的 id 与已有消息相同，则会更新该消息（而不是重复添加）。这使得多个节点可以安全地修改 messages 字段而不互相覆盖。

#### Q: conditional_edges 和普通 add_edge 的区别？

A: add_edge 是静态的，固定从节点 A 到节点 B；add_conditional_edges 接收一个路由函数，该函数读取当前 State，返回一个字符串键值，映射到不同的目标节点。这使得 Agent 可以根据运行时状态（如 LLM 是否返回了 tool_calls）动态决定下一步走向。

#### Q: LangGraph 如何处理工具调用失败？

A: 在 tool_node 中，可以捕获工具执行异常，将错误信息作为 ToolMessage 返回给 LLM。LLM 会看到错误信息并尝试修正（如换一个工具或调整参数），这就是 LangGraph 自我修复能力的来源。

#### Q: LangGraph 和 LangChain 的关系？

A: LangChain 是一个通用的 LLM 应用框架（提供 Chain、Tool、Memory 等抽象）；LangGraph 是 LangChain 团队专门为构建有状态的、多步骤的 Agent 应用而开发的子框架。LangGraph 使用 LangChain 的底层组件（如 ChatModel、Tool），但提供了更精细的流程控制能力。

## 相关链接

[[langgraph]] | [[react]] | [[interview-qa-overview]]
