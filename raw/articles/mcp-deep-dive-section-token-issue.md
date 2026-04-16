---
title: "工具消耗过多 token 导致 Agent 效率降低"
created: 2025-11-04
updated: 2026-04-16
type: concept
tags: [mcp, agent, architecture]
sources: []
---

## 工具消耗过多 token 导致 Agent 效率降低
随着 MCP 使用规模的扩大，有两种常见模式会增加 Agent 的成本和延迟：
1. 工具定义过载上下文窗口；
  1. 中间工具结果消耗额外的 token。

### 1. 工具定义过载上下文窗口
大多数 MCP 客户端会预先将所有工具定义直接加载到上下文中，使用直接工具调用语法将其暴露给模型。这些工具定义可能看起来像这样：

```javascript
gdrive.getDocument
     Description: Retrieves a document from Google Drive
     Parameters:
                documentId (required, string): The ID of the document to retrieve
                fields (optional, string): Specific fields to return
     Returns: Document object with title, body content, metadata, permissions, etc.

```

```javascript
salesforce.updateRecord
    Description: Updates a record in Salesforce
    Parameters:
               objectType (required, string): Type of Salesforce object (Lead, Contact,      Account, etc.)
               recordId (required, string): The ID of the record to update
               data (required, object): Fields to update with their new values
     Returns: Updated record object with confirmation

```

工具描述占据了更多的上下文窗口空间，增加了响应时间和成本。在 Agent 连接到数千个工具的情况下，它们需要在读取请求之前处理数十万个 token。

💡 术语解释：上下文窗口（Context Window）是指大语言模型在一次对话中能够处理的最大文本长度。工具定义越多，留给实际对话和推理的空间就越少。

### 2. 中间工具结果消耗额外的 token
大多数 MCP 客户端允许模型直接调用 MCP 工具。例如，你可能会要求你的 Agent："从 Google Drive 下载我的会议记录，并将其附加到 Salesforce 线索中。"

模型会进行如下调用：

```javascript
TOOL CALL: gdrive.getDocument(documentId: "abc123")
        → returns "Discussed Q4 goals...\n[full transcript text]"
           (loaded into model context)

TOOL CALL: salesforce.updateRecord(
			objectType: "SalesMeeting",
			recordId: "00Q5f000001abcXYZ",
		data: { "Notes": "Discussed Q4 goals...\n[full transcript text written out]" }
	)
	(model needs to write entire transcript into context again)

```

每个中间结果都必须经过模型。在这个例子中，完整的会议记录流经了两次。对于一个 2 小时的销售会议来说，这可能意味着额外处理 50,000 个 token。更大的文档甚至可能超出上下文窗口的限制，导致工作流中断。

在处理大型文档或复杂数据结构时，模型在工具调用之间复制数据时更容易出错。

MCP 客户端将工具定义加载到模型的上下文窗口中，并编排一个消息循环，其中每个工具调用和结果在操作之间都经过模型。

## 相关链接

[[mcp-deep-dive-modular|MCP 深度解析（模块化版本）]] | [[mcp-deep-dive-section-code-execution-detail|通过 MCP 实现代码执行：构建更高效的 Agent]] | [[mcp-deep-dive-section-context-efficiency|通过 MCP 实现代码执行提升上下文效率]]
