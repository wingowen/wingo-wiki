# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-15] create | Wiki initialized
- Domain: AI Agent 技术与工程实践
- Structure created with SCHEMA.md, index.md, log.md
- Source: Notion 总看板 (28 pages)

## [2026-04-15] ingest | Notion pages imported
- Imported 28 pages from Notion database "总看板"
- Created entity pages: AI Agent, Anthropic, Claude Code
- Created concept pages: LangGraph, RAG, MCP, ReAct, Multi-Agent, Context Engineering, Tool Use
- Created comparison pages: LangGraph vs ReAct
- Created index.md with full catalog
- All pages linked with [[wikilinks]]

## [2026-04-15] create | Core entity pages
- ai-agent.md: AI Agent 核心概念和架构模式
- anthropic.md: Anthropic 公司介绍
- claude-code.md: Claude Code 工具介绍
- tool-use.md: Tool Use 最佳实践
- langgraph.md: LangGraph 框架介绍
- rag.md: RAG 技术概览
- mcp.md: MCP 协议介绍
- react.md: ReAct 框架介绍
- multi-agent.md: Multi-Agent 系统介绍
- context-engineering.md: Context Engineering 概念

## [2026-04-15] create | Comparison pages
- comparisons/langgraph-vs-react.md: LangGraph 与 ReAct 对比分析

## [2026-04-15] lint | Wiki 审核修复
- 审核发现：44页全部孤立 + 25条broken wikilinks + 18页超大 + 标签体系混乱
- 执行修复：
  - 重命名 29 个超长中文文件名为规范短名称（如 rag.md, mcp.md, langgraph.md）
  - 修正 frontmatter type 污染（6个页面）
  - 全文替换 71 条 wikilinks，全部指向正确文件名
  - 移除 3 条无目标页的失效链接（Planning/Reasoning/Security）
  - 补充交叉引用：39 个页面新增 wikilinks outbound
  - 归档 1 个重复文件（我们如何构建多agent研究系统）至 _archive/
  - 重建 index.md，43 页全部在索引中
- 最终状态：43页 | 155条 wikilinks | 0条broken | 0个orphan | 0条missing in index

## [2026-04-15] update | 超大页面拆分 + Tag 体系规范化
- 18 个超大页面（>200行）处理结果：
  - `agent-framework-from-scratch`(647行) → 拆分为 `agent-framework-theory`(170行) + `agent-framework-practice`(488行)
  - `mcp-deep-dive`(581行) 保留，内容覆盖 MCP 核心协议+桌面扩展+代码执行三部分
  - 其余 16 个页面为内聚翻译/分析文章，维持现状不强行拆分
- Tag 体系规范化：43 页全量标签修正
  - 移除所有未定义标签（大小写错误如"Anthropic"→"anthropic"，中文标签如"面试复盘"→"interview"）
  - 统一为 SCHEMA.md taxonomy 中的标准标签
- 修复指向已归档页面的 wikilinks：`ai-agent`、`agent-framework-practice` → `agent-framework-theory`
- 重建 index.md：44 页全部在索引中
- 当前状态：44页 | 0条broken | 0个orphan | Tag体系规范
## [2026-04-15] update | 超大页面拆分 + Tag体系规范化 + 链接格式修复
- 18个超大页面处理：
  - `agent-framework-from-scratch`(647行) → 拆为 `agent-framework-theory`(170行) + `agent-framework-practice`(488行)
  - `mcp-deep-dive`(581行) 等其余16页内容内聚，保留不拆分
- 批量修复 wikilink 格式：9个文件的多个重复 ## 相关链接 section 合并去重
- Tag体系全量规范化：所有43页标签映射到SCHEMA taxonomy（含react/langgraph/mcp/hyde等）
- SCHEMA.md taxonomy 去重补全：添加react/query标签
- 修复指向已归档页面的wikilinks
- 当前：44页 | 161条wikilinks | 0 broken | 0 orphan | Tag体系规范

## [2026-04-15] lint | Wiki 审查 + 自动修复
- 审查项目：broken links, orphans, frontmatter, page size, tag taxonomy
- 实际状态：0 broken links | 0 orphans | Tag体系规范 | log.md 健康
- 发现问题：18 个 frontmatter type 污染（translation/analysis/framework → concept）
- 自动修复：18 个文件 type 已全部修正为 `concept`
- 剩余问题：18 个超大页面（>200行），建议手动拆分或接受现状（翻译/分析文章内聚）

## [2026-04-15] restructure | Layer 1/2 重构 - 补全 raw/ + 精简 Layer 2
### 背景
根据 LLM Wiki 正确架构：Layer 1 (raw/) 存放原始素材，Layer 2 (concepts/) 存放精简知识点。原 wiki 将完整翻译文章塞入 concepts/，raw/ 完全为空。

### 执行操作
- **Layer 1 补全**：30 篇原始翻译/分析文章迁移到 `raw/articles/`
- **Layer 2 精简**：30 个 concepts/ 页面从 100-581 行压缩至 27-70 行
- **删除重复页面**：`interview-rag.md`（与 `rag.md` 内容重叠）已删除
- **删除重复文件**：`comparisons/interview-langgraph-react.md`（与 `langgraph-vs-react.md` 重复）
- **修复损坏 frontmatter**：`queries/interview-overview.md`、`queries/interview-qa-overview.md` 损坏 frontmatter 已修复
- **修复残留引用**：替换 `interview-langgraph-react` → `langgraph-vs-react` 引用
- **清理临时目录**：`temp_raw/` 已删除

### 当前状态
- **raw/articles/**: 30 个文件（原始不可变素材）
- **concepts/**: 36 个精简知识点页（27-147 行）
- **entities/**: 3 个实体页（AI Agent, Anthropic, Claude Code）
- **comparisons/**: 1 个对比页（LangGraph vs ReAct）
- **queries/**: 3 个查询/复盘页
- **Total wiki pages**: 43 页
- **0 broken wikilinks | 0 orphan pages | Tag 体系规范**

