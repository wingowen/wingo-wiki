---
title: "通过 MCP 实现代码执行：构建更高效的 Agent | Code execution with MCP"
created: 2025-06-26
updated: 2025-06-26
type: concept
tags: [agent, anthropic]
sources: []
notion_id: 34267b21-8207-8138-b312-c3d319f17b5a
---

# 通过 MCP 实现代码执行：构建更高效的 Agent | Code execution with MCP
> 原文链接：Code execution with MCP: Building more efficient agents
> 作者：Adam Jones, Conor Kelly
> 发布日期：2025-11-04
> 翻译日期：2026-04-14
## 通过 MCP 实现代码执行：构建更高效的 Agent
直接的工具调用会为每个定义和结果消耗上下文。Agent 通过编写代码来调用工具，能够更好地扩展规模。以下是它在 MCP 中的工作方式。
Model Context Protocol（模型上下文协议，简称 MCP） 是一个连接 AI Agent 与外部系统的开放标准。传统上，将 Agent 连接到工具和数据需要为每一对组合构建自定义集成，这导致了碎片化和重复劳动，使得构建真正互联的系统变得困难。MCP 提供了一个通用协议——开发者只需在 Agent 中实现一次 MCP，即可解锁整个集成生态系统。
自 2024 年 11 月发布 MCP 以来，其采用速度非常迅速：社区已经构建了数千个 MCP 服务器，SDK 已覆盖所有主流编程语言，业界也已将 MCP 作为连接 Agent 与工具和数据的实际标准。
如今，开发者通常会构建能够访问跨数十个 MCP 服务器的数百或数千个工具的 Agent。然而，随着连接工具数量的增长，预先加载所有工具定义并将中间结果通过上下文窗口传递，会拖慢 Agent 的速度并增加成本。
在这篇博客中，我们将探讨代码执行如何让 Agent 更高效地与 MCP 服务器交互，在处理更多工具的同时使用更少的 token。
### 工具消耗过多 token 导致 Agent 效率降低
随着 MCP 使用规模的扩大，有两种常见模式会增加 Agent 的成本和延迟：
1. 工具定义过载上下文窗口；
  1. 中间工具结果消耗额外的 token。
#### 1. 工具定义过载上下文窗口
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
#### 2. 中间工具结果消耗额外的 token
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
### 通过 MCP 实现代码执行提升上下文效率
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
### 通过 MCP 实现代码执行的优势
通过 MCP 实现代码执行使 Agent 能够更高效地使用上下文——按需加载工具、在数据到达模型之前进行过滤，以及一步执行复杂逻辑。使用这种方法还有安全和状态管理方面的好处。
#### 渐进式披露
模型非常擅长导航文件系统。将工具以代码形式呈现在文件系统上，允许模型按需读取工具定义，而不是一次性读取所有定义。
或者，可以在服务器中添加一个 search_tools 工具来查找相关定义。例如，当使用上面假设的 Salesforce 服务器时，Agent 搜索"salesforce"并只加载当前任务需要的那些工具。在 search_tools 工具中包含一个详细级别参数，允许 Agent 选择所需的详细程度（如仅名称、名称和描述、或包含 schema 的完整定义），也有助于 Agent 节省上下文并高效地查找工具。
#### 上下文高效的工具结果
在处理大型数据集时，Agent 可以在返回结果之前在代码中过滤和转换数据。考虑获取一个 10,000 行的电子表格：
```javascript
// Without code execution - all rows flow through context
TOOL CALL: gdrive.getSheet(sheetId: 'abc123')
        → returns 10,000 rows in context to filter manually

// With code execution - filter in the execution environment
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(row => 
  row["Status"] === 'pending'
);
console.log(`Found ${pendingOrders.length} pending orders`);
console.log(pendingOrders.slice(0, 5)); // Only log first 5 for review

```
Agent 看到的是 5 行而不是 10,000 行。类似的模式也适用于聚合操作、跨多个数据源的连接，或提取特定字段——所有这些都不会膨胀上下文窗口。
循环、条件判断和错误处理可以使用熟悉的代码模式来完成，而不是链接单独的工具调用。例如，如果你需要在 Slack 中获取部署通知，Agent 可以编写：
```javascript
let found = false;
while (!found) {
  const messages = await slack.getChannelHistory({ channel: 'C123456' });
  found = messages.some(m => m.text.includes('deployment complete'));
  if (!found) await new Promise(r => setTimeout(r, 5000));
}
console.log('Deployment notification received');

```
这种方法比在 Agent 循环中交替进行 MCP 工具调用和休眠命令更高效。
此外，能够编写出被执行的条件树也节省了"首 token 时间"（Time to First Token）延迟：Agent 无需等待模型评估 if 语句，而是让代码执行环境来完成这项工作。
💡 术语解释：Time to First Token（首 token 时间）是指从发送请求到模型输出第一个 token 的时间。将条件判断放在代码中执行，可以避免等待模型推理，从而降低延迟。
#### 隐私保护操作
当 Agent 使用代码执行与 MCP 交互时，中间结果默认保留在执行环境中。这样，Agent 只能看到你显式记录或返回的内容，这意味着你不希望与模型共享的数据可以在你的工作流中流转，而无需进入模型的上下文。
对于更敏感的工作负载，Agent 框架可以自动对敏感数据进行令牌化处理。例如，假设你需要将客户联系信息从电子表格导入 Salesforce。Agent 编写如下代码：
```javascript
const sheet = await gdrive.getSheet({ sheetId: 'abc123' });
for (const row of sheet.rows) {
  await salesforce.updateRecord({
    objectType: 'Lead',
    recordId: row.salesforceId,
    data: { 
      Email: row.email,
      Phone: row.phone,
      Name: row.name
    }
  });
}
console.log(`Updated ${sheet.rows.length} leads`);

```
MCP 客户端在数据到达模型之前进行拦截并令牌化 PII（个人身份信息）：
```javascript
// What the agent would see, if it logged the sheet.rows:
[
  { salesforceId: '00Q...', email: '[EMAIL_1]', phone: '[PHONE_1]', name: '[NAME_1]' },
  { salesforceId: '00Q...', email: '[EMAIL_2]', phone: '[PHONE_2]', name: '[NAME_2]' },
  ...
]

```
然后，当数据在另一个 MCP 工具调用中被共享时，它会通过 MCP 客户端中的查找表进行反令牌化。真实的电子邮件地址、电话号码和姓名从 Google Sheets 流向 Salesforce，但不会经过模型。这防止了 Agent 意外记录或处理敏感数据。你还可以利用这一点来定义确定性的安全规则，选择数据可以流向和流出的位置。
💡 术语解释：PII（Personally Identifiable Information，个人身份信息）是指可以用来识别特定个人的数据，如姓名、电子邮件、电话号码等。令牌化（Tokenization）是将敏感数据替换为非敏感占位符的过程，以保护隐私。
#### 状态持久化和 Skills
具有文件系统访问权限的代码执行允许 Agent 在操作之间维护状态。Agent 可以将中间结果写入文件，使其能够恢复工作和跟踪进度：
```javascript
const leads = await salesforce.query({ 
  query: 'SELECT Id, Email FROM Lead LIMIT 1000' 
});
const csvData = leads.map(l => `${l.Id},${l.Email}`).join('\n');
await fs.writeFile('./workspace/leads.csv', csvData);

// Later execution picks up where it left off
const saved = await fs.readFile('./workspace/leads.csv', 'utf-8');

```
Agent 还可以将自己的代码保存为可重用的函数。一旦 Agent 为某个任务开发了可用的代码，它就可以保存该实现以供将来使用：
```javascript
// In ./skills/save-sheet-as-csv.ts
import * as gdrive from './servers/google-drive';
export async function saveSheetAsCsv(sheetId: string) {
  const data = await gdrive.getSheet({ sheetId });
  const csv = data.map(row => row.join(',')).join('\n');
  await fs.writeFile(`./workspace/sheet-${sheetId}.csv`, csv);
  return `./workspace/sheet-${sheetId}.csv`;
}

// Later, in any agent execution:
import { saveSheetAsCsv } from './skills/save-sheet-as-csv';
const csvPath = await saveSheetAsCsv('abc123');

```
这与 Skills 的概念密切相关——Skills 是可重用指令、脚本和资源的文件夹，旨在帮助模型在专业任务上提高性能。为这些保存的函数添加 SKILL.md 文件可以创建一个结构化的技能，模型可以引用和使用。随着时间的推移，这允许你的 Agent 构建一个高级能力的工具箱，不断演进其最高效工作所需的脚手架。
💡 术语解释：Skills（技能）是 Claude Agent 的一种组织模式，将可重用的指令、脚本和资源打包在文件夹中，形成模型可以在专业任务中引用的结构化能力单元。
请注意，代码执行引入了其自身的复杂性。运行 Agent 生成的代码需要一个安全的执行环境，配备适当的沙箱化、资源限制和监控。这些基础设施需求增加了运营开销和安全考量，而直接工具调用则避免了这些问题。代码执行的好处——降低 token 成本、减少延迟和改进工具组合——应该与这些实现成本进行权衡。
### 总结
MCP 为 Agent 连接许多工具和系统提供了基础协议。然而，一旦连接了过多的服务器，工具定义和结果可能会消耗过多的 token，降低 Agent 的效率。
尽管这里的许多问题看起来很新颖——上下文管理、工具组合、状态持久化——但它们在软件工程中已有已知的解决方案。代码执行将这些成熟的模式应用于 Agent，让它们使用熟悉的编程构造来更高效地与 MCP 服务器交互。如果你实现了这种方法，我们鼓励你与 MCP 社区分享你的发现。
#### 致谢
本文由 Adam Jones 和 Conor Kelly 撰写。感谢 Jeremy Fox、Jerome Swannack、Stuart Ritchie、Molly Vorwerck、Matt Samuels 和 Maggie Vo 对本文草稿的反馈。
---
> 译者注：本文介绍了 Anthropic 工程团队在 MCP 生态中发现的 token 效率问题及其解决方案。核心思路是将 MCP 服务器从"直接工具调用"模式转变为"代码 API"模式，让 Agent 通过编写代码来按需发现和调用工具。这一思路与 Cloudflare 提出的"Code Mode"不谋而合，体现了业界对 Agent 效率优化的共同探索。文中提到的渐进式披露、隐私保护令牌化、Skills 等概念，对于构建生产级 Agent 系统具有重要的参考价值。值得注意的是，代码执行方案需要配合沙箱化等安全措施使用，读者在实际应用时应充分评估安全风险。

## 相关链接

[[mcp]] | [[claude-code]]
