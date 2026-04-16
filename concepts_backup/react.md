---
title: "ReAct"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, planning, react, reasoning]
sources: []
---

# ReAct

## Overview

ReAct = Reasoning + Acting，是一种让 LLM 交替进行推理和行动的提示词框架。

## 核心循环

```
Thought → Action → Observation → Thought → ...
```

- **Thought (思考)**: 分析当前状态，决定下一步
- **Action (行动)**: 执行工具或 API 调用
- **Observation (观察)**: 获取行动结果

## 与 LangGraph 对比

[[langgraph]] 是 ReAct 的工程化实现，添加了状态管理和持久化能力。

## 代码示例

```python
response = llm.invoke(f"""
请按照以下步骤完成任务：
1. 思考：{user_input}
2. 行动：使用搜索工具查找相关信息
3. 观察：分析搜索结果
4. 重复直到得到答案
""")
```

## 相关链接

[[ai-agent]] | [[langgraph]] | Reasoning | Planning