---
title: "MCP 核心原理"
created: 2025-06-26
updated: 2025-06-26
type: concept
tags: [anthropic, mcp]
sources: []
notion_id: 34367b21-8207-8199-83e2-4f68f4d7e0b7
---

# MCP 核心原理

## Overview

MCP（Model Context Protocol）是 Anthropic 提出的开放协议，用于标准化 AI 模型与外部工具、数据的连接。

## 架构

┌─────────────┐     MCP      ┌─────────────┐
│   Claude    │◄────────────►│  MCP Server │
│   (Client)  │              │ (File, DB,  │
└─────────────┘              │  Web, etc.) │
                             └─────────────┘

## 核心优势

- **标准化**: 一次开发，多处使用
- **安全**: 数据不离开本地
- **简化安装**: Desktop Extensions 实现一键安装



## Desktop Extensions（桌面扩展）

> 原文链接：Desktop Extensions: One-click MCP server installation for Claude Desktop
> 作者：Anthropic Engineering Team
> 发布日期：2025-06-26
> 翻译日期：2026-04-14
## 桌面扩展：Claude Desktop 一键安装 MCP 服务器 | Desktop Extensions
发布于 2025 年 6 月 26 日
Desktop Extensions（桌面扩展）让安装 MCP 服务器变得像点击按钮一样简单。本文将分享其技术架构以及创建优秀扩展的实用建议。
- 文件扩展名更新
去年当我们发布 Model Context Protocol（模型上下文协议，简称 MCP）时，我们看到开发者构建了令人惊叹的本地服务器，让 Claude 能够访问从文件系统到数据库的各种资源。但我们反复听到同样的反馈：安装过程太复杂了。用户需要安装开发者工具、手动编辑配置文件，还经常被依赖问题卡住。
今天，我们推出了 Desktop Extensions（桌面扩展）——一种全新的打包格式，让安装 MCP 服务器变得像点击按钮一样简单。
#### 解决 MCP 安装难题
本地 MCP 服务器为 Claude Desktop 用户解锁了强大的能力。它们可以与本地应用交互、访问私有数据、与开发工具集成——同时所有数据都保留在用户的机器上。然而，当前的安装流程造成了显著的障碍：
- 需要开发者工具：用户需要安装 Node.js、Python 或其他运行时（Runtime）
  - 手动配置：每个服务器都需要编辑 JSON 配置文件
  - 依赖管理：用户必须自行解决包冲突和版本不匹配问题
  - 缺乏发现机制：寻找有用的 MCP 服务器需要在 GitHub 上搜索
  - 更新复杂：保持服务器最新意味着需要手动重新安装
💡 术语解释：运行时（Runtime）是指运行程序所需的软件环境。例如，Node.js 就是 JavaScript 代码的运行时环境，Python 则是 Python 代码的运行时环境。
这些摩擦点意味着，尽管 MCP 服务器功能强大，但对非技术用户来说基本无法使用。
#### 介绍 Desktop Extensions
Desktop Extensions（.mcpb 文件）通过将整个 MCP 服务器——包括所有依赖——打包成一个可安装的包来解决这些问题。以下是用户体验的变化：
之前：
```javascript
# 先安装 Node.js
npm install -g @example/mcp-server
# 手动编辑 ~/.claude/claude_desktop_config.json
# 重启 Claude Desktop
# 祈祷它能正常工作
```
之后：
1. 下载一个 .mcpb 文件
  1. 双击用 Claude Desktop 打开
  1. 点击"安装"
就这样。不需要终端，不需要配置文件，没有依赖冲突。
### 架构概览
Desktop Extension 是一个 ZIP 压缩包，包含本地 MCP 服务器以及一个 manifest.json，后者描述了 Claude Desktop 和其他支持桌面扩展的应用所需了解的一切信息。
```javascript
extension.mcpb (ZIP 压缩包)
├── manifest.json # 扩展元数据和配置
├── server/ # MCP 服务器实现
│   └── [服务器文件]
├── dependencies/ # 所有必需的包/库
└── icon.png # 可选：扩展图标

# 示例：Node.js 扩展
extension.mcpb
├── manifest.json # 必需：扩展元数据和配置
├── server/ # 服务器文件
│   └── index.js # 主入口文件
├── node_modules/ # 打包的依赖
├── package.json # 可选：NPM 包定义
└── icon.png # 可选：扩展图标

# 示例：Python 扩展
extension.mcpb (ZIP 文件)
├── manifest.json # 必需：扩展元数据和配置
├── server/ # 服务器文件
│   ├── main.py # 主入口文件
│   └── utils.py # 附加模块
├── lib/ # 打包的 Python 包
├── requirements.txt # 可选：Python 依赖列表
└── icon.png # 可选：扩展图标
```
Desktop Extension 中唯一必需的文件就是 manifest.json。Claude Desktop 处理所有复杂性：
- 内置运行时：我们随 Claude Desktop 一起附带 Node.js，消除了外部依赖
  - 自动更新：当有新版本可用时，扩展会自动更新
  - 安全密钥存储：API Key 等敏感配置存储在操作系统密钥链（OS Keychain）中
💡 术语解释：OS Keychain（操作系统密钥链）是操作系统提供的一种安全存储机制，用于保存密码、API Key 等敏感信息。macOS 使用 Keychain，Windows 使用 Credential Manager，Linux 使用 Secret Service API。
manifest 包含人类可读的信息（如名称、描述或作者）、功能声明（工具、提示词）、用户配置和运行时需求。大多数字段是可选的，因此最小版本非常简短，尽管在实际中，我们预期所有三种支持的扩展类型（Node.js、Python 和经典二进制/可执行文件）都会包含文件：
```javascript
{
  "mcpb_version": "0.1", // 此 manifest 遵循的 MCPB 规范版本
  "name": "my-extension", // 机器可读名称（用于 CLI、API）
  "version": "1.0.0", // 扩展的语义化版本
  "description": "A simple MCP extension", // 扩展功能的简要描述
  "author": { // 作者信息（必需）
    "name": "Extension Author" // 作者姓名（必需字段）
  },
  "server": { // 服务器配置（必需）
    "type": "node", // 服务器类型："node"、"python" 或 "binary"
    "entry_point": "server/index.js", // 主服务器文件的路径
    "mcp_config": { // MCP 服务器配置
      "command": "node", // 运行服务器的命令
      "args": [ // 传递给命令的参数
        "${__dirname}/server/index.js" // ${__dirname} 会被替换为扩展的目录
      ]
    }
  }
}
```
💡 术语解释：Semantic Versioning（语义化版本）是一种版本号命名规范，格式为 主版本号.次版本号.修订号（如 1.0.0）。主版本号变更表示不兼容的 API 修改，次版本号变更表示向后兼容的功能新增，修订号变更表示向后兼容的问题修复。
manifest 规范中有许多便捷选项，旨在简化本地 MCP 服务器的安装和配置。服务器配置对象可以以模板字面量（Template Literal）的形式定义用户自定义配置，同时支持平台特定的覆盖。扩展开发者可以详细定义他们希望从用户那里收集什么样的配置。
让我们看一个具体示例，了解 manifest 如何辅助配置。在下面的 manifest 中，开发者声明用户需要提供一个 api_key。在用户提供该值之前，Claude 不会启用该扩展，会自动将其保存在操作系统的密钥库中，并在启动服务器时将 ${user_config.api_key} 透明地替换为用户提供的值。类似地，${__dirname} 会被替换为扩展解压目录的完整路径。
```javascript
{
  "mcpb_version": "0.1",
  "name": "my-extension",
  "version": "1.0.0",
  "description": "A simple MCP extension",
  "author": {
    "name": "Extension Author"
  },
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "API_KEY": "${user...key}"
      }
    }
  },
  "user_config": {
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": true
    }
  }
}
```
💡 举例说明：${user_config.api_key} 是一个模板变量。当 Claude Desktop 启动服务器时，它会自动将这个占位符替换为用户在配置界面中实际输入的 API Key 值。这样开发者就不需要在代码中硬编码敏感信息。
一个包含大部分可选字段的完整 manifest.json 可能如下所示：
```javascript
{
  "mcpb_version": "0.1",
  "name": "My MCP Extension",
  "display_name": "My Awesome MCP Extension",
  "version": "1.0.0",
  "description": "A brief description of what this extension does",
  "long_description": "A detailed description that can include multiple paragraphs explaining the extension's functionality, use cases, and features. It supports basic markdown.",
  "author": {
    "name": "Your Name",
    "email": "yourname@example.com",
    "url": "https://your-website.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/your-username/my-mcp-extension"
  },
  "homepage": "https://example.com/my-extension",
  "documentation": "https://docs.example.com/my-extension",
  "support": "https://github.com/your-username/my-mcp-extension/issues",
  "icon": "icon.png",
  "screenshots": [
    "assets/screenshots/screenshot1.png",
    "assets/screenshots/screenshot2.png"
  ],
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
      }
    }
  },
  "tools": [
    {
      "name": "search_files",
      "description": "Search for files in a directory"
    }
  ],
  "prompts": [
    {
      "name": "poetry",
      "description": "Have the LLM write poetry",
      "arguments": ["topic"],
      "text": "Write a creative poem about the following topic: ${arguments.topic}"
    }
  ],
  "tools_generated": true,
  "keywords": ["api", "automation", "productivity"],
  "license": "MIT",
  "compatibility": {
    "claude_desktop": ">=1.0.0",
    "platforms": ["darwin", "win32", "linux"],
    "runtimes": {
      "node": ">=16.0.0"
    }
  },
  "user_config": {
    "allowed_directories": {
      "type": "directory",
      "title": "Allowed Directories",
      "description": "Directories the server can access",
      "multiple": true,
      "required": true,
      "default": ["${HOME}/Desktop"]
    },
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": false
    },
    "max_file_size": {
      "type": "number",
      "title": "Maximum File Size (MB)",
      "description": "Maximum file size to process",
      "default": 10,
      "min": 1,
      "max": 100
    }
  }
}
```
要查看扩展和 manifest 的示例，请参阅 MCPB 仓库中的示例。
manifest.json 中所有必需和可选字段的完整规范可以在我们的开源工具链中找到。
#### 构建你的第一个扩展
让我们逐步将一个现有的 MCP 服务器打包为 Desktop Extension。我们将以一个简单的文件系统服务器为例。
首先，为你的服务器初始化一个 manifest：
```javascript
npx @anthropic-ai/mcpb init
```
这个交互式工具会询问关于你服务器的信息，并生成一个完整的 manifest.json。如果你想快速生成最基本的 manifest.json，可以使用 --yes 参数运行命令。
如果你的服务器需要用户输入（如 API Key 或允许访问的目录），请在 manifest 中声明：
```javascript
"user_config": {
  "allowed_directories": {
    "type": "directory",
    "title": "Allowed Directories",
    "description": "Directories the server can access",
    "multiple": true,
    "required": true,
    "default": ["${HOME}/Documents"]
  }
}
```
Claude Desktop 将会：
- 显示用户友好的配置界面
  - 在启用扩展之前验证输入
  - 安全存储敏感值
  - 根据开发者配置，将配置作为参数或环境变量传递给你的服务器
在下面的示例中，我们将用户配置作为环境变量传递，但它也可以作为参数传递。
```javascript
"server": {
  "type": "node",
  "entry_point": "server/index.js",
  "mcp_config": {
    "command": "node",
    "args": ["${__dirname}/server/index.js"],
    "env": {
      "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
    }
  }
}
```
将所有内容打包成一个 .mcpb 文件：
```javascript
npx @anthropic-ai/mcpb pack
```
此命令会：
1. 验证你的 manifest
  1. 生成 .mcpb 压缩包
将你的 .mcpb 文件拖入 Claude Desktop 的设置窗口。你会看到：
- 关于你扩展的人类可读信息
  - 所需的权限和配置
  - 一个简单的"安装"按钮
#### 高级功能
扩展可以适配不同的操作系统：
```javascript
"server": {
  "type": "node",
  "entry_point": "server/index.js",
  "mcp_config": {
    "command": "node",
    "args": ["${__dirname}/server/index.js"],
    "platforms": {
      "win32": {
        "command": "node.exe",
        "env": {
          "TEMP_DIR": "${TEMP}"
        }
      },
      "darwin": {
        "env": {
          "TEMP_DIR": "${TMPDIR}"
        }
      }
    }
  }
}
```
💡 术语解释：darwin 是 macOS 的内部系统名称（源自 Darwin 操作系统），win32 是 Windows 平台的标识符（即使 64 位系统也使用此名称），linux 则是 Linux 平台的标识符。
使用模板字面量处理运行时值：
- ${__dirname}：扩展的安装目录
  - ${user_config.key}：用户提供的配置
  - ${HOME}, ${TEMP}：系统环境变量
帮助用户提前了解扩展的能力：
```javascript
"tools": [
  {
    "name": "read_file",
    "description": "Read contents of a file"
  }
],
"prompts": [
  {
    "name": "code_review",
    "description": "Review code for best practices",
    "arguments": ["file_path"]
  }
]
```
#### 扩展目录
我们正在推出一个内置于 Claude Desktop 的精选扩展目录。用户可以浏览、搜索并一键安装——无需搜索 GitHub 或审查代码。
虽然我们预期 Desktop Extension 规范以及 Claude 在 macOS 和 Windows 上的实现会随时间不断演进，但我们期待看到扩展以各种富有创意的方式扩展 Claude 的能力。
提交你的扩展：
1. 确保它遵循提交表单中的指南
  1. 在 Windows 和 macOS 上进行跨平台测试
  1. 提交你的扩展
  1. 我们的团队将进行质量和安全审查
#### 构建开放生态系统
我们致力于围绕 MCP 服务器构建开放生态系统，并相信其被多个应用和服务广泛采用的能力造福了整个社区。秉承这一承诺，我们将 Desktop Extension 规范、工具链以及 Claude 在 macOS 和 Windows 上用于实现桌面扩展支持所使用的 Schema（模式定义）和关键函数进行开源。我们希望 MCPB 格式不仅能让本地 MCP 服务器在 Claude 中更具可移植性，也能在其他 AI 桌面应用中发挥作用。
我们正在开源的内容包括：
- 完整的 MCPB 规范
  - 打包和验证工具

## 通过 MCP 实现代码执行

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

[[claude-desktop-extensions]] | [[claude-code]] | [[tool-use]] | [[anthropic]]
