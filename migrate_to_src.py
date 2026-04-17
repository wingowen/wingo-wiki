#!/usr/bin/env python3
"""
Migrate: docs/concepts/ (hierarchical) → src/concepts/ (flat, LLM Wiki standard)

扁平化规则：
- core/category.md (如 mcp/core/mcp.md) → category.md (如 mcp.md)
- 其他文件保留原名（如 rag/interview/interview-hyde.md → interview-hyde.md）

同时生成 WIKILINK_MAP 用于后续 wikilink 重写。
"""

import os
import shutil
from pathlib import Path

WIKI = Path(os.path.expanduser("~/wingo-wiki"))
DOCS_CONCEPTS = WIKI / "docs" / "concepts"
SRC_CONCEPTS = WIKI / "src" / "concepts"

# -------------------------------------------------------------------
# 1. 迁移文件
# -------------------------------------------------------------------

shutil.rmtree(SRC_CONCEPTS, ignore_errors=True)
SRC_CONCEPTS.mkdir(parents=True)

# category → core short name
CORE_SHORT = {
    "agent-architecture": "agent-architecture.md",
    "claude": "claude.md",
    "context-engineering": "context-engineering.md",
    "mcp": "mcp.md",
    "multi-agent": "multi-agent.md",
    "rag": "rag.md",
    "tool-use": "tool-use.md",
}

# For "other" category, no single core page, so we map differently
# other has no category-level core file, so langgraph.md etc stay as-is

FLATTEN_RULES = {
    # (category, subdir, filename) → short_name
    # agent-architecture
    ("agent-architecture", "core", "agent-architecture.md"): "agent-architecture.md",
    ("agent-architecture", "core", "agent-framework-theory.md"): "agent-framework-theory.md",
    ("agent-architecture", "interview", "interview-agent-arch.md"): "interview-agent-arch.md",
    ("agent-architecture", "practice", "agent-framework-practice.md"): "agent-framework-practice.md",
    ("agent-architecture", "practice", "building-effective-agents.md"): "building-effective-agents.md",
    # claude (no core/ subdir, all in practice/)
    ("claude", "practice", "claude-agent-sdk.md"): "claude-agent-sdk.md",
    ("claude", "practice", "claude-code-best-practices.md"): "claude-code-best-practices.md",
    ("claude", "practice", "claude-desktop-extensions.md"): "claude-desktop-extensions.md",
    ("claude", "practice", "claude-postmortem.md"): "claude-postmortem.md",
    # Also handle if there's a claude/core subdir (there isn't, but we handle it gracefully)
    # context-engineering
    ("context-engineering", "core", "context-engineering.md"): "context-engineering.md",
    ("context-engineering", "core", "context-management.md"): "context-management.md",
    ("context-engineering", "interview", "interview-context-mgmt.md"): "interview-context-mgmt.md",
    ("context-engineering", "practice", "effective-context-engineering.md"): "effective-context-engineering.md",
    # mcp
    ("mcp", "core", "mcp.md"): "mcp.md",
    ("mcp", "practice", "mcp-code-execution.md"): "mcp-code-execution.md",
    ("mcp", "practice", "mcp-deep-dive.md"): "mcp-deep-dive.md",
    # multi-agent
    ("multi-agent", "core", "multi-agent.md"): "multi-agent.md",
    ("multi-agent", "practice", "multi-agent-research.md"): "multi-agent-research.md",
    # other
    ("other", "core", "langgraph.md"): "langgraph.md",
    ("other", "core", "prompt-injection.md"): "prompt-injection.md",
    ("other", "core", "react.md"): "react.md",
    ("other", "practice", "agent-skills.md"): "agent-skills.md",
    ("other", "practice", "beyond-permission-prompts.md"): "beyond-permission-prompts.md",
    ("other", "practice", "dual-memory-system.md"): "dual-memory-system.md",
    ("other", "practice", "long-running-agents.md"): "long-running-agents.md",
    ("other", "practice", "slash-commands.md"): "slash-commands.md",
    ("other", "practice", "swe-bench.md"): "swe-bench.md",
    # rag
    ("rag", "core", "contextual-retrieval.md"): "contextual-retrieval.md",
    ("rag", "core", "hyde.md"): "hyde.md",
    ("rag", "core", "rag.md"): "rag.md",
    ("rag", "interview", "interview-hyde.md"): "interview-hyde.md",
    # tool-use
    ("tool-use", "core", "advanced-tool-use.md"): "advanced-tool-use.md",
    ("tool-use", "core", "tool-use.md"): "tool-use.md",
    ("tool-use", "practice", "think-tool.md"): "think-tool.md",
    ("tool-use", "practice", "writing-effective-tools.md"): "writing-effective-tools.md",
}

# Also migrate docs/concepts/index.md if it exists
docs_index = DOCS_CONCEPTS / "index.md"
if docs_index.exists():
    # Read it for reference
    print(f"Found docs/concepts/index.md, will regenerate")

migrated = []
for cat_dir in sorted(DOCS_CONCEPTS.iterdir()):
    if not cat_dir.is_dir():
        continue
    category = cat_dir.name
    for subdir in cat_dir.iterdir():
        if not subdir.is_dir():
            continue
        subcategory = subdir.name
        for md_file in sorted(subdir.glob("*.md")):
            if md_file.name.startswith('_'):
                continue
            key = (category, subcategory, md_file.name)
            if key not in FLATTEN_RULES:
                print(f"  WARNING: No rule for {key}")
                continue
            short_name = FLATTEN_RULES[key]
            dest = SRC_CONCEPTS / short_name
            shutil.copy2(md_file, dest)
            migrated.append((str(md_file), short_name))

print(f"\nMigrated {len(migrated)} files to src/concepts/")
for src, short in migrated:
    src_name = Path(src).name
    marker = " ✓" if src_name == short else f" → {short}"
    print(f"  {src_name}{marker}")

# -------------------------------------------------------------------
# 2. 构建 WIKILINK_MAP（用于 build.py）
# -------------------------------------------------------------------

# Wikilink → short filename (without .md)
# Short filenames in src/concepts are the source of truth
src_files = {f.stem: f.name for f in SRC_CONCEPTS.glob("*.md")}
print(f"\nWIKILINK_MAP: {len(src_files)} entries")
for stem, fname in sorted(src_files.items()):
    print(f"  [[{stem}]] → {fname}")
