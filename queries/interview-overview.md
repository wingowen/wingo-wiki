---
title: "AI Agent 面试复盘总览"
created: "2026-04-15"
updated: "2026-04-15T10:07:00.000Z"
type: concept
tags: [agent, hyde, interview, rag]
sources: ["notion:34367b21-8207-81e2-bc9c-f119f7ae87f6"]
notion_id: "34367b21-8207-81e2-bc9c-f119f7ae87f6"
---

> **面试岗位**：AI应用开发 / 智能体（Agent）开发实习生
> **面试强度**：⭐⭐⭐⭐⭐（极高，高压压力测试）
> **项目方向**：智能体旅游项目
> **核心痛点**：项目细节被深度拷问，底层原理掌握不足

---

# AI Agent 面试复盘总览

## 一、面试核心分析

本次面试官专业能力极强，直击项目底层实现逻辑，属于典型的高压技术面试。面试重点不在于"你做了什么功能"，而在于"你为什么这么做"以及"底层原理是什么"。

---

## 二、技术考点索引

### 1. LangGraph 核心原理

- LangGraph 如何替代 ReAct？图流转 vs 线性循环
- State（全局状态）、Nodes（节点）、Edges（边）的设计思想
- add_messages 注解与条件路由（conditional_edges）
- 多智能体协作与中断恢复机制
- **关联页面**：👉 [[langgraph-vs-react]]

### 2. 上下文管理（Context Management）

- 短期记忆：State 传递、Checkpointer、线程隔离
- 长期记忆：数据库存储、向量检索历史摘要
- 消息裁剪策略与 Context Window 溢出防护
- **关联页面**：👉 [[context-management]]

### 3. RAG 检索增强生成

- 文档分块（Chunking）策略：语义切分、重叠设置
- 向量存储与 Top-K 检索
- 超大文件处理方案
- **关联页面**：👉 [[interview-rag]]

### 4. HyDE 假设文档嵌入

- HyDE 原理：用 LLM 生成的假答案来引导检索
- 适用场景：查询简短、模糊时
- 与 RAG Fusion、Query Rewriting 的对比
- **关联页面**：👉 [[interview-hyde]]

### 5. Agent 架构设计

- 智能体 vs 传统开发的根本区别
- 感知-决策-行动闭环（Perception-Decision-Action）
- C端用户偏好实现：用户画像 + 向量检索
- **关联页面**：👉 [[agent-architecture]]

---

## 三、改进建议

1. **夯实底层**：不仅要会用 LangChain/LangGraph，更要理解其底层的 State 管理机制和图流转逻辑
2. **RAG 深化**：重点掌握 HyDE、RAG Fusion、Query Rewriting 等高级检索优化策略
3. **项目包装**：复盘时不要只罗列"做了什么功能"，要突出技术难点和解决方案
4. **心态建设**：AI Agent 面试本身就偏向底层原理，被问住是正常的，关键是展现思考过程

---

## 四、面试高频问题速查表

| 问题 | 考察点 | 关联 |
|------|--------|------|
| LangGraph 如何实现循环？ | 图流转机制 | [[langgraph]] |
| Checkpointer 原理？ | 状态持久化 | [[context-management]] |
| HyDE 幻觉问题？ | RAG 增强原理 | [[hyde]] |
| Chunk_size 怎么选？ | RAG 分块策略 | [[rag]] |
| Agent 安全怎么保证？ | Agent 架构 | [[agent-architecture]] |

## 相关链接

[[ai-agent]] | [[interview-qa-overview]]
