---
title: "2.2 Agent 框架三大要素设计"
created: 2026-04-15
updated: 2026-04-16
type: concept
tags: [agent, architecture, tool-use]
sources: [raw/articles/agent-framework-from-scratch.md]
---

## 2.2 Agent 框架三大要素设计

### 2.2.1 LLM Call

采用极简设计，以DeepSeek模型示例说明

- LLM Provider：使用DeepSeek deepseek-chat 模型
- LLM Call API：使用标准化OpenAI SDK
为保证代码的最大可读性，这里使用同步非流式调用。

### 2.2.2 Tools Call

采用极简的工具集，操作对象包含文件、Shell和Python代码执行

1）Tools 实现：总共支持4个工具函数

- shell_exec：执行shell命令并返回输出
- file_read：读取文件内容
- file_write：写入文件内容（自动创建目录）
- python_exec：在子进程中执行Python代码并返回输出

2）Tools 注册：这里选择的是手动维护字典映射的方式 name → (function, OpenAI function schema) ，这一步是为了解析llm call 的response时可以根据name匹配需要具体执行哪个tool

Tools 的定义遵循的是 OpenAI Function Calling 的标准格式（也称 OpenAI Tools API schema）

### 2.2.3 Context Engineering

- System Prompt：极简系统提示词，告知LLM可用工具和ReAct思考方式
- 用户Session管理：使用messages 列表方式（OpenAI chat 格式），它是核心状态，累积系统提示词、用户消息、助手响应和工具结果

## 相关链接

[[agent-framework-practice-modular|AI Agent 框架实践篇（模块化版本）]] | [[agent-framework-practice-section-architecture|2.1 Agent 框架架构图一览]] | [[agent-framework-practice-section-implementation|2.3 Agent 框架代码实现]]
