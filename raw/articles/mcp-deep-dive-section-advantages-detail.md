---
title: "通过 MCP 实现代码执行的优势"
created: 2025-11-04
updated: 2026-04-16
type: concept
tags: [mcp, agent, architecture]
sources: []
---

## 通过 MCP 实现代码执行的优势
通过 MCP 实现代码执行使 Agent 能够更高效地使用上下文——按需加载工具、在数据到达模型之前进行过滤，以及一步执行复杂逻辑。使用这种方法还有安全和状态管理方面的好处。

### 渐进式披露
模型非常擅长导航文件系统。将工具以代码形式呈现在文件系统上，允许模型按需读取工具定义，而不是一次性读取所有定义。

或者，可以在服务器中添加一个 search_tools 工具来查找相关定义。例如，当使用上面假设的 Salesforce 服务器时，Agent 搜索"salesforce"并只加载当前任务需要的那些工具。在 search_tools 工具中包含一个详细级别参数，允许 Agent 选择所需的详细程度（如仅名称、名称和描述、或包含 schema 的完整定义），也有助于 Agent 节省上下文并高效地查找工具。

### 上下文高效的工具结果
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

### 隐私保护操作
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

### 状态持久化和 Skills
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

## 相关链接

[[mcp-deep-dive-modular|MCP 深度解析（模块化版本）]] | [[mcp-deep-dive-section-context-efficiency|通过 MCP 实现代码执行提升上下文效率]] | [[mcp-deep-dive-section-summary|总结]]
