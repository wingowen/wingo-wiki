# Wiki Schema

## Domain
AI Agent 技术与工程实践 — 涵盖 Agent 架构、工具使用、记忆系统、RAG、Multi-Agent、Anthropic 技术栈等

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `agent-architecture-design.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
---
```

## Tag Taxonomy
定义以下顶层标签（Tag Taxonomy）：

### 人物/组织 (People/Orgs)
- person: 人物
- company: 公司
- lab: 研究实验室
- open-source: 开源组织

### 技术概念 (Technical)
- model: 模型架构
- architecture: 系统架构
- training: 训练技术
- fine-tuning: 微调
- inference: 推理优化
- optimization: 优化技术
- hyde: 假设文档嵌入
- langgraph: LangGraph 框架
- mcp: MCP 协议
- react: ReAct 推理行动框架

### Agent 相关 (Agent)
- agent: Agent 通用概念
- tool-use: 工具使用
- memory: 记忆系统
- rag: RAG 检索增强
- multi-agent: 多智能体
- planning: 规划能力
- reasoning: 推理能力
- claude-code: Claude Code

### 应用场景 (Applications)
- benchmark: 基准测试
- evaluation: 评估方法
- productivity: 生产力工具
- development: 开发工具

### 平台/框架 (Platforms)
- anthropic: Anthropic 相关

### 文档类型 (Doc Types)
- interview: 面试复盘
- translation: 翻译文档
- original: 原创内容
- summary: 摘要总结
- analysis: 分析报告
- query: 查询结果

### 元标签 (Meta)
- comparison: 对比分析
- timeline: 时间线
- controversy: 争议讨论
- prediction: 预测展望

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
