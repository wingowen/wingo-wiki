#!/usr/bin/env python3
"""
Build Script: src/concepts/ (flat) → docs/concepts/ (hierarchical)
              + mkdocs.yml generation
              + index.md generation

Wikilinks (flat) → Markdown relative links (hierarchical)
"""

import os
import re
import shutil
from pathlib import Path

WIKI = Path(os.path.expanduser("~/wingo-wiki"))
SRC_CONCEPTS = WIKI / "src" / "concepts"
DOCS_CONCEPTS = WIKI / "docs" / "concepts"
DOCS = WIKI / "docs"

# -------------------------------------------------------------------
# WIKILINK_MAP: wikilink stem → short_filename
# -------------------------------------------------------------------
WIKILINK_MAP = {
    "advanced-tool-use": "advanced-tool-use.md",
    "agent-architecture": "agent-architecture.md",
    "agent-framework-practice": "agent-framework-practice.md",
    "agent-framework-theory": "agent-framework-theory.md",
    "agent-skills": "agent-skills.md",
    "beyond-permission-prompts": "beyond-permission-prompts.md",
    "building-effective-agents": "building-effective-agents.md",
    "claude-agent-sdk": "claude-agent-sdk.md",
    "claude-code-best-practices": "claude-code-best-practices.md",
    "claude-desktop-extensions": "claude-desktop-extensions.md",
    "claude-postmortem": "claude-postmortem.md",
    "context-engineering": "context-engineering.md",
    "context-management": "context-management.md",
    "contextual-retrieval": "contextual-retrieval.md",
    "dual-memory-system": "dual-memory-system.md",
    "effective-context-engineering": "effective-context-engineering.md",
    "hyde": "hyde.md",
    "interview-agent-arch": "interview-agent-arch.md",
    "interview-context-mgmt": "interview-context-mgmt.md",
    "interview-hyde": "interview-hyde.md",
    "langgraph": "langgraph.md",
    "long-running-agents": "long-running-agents.md",
    "mcp": "mcp.md",
    "mcp-code-execution": "mcp-code-execution.md",
    "mcp-deep-dive": "mcp-deep-dive.md",
    "multi-agent": "multi-agent.md",
    "multi-agent-research": "multi-agent-research.md",
    "prompt-injection": "prompt-injection.md",
    "rag": "rag.md",
    "react": "react.md",
    "slash-commands": "slash-commands.md",
    "swe-bench": "swe-bench.md",
    "think-tool": "think-tool.md",
    "tool-use": "tool-use.md",
    "writing-effective-tools": "writing-effective-tools.md",
    "ai-agent": "ai-agent.md",
    "anthropic": "anthropic.md",
    "claude-code": "claude-code.md",
    "langgraph-vs-react": "langgraph-vs-react.md",
    "interview-overview": "interview-overview.md",
    "interview-qa-overview": "interview-qa-overview.md",
    "session-context": "session-context.md",
}

# -------------------------------------------------------------------
# CATEGORY_MAP: short_filename → (category, subcategory)
# -------------------------------------------------------------------
CATEGORY_MAP = {
    "agent-architecture.md": ("agent-architecture", "core"),
    "agent-framework-theory.md": ("agent-architecture", "core"),
    "interview-agent-arch.md": ("agent-architecture", "interview"),
    "agent-framework-practice.md": ("agent-architecture", "practice"),
    "building-effective-agents.md": ("agent-architecture", "practice"),
    "claude-agent-sdk.md": ("claude", "practice"),
    "claude-code-best-practices.md": ("claude", "practice"),
    "claude-desktop-extensions.md": ("claude", "practice"),
    "claude-postmortem.md": ("claude", "practice"),
    "context-engineering.md": ("context-engineering", "core"),
    "context-management.md": ("context-engineering", "core"),
    "interview-context-mgmt.md": ("context-engineering", "interview"),
    "effective-context-engineering.md": ("context-engineering", "practice"),
    "mcp.md": ("mcp", "core"),
    "mcp-code-execution.md": ("mcp", "practice"),
    "mcp-deep-dive.md": ("mcp", "practice"),
    "multi-agent.md": ("multi-agent", "core"),
    "multi-agent-research.md": ("multi-agent", "practice"),
    "langgraph.md": ("other", "core"),
    "prompt-injection.md": ("other", "core"),
    "react.md": ("other", "core"),
    "agent-skills.md": ("other", "practice"),
    "beyond-permission-prompts.md": ("other", "practice"),
    "dual-memory-system.md": ("other", "practice"),
    "long-running-agents.md": ("other", "practice"),
    "slash-commands.md": ("other", "practice"),
    "swe-bench.md": ("other", "practice"),
    "contextual-retrieval.md": ("rag", "core"),
    "hyde.md": ("rag", "core"),
    "rag.md": ("rag", "core"),
    "interview-hyde.md": ("rag", "interview"),
    "advanced-tool-use.md": ("tool-use", "core"),
    "tool-use.md": ("tool-use", "core"),
    "think-tool.md": ("tool-use", "practice"),
    "writing-effective-tools.md": ("tool-use", "practice"),
    "ai-agent.md": ("entities", ""),
    "anthropic.md": ("entities", ""),
    "claude-code.md": ("entities", ""),
    "langgraph-vs-react.md": ("comparisons", ""),
    "interview-overview.md": ("queries", ""),
    "interview-qa-overview.md": ("queries", ""),
    "session-context.md": ("queries", ""),
}


def rewrite_wikilinks(content, source_filename):
    """Convert [[wikilink]] or [[wikilink|display]] to markdown relative links."""
    def replacer(m):
        inner = m.group(1)
        if "|" in inner:
            link_part, display = inner.split("|", 1)
            link_part = link_part.strip()
            display = display.strip()
        else:
            link_part = inner.strip()
            display = link_part

        target_file = WIKILINK_MAP.get(link_part)
        if not target_file:
            return f"[[{link_part}]]"  # keep unknown

        source_cat, source_sub = CATEGORY_MAP.get(source_filename, ("", ""))
        target_cat, target_sub = CATEGORY_MAP.get(target_file, ("", ""))

        if source_sub == "":
            source_dir = Path(source_cat)
        else:
            source_dir = Path(source_cat) / source_sub

        if target_sub == "":
            target_dir = Path(target_cat)
        else:
            target_dir = Path(target_cat) / target_sub

        rel = os.path.relpath(target_dir / target_file, source_dir).replace("\\", "/")
        return f"[{display}]({rel})"

    return re.sub(r'\[\[([^\]]+)\]\]', replacer, content)


def get_title(src_file):
    """Extract title from frontmatter of a source file."""
    try:
        content = src_file.read_text()
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            for line in fm_match.group(1).split('\n'):
                if line.startswith('title:'):
                    title = line.split(':', 1)[1].strip().strip('"\'')
                    if '|' in title:
                        title = title.split('|')[0].strip()
                    return title
    except Exception:
        pass
    return src_file.stem.replace("-", " ").title()


# -------------------------------------------------------------------
# Step 0: Sync root-level wiki dirs → docs/ root (entities, comparisons, queries)
# These files also have wikilinks that need rewriting
# -------------------------------------------------------------------

print("=== Step 0: Syncing root wiki dirs → docs/ ===")
ROOT_SYNC = {
    "entities": "entities",
    "comparisons": "comparisons",
    "queries": "queries",
}
for rd in ["entities", "comparisons", "queries"]:
    src_dir = WIKI / rd
    dst_dir = DOCS / rd
    if src_dir.is_dir():
        dst_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        for src_file in src_dir.glob("*.md"):
            content = src_file.read_text()
            # Rewrite wikilinks for docs/ placement
            new_content = rewrite_wikilinks(content, src_file.name)
            dst_file = dst_dir / src_file.name
            dst_file.write_text(new_content)
            count += 1
        print(f"  {rd}/: {count} files synced (wikilinks rewritten)")

print()


# -------------------------------------------------------------------
# Step 1: Prepare docs/concepts
# -------------------------------------------------------------------

print("=== Step 1: Preparing docs/concepts ===")
for item in list(DOCS_CONCEPTS.iterdir()):
    if item.is_dir() and item.name not in [".", "skills"]:
        shutil.rmtree(item)
    elif item.is_file() and item.name not in ["index.md"]:
        item.unlink()

# Only create category dirs for actual concept categories (not entities/comparisons/queries)
concept_categories = {"agent-architecture", "claude", "context-engineering", "mcp", "multi-agent", "other", "rag", "tool-use"}
categories = concept_categories & set(v[0] for v in CATEGORY_MAP.values())
for cat in sorted(categories):
    cat_dir = DOCS_CONCEPTS / cat
    cat_dir.mkdir(parents=True, exist_ok=True)
    (cat_dir / "_index.md").write_text(
        f"---\ntitle: {cat.replace('-', ' ').title()}\n---\n\n# {cat.replace('-', ' ').title()}\n"
    )

subcats = set((v[0], v[1]) for v in CATEGORY_MAP.values() if v[1])
for cat, subcat in sorted(subcats):
    (DOCS_CONCEPTS / cat / subcat).mkdir(parents=True, exist_ok=True)

print(f"  Created {len(categories)} category dirs, {len(subcats)} subcategory dirs")


# -------------------------------------------------------------------
# Step 2: Process and copy src files → docs
# -------------------------------------------------------------------

print("\n=== Step 2: Rewriting wikilinks and copying to docs ===")
processed = []
unresolved = []

for src_file in sorted(SRC_CONCEPTS.glob("*.md")):
    short_name = src_file.name
    content = src_file.read_text()
    new_content = rewrite_wikilinks(content, short_name)

    cat, subcat = CATEGORY_MAP.get(short_name, (None, None))
    if cat is None:
        continue

    if subcat:
        out_dir = DOCS_CONCEPTS / cat / subcat
    else:
        out_dir = DOCS_CONCEPTS / cat

    out_file = out_dir / short_name
    out_file.write_text(new_content)

    unresolved_in_file = re.findall(r'\[\[([^\]]+)\]\]', new_content)
    if unresolved_in_file:
        unresolved.append((short_name, unresolved_in_file))

    processed.append(short_name)
    print(f"  {short_name} → {cat}/{subcat}/{short_name}" if subcat else f"  {short_name} → {cat}/{short_name}")

print(f"\n  Processed: {len(processed)} files")
if unresolved:
    print(f"  WARNING: {len(unresolved)} files have unresolved wikilinks:")
    for fname, links in unresolved[:5]:
        print(f"    {fname}: {links}")


# -------------------------------------------------------------------
# Step 3: Generate mkdocs.yml (manual YAML)
# -------------------------------------------------------------------

print("\n=== Step 3: Generating mkdocs.yml ===")

nav_lines = []
nav_lines.append("site_name: Wingo Wiki")
nav_lines.append("site_url: https://wingo-wiki.netlify.app")
nav_lines.append("site_description: Wingo's personal wiki")
nav_lines.append("")
nav_lines.append("theme:")
nav_lines.append("  name: material")
nav_lines.append("  features:")
nav_lines.append("    - navigation.tabs")
nav_lines.append("    - navigation.path")
nav_lines.append("    - navigation.indexes")
nav_lines.append("    - toc.integrate")
nav_lines.append("    - search.suggest")
nav_lines.append("    - search.highlight")
nav_lines.append("  palette:")
nav_lines.append("    scheme: slate")
nav_lines.append("    primary: indigo")
nav_lines.append("    accent: indigo")
nav_lines.append("")
nav_lines.append("plugins:")
nav_lines.append("  - search")
nav_lines.append("  - roamlinks")
nav_lines.append("  - glightbox")
nav_lines.append("")
nav_lines.append("markdown_extensions:")
nav_lines.append("  - pymdownx.highlight")
nav_lines.append("  - pymdownx.superfences")
nav_lines.append("  - pymdownx.tasklist")
nav_lines.append("  - pymdownx.tabbed")
nav_lines.append("  - admonition")
nav_lines.append("  - pymdownx.details")
nav_lines.append("  - attr_list")
nav_lines.append("  - footnotes")
nav_lines.append("")
nav_lines.append("extra_javascript:")
nav_lines.append("  - https://fastly.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js")
nav_lines.append("  - https://fastly.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js")
nav_lines.append("  - assets/javascripts/graph.js")
nav_lines.append("")
nav_lines.append("extra_css:")
nav_lines.append("  - assets/stylesheets/graph.css")
nav_lines.append("")

# Build nav
nav_lines.append("nav:")

# Concepts: group by category with sub-sections
cat_display = {
    "agent-architecture": "Agent Architecture",
    "claude": "Claude",
    "context-engineering": "Context Engineering",
    "mcp": "MCP",
    "multi-agent": "Multi-Agent",
    "other": "其他",
    "rag": "RAG",
    "tool-use": "Tool Use",
}
subcat_display = {
    "core": "核心概念",
    "interview": "面试相关",
    "practice": "实践应用",
}

# Concepts section
nav_lines.append("  - Concepts:")
for cat in ["agent-architecture", "claude", "context-engineering", "mcp", "multi-agent", "rag", "tool-use", "other"]:
    cat_files = [(sn, get_title(SRC_CONCEPTS / sn)) for sn, (c, sc) in CATEGORY_MAP.items() if c == cat]
    if not cat_files:
        continue
    cat_label = cat_display.get(cat, cat.replace("-", " ").title())
    nav_lines.append(f"    - {cat_label}:")

    # Group by subcategory
    by_subcat = {}
    for sn, title in cat_files:
        _, sc = CATEGORY_MAP[sn]
        if sc not in by_subcat:
            by_subcat[sc] = []
        by_subcat[sc].append((sn, title))

    for sc in ["core", "interview", "practice"]:
        if sc not in by_subcat:
            continue
        sc_label = subcat_display.get(sc, sc)
        nav_lines.append(f"      - {sc_label}:")
        for sn, title in sorted(by_subcat[sc], key=lambda x: x[1]):
            cat_dir = CATEGORY_MAP[sn][1] if CATEGORY_MAP[sn][1] else ""
            path_sn = sn[:-3] if sn.endswith(".md") else sn
            path = f"concepts/{cat}/{cat_dir}/{path_sn}" if cat_dir else f"concepts/{cat}/{path_sn}"
            nav_lines.append(f"        - \"{title}\": {path}")

# Comparisons
nav_lines.append("  - Comparisons:")
nav_lines.append("    - LangGraph vs React: comparisons/langgraph-vs-react.md")

# Entities
nav_lines.append("  - Entities:")
for sn in ["ai-agent.md", "anthropic.md", "claude-code.md"]:
    title = get_title(WIKI / "entities" / sn)
    nav_lines.append(f"    - \"{title}\": entities/{sn}")

# Queries
nav_lines.append("  - Queries:")
for sn in ["interview-overview.md", "interview-qa-overview.md", "session-context.md"]:
    title = get_title(WIKI / "queries" / sn)
    nav_lines.append(f"    - \"{title}\": queries/{sn}")

mkdocs_path = WIKI / "mkdocs.yml"
mkdocs_path.write_text("\n".join(nav_lines))
print(f"  Written mkdocs.yml")


# -------------------------------------------------------------------
# Step 4: Generate docs/index.md
# -------------------------------------------------------------------

print("\n=== Step 4: Generating docs/index.md ===")

total = len(processed) + 3 + 1 + 3
lines = []
lines.append("# Wingo Wiki")
lines.append("")
lines.append("> AI Agent 技术与工程实践 Wiki | LLM Wiki 规范 + MkDocs 发布")
lines.append(f"> Last updated: 2026-04-17 | Total pages: {total}")
lines.append("")
lines.append("## Entities")
lines.append("")

for sn in ["ai-agent.md", "anthropic.md", "claude-code.md"]:
    title = get_title(WIKI / "entities" / sn)
    lines.append(f"- [[{title}]]")

lines.append("")
lines.append("## Concepts")
lines.append("")

for cat in ["agent-architecture", "claude", "context-engineering", "mcp", "multi-agent", "rag", "tool-use", "other"]:
    cat_files = [(sn, get_title(SRC_CONCEPTS / sn)) for sn, (c, sc) in CATEGORY_MAP.items() if c == cat]
    if not cat_files:
        continue
    cat_label = cat_display.get(cat, cat.replace("-", " ").title())
    lines.append(f"### {cat_label}")
    lines.append("")
    for sn, title in sorted(cat_files, key=lambda x: x[1]):
        lines.append(f"- [[{title}]]")

lines.append("")
lines.append("## Comparisons")
lines.append("")
for sn in ["langgraph-vs-react.md"]:
    title = get_title(WIKI / "comparisons" / sn)
    lines.append(f"- [[{title}]]")

lines.append("")
lines.append("## Queries")
lines.append("")
for sn in ["interview-overview.md", "interview-qa-overview.md", "session-context.md"]:
    title = get_title(WIKI / "queries" / sn)
    lines.append(f"- [[{title}]]")

# Build index content and rewrite wikilinks
index_content = "\n".join(lines)
# Rewrite wikilinks for index.md (located at docs/ root)
INDEX_WIKILINK_MAP = {
    "AI Agent": "entities/ai-agent/",
    "Anthropic": "entities/anthropic/",
    "Claude Code": "entities/claude-code/",
    "AI Agent 框架实践篇": "concepts/agent-architecture/practice/agent-framework-practice/",
    "AI Agent 框架理论篇": "concepts/agent-architecture/core/agent-framework-theory/",
    "Agent 架构设计：从传统开发到智能体": "concepts/agent-architecture/core/agent-architecture/",
    "构建高效 Agent": "concepts/agent-architecture/practice/building-effective-agents/",
    "Claude Code：Agent 编程最佳实践": "concepts/claude/practice/claude-code-best-practices/",
    "三个近期问题的故障复盘": "concepts/claude/practice/claude-postmortem/",
    "使用 Claude Agent SDK 构建 Agent": "concepts/claude/practice/claude-agent-sdk/",
    "桌面扩展：Claude Desktop 一键安装 MCP 服务器": "concepts/claude/practice/claude-desktop-extensions/",
    "AI Agent 的有效上下文工程": "concepts/context-engineering/practice/effective-context-engineering/",
    "Context Engineering": "concepts/context-engineering/core/context-engineering/",
    "上下文管理：短期记忆与长期记忆": "concepts/context-engineering/core/context-management/",
    "MCP": "concepts/mcp/core/mcp/",
    "MCP 核心原理": "concepts/mcp/practice/mcp-deep-dive/",
    "通过 MCP 实现代码执行：构建更高效的 Agent": "concepts/mcp/practice/mcp-code-execution/",
    "Multi-Agent": "concepts/multi-agent/core/multi-agent/",
    "我们如何构建多 Agent 研究系统": "concepts/multi-agent/practice/multi-agent-research/",
    "HyDE 假设文档嵌入与高级检索策略": "concepts/rag/core/hyde/",
    "RAG 检索增强生成：从分块到检索": "concepts/rag/core/rag/",
    "介绍上下文检索": "concepts/rag/core/contextual-retrieval/",
    "Think 工具：让 Claude 在复杂工具使用场景中停下来思考": "concepts/tool-use/practice/think-tool/",
    "Tool Use": "concepts/tool-use/core/tool-use/",
    "在 Claude 开发者平台引入高级工具使用": "concepts/tool-use/core/advanced-tool-use/",
    "用 Agent 为 Agent 编写高效工具": "concepts/tool-use/practice/writing-effective-tools/",
    "LangGraph": "concepts/other/core/langgraph/",
    "ReAct": "concepts/other/core/react/",
    "双层记忆系统与 Dream 管理知识文件的具体实现分析": "concepts/other/practice/dual-memory-system/",
    "构建长时间运行 Agent 的有效 Harness": "concepts/other/practice/long-running-agents/",
    "用 Agent Skills 装备 Agent 应对真实世界": "concepts/other/practice/agent-skills/",
    "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩": "concepts/other/practice/swe-bench/",
    "系统提示词注入分析": "concepts/other/core/prompt-injection/",
    "自定义 Slash 命令 Hook 设计方案": "concepts/other/practice/slash-commands/",
    "超越权限提示：让 Claude Code 更安全更自主": "concepts/other/practice/beyond-permission-prompts/",
    "Interview Agent Arch": "concepts/agent-architecture/interview/interview-agent-arch/",
    "Interview Context Mgmt": "concepts/context-engineering/interview/interview-context-mgmt/",
    "Interview Hyde": "concepts/rag/interview/interview-hyde/",
    "LangGraph 核心原理与 ReAct 对比": "comparisons/langgraph-vs-react/",
    "AI Agent 面试复盘总览": "queries/interview-overview/",
    "【面试复盘】AI Agent 面试突击问答清单（总览）": "queries/interview-qa-overview/",
    "Session Context 影响技能选择的问题分析与解决方案": "queries/session-context/",
}

def rewrite_index_wikilinks(content):
    def replacer(m):
        inner = m.group(1)
        if "|" in inner:
            link_part, display = inner.split("|", 1)
            link_part = link_part.strip()
            display = display.strip()
        else:
            link_part = inner.strip()
            display = link_part
        target = INDEX_WIKILINK_MAP.get(link_part)
        if target:
            return f"[{display}]({target})"
        return f"[[{link_part}]]"
    return re.sub(r'\[\[([^\]]+)\]\]', replacer, content)

index_content = rewrite_index_wikilinks(index_content)

lines = index_content.split("\n")

if len(lines) > 100:
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Total**: {total} pages | **Source**: `src/concepts/` (flat, LLM Wiki standard)")
    lines.append("")
    lines.append("**Build**: `python build.py` → generates `docs/concepts/` for MkDocs publishing")

index_path = WIKI / "docs" / "index.md"
index_path.write_text("\n".join(lines))
print(f"  Written docs/index.md ({total} pages)")


# -------------------------------------------------------------------
# Step 5: Summary
# -------------------------------------------------------------------

print(f"""
=== Build Complete ===

Source:      src/concepts/ ({len(processed)} flat .md files)
Published:   docs/concepts/ (hierarchical for MkDocs)
Nav:         mkdocs.yml (auto-generated)
Index:       docs/index.md (auto-generated)

To publish:
  1. cd ~/wingo-wiki && python build.py
  2. mkdocs build
  3. git push → Netlify deploys
""")
