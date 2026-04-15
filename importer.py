#!/usr/bin/env python3
"""Process Notion pages and create wiki files"""
import os
import re
from datetime import datetime

WIKI = os.path.expanduser("~/wiki")

# Page metadata extracted from Notion API results
PAGES = [
    {
        "id": "34367b21-8207-8163-9cdf-c8c77b1efa54",
        "title": "【面试专题】Agent 架构设计：从传统开发到智能体",
        "created": "2026-04-15",
        "tags": ["面试复盘", "AI Agent", "Agent架构", "用户画像", "推荐系统"],
        "type": "summary",
        "category": "concepts"
    },
    {
        "id": "34367b21-8207-818d-9eb8-fb9c821dbd20",
        "title": "【面试专题】HyDE 假设文档嵌入与高级检索策略",
        "created": "2026-04-15",
        "tags": ["面试复盘", "AI Agent", "HyDE", "RAG", "Query Rewriting"],
        "type": "concept",
        "category": "concepts"
    },
    {
        "id": "34367b21-8207-818e-a7de-d00cd93fab00",
        "title": "【面试专题】RAG 检索增强生成：从分块到检索",
        "created": "2026-04-15",
        "tags": ["面试复盘", "AI Agent", "RAG", "向量检索", "Chunking"],
        "type": "concept",
        "category": "concepts"
    },
    {
        "id": "34367b21-8207-81c6-8eed-f5368d5630dd",
        "title": "【面试专题】上下文管理：短期记忆与长期记忆",
        "created": "2026-04-15",
        "tags": ["面试复盘", "AI Agent", "Context Engineering", "Checkpointer", "RAG"],
        "type": "concept",
        "category": "concepts"
    },
    {
        "id": "34367b21-8207-81b2-9f8b-c1218f7b3104",
        "title": "【面试专题】LangGraph 核心原理与 ReAct 对比",
        "created": "2026-04-15",
        "tags": ["面试复盘", "AI Agent", "LangGraph", "ReAct", "State管理"],
        "type": "comparison",
        "category": "comparisons"
    },
    {
        "id": "34367b21-8207-81e2-bc9c-f119f7ae87f6",
        "title": "【面试复盘】AI Agent 面试突击问答清单（总览）",
        "created": "2026-04-15",
        "tags": ["面试复盘", "AI Agent", "LangGraph", "RAG", "HyDE"],
        "type": "summary",
        "category": "queries"
    },
    {
        "id": "34367b21-8207-8106-9972-f0d42cf861ef",
        "title": "详尽地带你从零开始设计实现一个 AI Agent 框架",
        "created": "2026-04-13",
        "tags": ["腾讯技术工程", "AI Agent", "框架设计", "ReAct", "Context Engineering"],
        "type": "concept",
        "category": "concepts"
    },
    {
        "id": "34367b21-8207-8140-9199-e7fefb5ffb3c",
        "title": "系统提示词注入分析",
        "created": "2026-04-15",
        "tags": ["Nanobot", "提示词", "分析"],
        "type": "analysis",
        "category": "concepts"
    },
    {
        "id": "34367b21-8207-81d2-afd3-cd5fe531fbc6",
        "title": "自定义 Slash 命令 Hook 设计方案",
        "created": "2026-04-15",
        "tags": ["Slash命令", "Hook", "设计", "Nanobot"],
        "type": "concept",
        "category": "concepts"
    },
    {
        "id": "34367b21-8207-81fe-b72e-d5cd215313a6",
        "title": "Session Context 影响技能选择的问题分析与解决方案",
        "created": "2026-04-15",
        "tags": ["Session Context", "技能选择", "优化", "Nanobot"],
        "type": "analysis",
        "category": "queries"
    },
    {
        "id": "34267b21-8207-81a8-9d00-fff6df2ade12",
        "title": "我们如何构建多 Agent 研究系统 | How we built our multi-agent research system",
        "created": "2025-06-13",
        "tags": ["Anthropic", "Agent", "Multi-Agent"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-8199-9743-c072860e6ac1",
        "title": "AI Agent 的有效上下文工程 | Effective context engineering for AI agents",
        "created": "2025-09-29",
        "tags": ["Anthropic", "Context Engineering", "Agent"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-812d-8ba2-e62bfbdca0aa",
        "title": "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 | Raising the bar on SWE-bench Verified",
        "created": "2025-01-06",
        "tags": ["Anthropic", "Benchmark", "Evaluation"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-813f-b0e2-cae2d942f74c",
        "title": "介绍上下文检索 | Introducing Contextual Retrieval",
        "created": "2024-09-19",
        "tags": ["Anthropic", "RAG", "Retrieval"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-819b-b24d-e80f17fa0201",
        "title": "三个近期问题的故障复盘 | A postmortem of three recent issues",
        "created": "2025-09-17",
        "tags": ["Anthropic", "Infrastructure", "Engineering"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-8197-b8ca-d8f11d3ca649",
        "title": "桌面扩展：Claude Desktop 一键安装 MCP 服务器 | Desktop Extensions",
        "created": "2025-06-26",
        "tags": ["Anthropic", "MCP", "Claude Desktop"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-8192-a0d4-cff1c99ff3d2",
        "title": "Claude Code：Agent 编程最佳实践 | Claude Code best practices",
        "created": "2025-04-18",
        "tags": ["Anthropic", "Claude Code", "Agent"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-8138-b312-c3d319f17b5a",
        "title": "通过 MCP 实现代码执行：构建更高效的 Agent | Code execution with MCP",
        "created": "2025-11-04",
        "tags": ["Anthropic", "MCP", "Agent"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-81cb-b299-d66221d93419",
        "title": "超越权限提示：让 Claude Code 更安全更自主 | Beyond permission prompts",
        "created": "2025-10-20",
        "tags": ["Anthropic", "Security", "Claude Code"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-81a2-b94a-f7ba3a444a5f",
        "title": "在 Claude 开发者平台引入高级工具使用 | Introducing advanced tool use on the Claude Developer Platform",
        "created": "2025-11-24",
        "tags": ["Anthropic", "Tool Use", "Agent"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-813f-9e2a-fe299323ddce",
        "title": "用 Agent 为 Agent 编写高效工具 | Writing effective tools for agents — with agents",
        "created": "2025-09-11",
        "tags": ["Anthropic", "Tool Use", "Agent"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-813d-bba1-e5e25ef455a2",
        "title": "\"Think\" 工具：让 Claude 在复杂工具使用场景中停下来思考 | The think tool",
        "created": "2025-03-20",
        "tags": ["Anthropic", "Tool Use", "Agent", "Reasoning"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-8154-b45a-d542679a17a0",
        "title": "用 Agent Skills 装备 Agent 应对真实世界 | Equipping agents with Agent Skills",
        "created": "2025-10-16",
        "tags": ["Anthropic", "Agent", "Skills"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-8141-8638-c436b190d370",
        "title": "使用 Claude Agent SDK 构建 Agent | Building agents with the Claude Agent SDK",
        "created": "2025-09-29",
        "tags": ["Anthropic", "Agent", "SDK"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-81b1-a412-df36f5a33826",
        "title": "构建高效 Agent | Building effective agents",
        "created": "2024-12-19",
        "tags": ["Anthropic", "Agent", "Architecture", "Best Practices"],
        "type": "translation",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-8131-929e-fb39d34023b5",
        "title": "构建长时间运行 Agent 的有效 Harness",
        "created": "2026-04-14",
        "tags": ["Anthropic"],
        "type": "concept",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-81a2-b887-ec73bb83404c",
        "title": "双层记忆系统与 Dream 管理知识文件的具体实现分析",
        "created": "2026-04-13",
        "tags": ["记忆系统", "文档", "技术"],
        "type": "analysis",
        "category": "concepts"
    },
    {
        "id": "34267b21-8207-819b-b24d-e80f17fa0201",
        "title": "三个近期问题的故障复盘 | A postmortem of three recent issues",
        "created": "2025-09-17",
        "tags": ["Anthropic", "Infrastructure", "Engineering"],
        "type": "translation",
        "category": "concepts"
    }
]

def slugify(title):
    """Convert title to a URL-safe slug"""
    # Remove Chinese brackets and content
    slug = re.sub(r'[\[\]【】\(\)]', '', title)
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-').lower()
    # Truncate
    if len(slug) > 60:
        slug = slug[:60]
    return slug

def create_wikilinks(tags):
    """Generate wikilinks from tags"""
    links = []
    tag_to_page = {
        "AI Agent": "[[AI Agent]]",
        "Agent": "[[Agent]]",
        "Agent架构": "[[Agent 架构设计]]",
        "Anthropic": "[[Anthropic]]",
        "RAG": "[[RAG]]",
        "LangGraph": "[[LangGraph]]",
        "ReAct": "[[ReAct]]",
        "MCP": "[[MCP]]",
        "Claude Code": "[[Claude Code]]",
        "Context Engineering": "[[Context Engineering]]",
        "Tool Use": "[[Tool Use]]",
        "Multi-Agent": "[[Multi-Agent]]",
        "记忆系统": "[[记忆系统]]",
        "面试复盘": "[[面试复盘]]",
        "Benchmark": "[[Benchmark]]",
        "HyDE": "[[HyDE]]",
        "SDK": "[[Claude Agent SDK]]",
        "Skills": "[[Agent Skills]]",
        "Security": "[[Security]]",
        "Evaluation": "[[Evaluation]]",
        "Infrastructure": "[[Infrastructure]]",
        "Engineering": "[[Engineering]]",
        "Chunking": "[[Chunking]]",
        "向量检索": "[[向量检索]]",
        "Query Rewriting": "[[Query Rewriting]]",
        "State管理": "[[State 管理]]",
        "Checkpointer": "[[Checkpointer]]",
        "腾讯技术工程": "[[腾讯技术工程]]",
        "框架设计": "[[框架设计]]",
        "提示词": "[[提示词]]",
        "Slash命令": "[[Slash 命令]]",
        "Hook": "[[Hook]]",
        "Nanobot": "[[Nanobot]]",
        "Session Context": "[[Session Context]]",
        "技能选择": "[[技能选择]]",
        "Best Practices": "[[Best Practices]]",
        "Architecture": "[[Architecture]]",
        "Reasoning": "[[Reasoning]]",
        "Retrieval": "[[Retrieval]]",
        "分析": "[[分析]]",
        "设计": "[[设计]]",
        "优化": "[[优化]]",
        "文档": "[[文档]]",
        "技术": "[[技术]]",
        "推荐系统": "[[推荐系统]]",
        "用户画像": "[[用户画像]]",
    }
    for tag in tags:
        if tag in tag_to_page:
            links.append(tag_to_page[tag])
    return links

# Generate wiki pages
index_entries = []
log_entries = []

for page in PAGES:
    slug = slugify(page['title'])
    category = page['category']
    
    # Create page path
    if category == 'entities':
        path = f"{WIKI}/entities/{slug}.md"
    elif category == 'comparisons':
        path = f"{WIKI}/comparisons/{slug}.md"
    elif category == 'queries':
        path = f"{WIKI}/queries/{slug}.md"
    else:
        path = f"{WIKI}/concepts/{slug}.md"
    
    # Create wikilinks
    wikilinks = create_wikilinks(page['tags'])
    wikilinks_text = '\n'.join(wikilinks) if wikilinks else '（无相关链接）'
    
    # Frontmatter
    frontmatter = f"""---
title: "{page['title']}"
created: {page['created']}
updated: {page['created']}
type: {page['type']}
tags: [{', '.join(page['tags'])}]
sources: []
notion_id: {page['id']}
---

# {page['title']}
"""
    
    # Content placeholder (actual content would need the full Notion blocks)
    content = f"""
## 概述

本文来自 Notion 总看板，记录于 {page['created']}。

**标签:** {', '.join(['`'+t+'`' for t in page['tags']])}  
**类型:** {page['type']}  
**分类:** {category}

## 核心要点

> 此页面内容待从 Notion 完整导入。原始页面 ID: `{page['id']}`

## 相关链接

{wikilinks_text}

"""

    # Write file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    
    # Add to index
    index_entries.append({
        'title': page['title'],
        'path': path,
        'tags': page['tags'],
        'type': page['type'],
        'created': page['created']
    })
    
    print(f"Created: {path}")

# Create index.md
index_md = """# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Last updated: 2026-04-15 | Total pages: {total}

## Concepts

""".format(total=len(index_entries))

for entry in sorted(index_entries, key=lambda x: x['title']):
    title = entry['title']
    tags = ', '.join(entry['tags'][:3])
    index_md += f"- [[{title}]] — {tags}\n"

index_md += """

## Comparisons



## Queries



## Entities



"""

with open(f"{WIKI}/index.md", 'w', encoding='utf-8') as f:
    f.write(index_md)

# Create log.md
log_md = """# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-15] ingest | Wiki initialized from Notion 总看板
- Domain: AI Agent 技术与工程实践
- Structure created with SCHEMA.md, index.md, log.md
- Imported 28 pages from Notion database

"""

with open(f"{WIKI}/log.md", 'w', encoding='utf-8') as f:
    f.write(log_md)

print(f"\n✓ Created {len(index_entries)} wiki pages")
print(f"✓ Created index.md")
print(f"✓ Created log.md")
print(f"\nWiki location: {WIKI}")
