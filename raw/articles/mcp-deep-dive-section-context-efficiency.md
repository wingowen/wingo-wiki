---
title: "通过 MCP 实现代码执行提升上下文效率"
created: 2025-11-04
updated: 2026-04-16
type: concept
tags: [mcp, agent, architecture]
sources: []
---

## 通过 MCP 实现代码执行提升上下文效率
随着代码执行环境在 Agent 中变得越来越普遍，一种解决方案是将 MCP 服务器作为代码 API 而非直接工具调用。Agent 可以编写代码来与 MCP 服务器交互。这种方法同时解决了两个挑战：Agent 可以只加载所需的工具，并在将结果返回给模型之前在执行环境中处理数据。

有多种方式可以实现这一点。一种方法是从连接的 MCP 服务器生成所有可用工具的文件树。以下是使用 TypeScript 的实现：

```javascript
servers
├── google-drive
│   ├── getDocument.ts
│   ├── ... (other tools)
│   └── index.ts
├── salesforce
│   ├── updateRecord.ts
│   ├── ... (other tools)
│   └── index.ts
└── ... (other servers)

```

然后每个工具对应一个文件，类似于：

```javascript
// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
}

interface GetDocumentResponse {
  content: string;
}

/* Read a document from Google Drive */
export async function getDocument(input: GetDocumentInput): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>('google_drive__get_document', input);
}


```

我们上面的 Google Drive 到 Salesforce 的例子变成了这样的代码：

```javascript
// Read transcript from Google Docs and add to Salesforce prospect
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;
await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});


```

Agent 通过探索文件系统来发现工具：列出 ./servers/ 目录以查找可用的服务器（如 google-drive 和 salesforce），然后读取它需要的特定工具文件（如 getDocument.ts 和 updateRecord.ts）来了解每个工具的接口。这让 Agent 只加载当前任务所需的定义。这将 token 使用量从 150,000 个减少到 2,000 个——节省了 98.7% 的时间和成本。

Cloudflare 发布了类似的发现，将这种通过 MCP 实现的代码执行称为"Code Mode"。核心洞察是相同的：LLM 擅长编写代码，开发者应该利用这一优势来构建更高效地与 MCP 服务器交互的 Agent。

💡 术语解释：Progressive Disclosure（渐进式披露）是一种交互设计模式，信息按需逐步展示，而非一次性全部呈现。在本文中，Agent 只在需要时才读取工具定义，而非预先加载所有定义。

## 相关链接

[[mcp-deep-dive-modular|MCP 深度解析（模块化版本）]] | [[mcp-deep-dive-section-token-issue|工具消耗过多 token 导致 Agent 效率降低]] | [[mcp-deep-dive-section-advantages-detail|通过 MCP 实现代码执行的优势]]
