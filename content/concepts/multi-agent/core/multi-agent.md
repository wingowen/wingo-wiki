---
title: "Multi-Agent | 多智能体"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, architecture]
sources: []
---

# Multi-Agent

## Overview

Multi-Agent 系统由多个独立的 Agent 组成，它们协作完成复杂任务。

## 协作模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **Sequential** | Agent 按顺序执行，一个完成后再下一个 | 有依赖的任务链 |
| **Parallel** | 多个 Agent 同时工作 | 独立子任务 |
| **Hierarchical** | 一个主 Agent 协调多个子 Agent | 复杂项目管理 |

## Anthropic 多 Agent 研究系统

Anthropic 在其工程博客中分享了构建多 Agent 研究系统的经验，核心要点包括：
- 明确 Agent 职责边界
- 设计有效的通信协议
- 处理 Agent 间的冲突

## 相关链接

[[ai-agent]] | [[anthropic]] | [[langgraph]] | [[multi-agent-research]]
