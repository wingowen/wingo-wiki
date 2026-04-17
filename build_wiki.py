#!/usr/bin/env python3
"""
Wingo Wiki Build Script — 方案二：单源码，生成发布

SRC/           = 唯一种源码（LLM Wiki 标准，扁平目录，短文件名）
DOCS/          = MkDocs 发布源（构建时从 SRC/ 生成）
WIKI_ROOT/     = 包含 raw/, entities/, comparisons/, queries/ 的 LLM Wiki 根

工作流程：
1. 读取 src/concepts/ 下所有 .md 文件
2. 按 category 组织发布到 docs/concepts/{category}/
3. 将 wikilinks 从短名称转换为 Markdown relative links
4. 生成 mkdocs.yml nav 结构
5. 生成 index.md 内容目录
"""

import os
import re
import shutil
import yaml
from pathlib import Path

WIKI = Path(os.path.expanduser("~/wingo-wiki"))
SRC = WIKI / "src"
DOCS = WIKI / "docs"
SCHEMA = WIKI / "SCHEMA.md"
LOG = WIKI / "log.md"

# -------------------------------------------------------------------
# Step 1: 定义 concept 文件的 category 映射
# key: short filename, value: category
# -------------------------------------------------------------------

CONCEPT_FILES = {
    # agent-architecture
    "agent-architecture.md":          "agent-architecture/core",
    "agent-framework-theory.md":      "agent-architecture/core",
    "interview-agent-arch.md":        "agent-architecture/interview",
    "agent-framework-practice.md":    "agent-architecture/practice",
    "building-effective-agents.md":  "agent-architecture/practice",
    # claude
    "claude-agent-sdk.md":            "claude/practice",
    "claude-code-best-practices.md": "claude/practice",
    "claude-desktop-extensions.md":  "claude/practice",
    "claude-postmortem.md":           "claude/practice",
    # context-engineering
    "context-engineering.md":         "context-engineering/core",
    "context-management.md":          "context-engineering/core",
    "interview-context-mgmt.md":      "context-engineering/interview",
    "effective-context-engineering.md": "context-engineering/practice",
    # mcp
    "mcp.md":                         "mcp/core",
    "mcp-code-execution.md":          "mcp/practice",
    "mcp-deep-dive.md":              "mcp/practice",
    # multi-agent
    "multi-agent.md":                 "multi-agent/core",
    "multi-agent-research.md":       "multi-agent/practice",
    # other
    "langgraph.md":                   "other/core",
    "prompt-injection.md":            "other/core",
    "react.md":                       "other/core",
    "agent-skills.md":               "other/practice",
    "beyond-permission-prompts.md":  "other/practice",
    "dual-memory-system.md":         "other/practice",
    "long-running-agents.md":        "other/practice",
    "slash-commands.md":              "other/practice",
    "swe-bench.md":                   "other/practice",
    # rag
    "contextual-retrieval.md":        "rag/core",
    "hyde.md":                        "rag/core",
    "rag.md":                         "rag/core",
    "interview-hyde.md":             "rag/interview",
    # tool-use
    "advanced-tool-use.md":           "tool-use/core",
    "tool-use.md":                   "tool-use/core",
    "think-tool.md":                  "tool-use/practice",
    "writing-effective-tools.md":    "tool-use/practice",
}

# Wikilink → short filename 映射（用于 wikilink 重写）
WIKILINK_MAP = {}  # wikilink → short_filename (no extension)

for fname, cat_path in CONCEPT_FILES.items():
    category = cat_path.split("/")[0]
    # Determine wikilink for this file
    # Core files of a category use the category shortname (e.g. mcp.md → [[mcp]])
    if fname == f"{category}.md":
        wikilink = category
    else:
        # Remove extension, keep as-is
        wikilink = fname.replace(".md", "")
    WIKILINK_MAP[wikilink] = fname

# Add entities, comparisons, queries
for fname in ["ai-agent.md", "anthropic.md", "claude-code.md"]:
    WIKILINK_MAP[fname.replace(".md", "")] = fname
for fname in ["langgraph-vs-react.md"]:
    WIKILINK_MAP[fname.replace(".md", "")] = fname
for fname in ["interview-overview.md", "interview-qa-overview.md", "session-context.md"]:
    WIKILINK_MAP[fname.replace(".md", "")] = fname

print(f"WIKILINK_MAP has {len(WIKILINK_MAP)} entries")
print("Sample entries:")
for k, v in list(WIKILINK_MAP.items())[:10]:
    print(f"  [[{k}]] → {v}")


# -------------------------------------------------------------------
# Step 2: 准备 docs/concepts 目录（清理旧的，构建新的）
# -------------------------------------------------------------------

# Remove existing docs/concepts subdirs (keep index.md)
for item in (DOCS / "concepts").iterdir():
    if item.is_dir():
        shutil.rmtree(item)
    elif item.name != "index.md":
        item.unlink()

# Create fresh category subdirs
categories = set(v.split("/")[0] for v in CONCEPT_FILES.values())
for cat in categories:
    (DOCS / "concepts" / cat).mkdir(parents=True, exist_ok=True)
    # Create _index.md for category
    (DOCS / "concepts" / cat / "_index.md").write_text(
        f"---\ntitle: {cat.replace('-', ' ').title()}\n---\n\n# {cat.replace('-', ' ').title()}\n"
    )

print(f"\nCreated {len(categories)} category directories")


# -------------------------------------------------------------------
# Step 3: 复制并转换 src/concepts/ → docs/concepts/{cat}/
# -------------------------------------------------------------------

def rewrite_wikilinks(content):
    """将 [[wikilink]] 或 [[wikilink|display]] 转换为 Markdown relative link."""
    def replacer(m):
        full_match = m.group(0)
        # Extract the link target (before |) and display (after |)
        inner = m.group(1)
        if "|" in inner:
            link_part, display = inner.split("|", 1)
            link_part = link_part.strip()
            display = display.strip()
        else:
            link_part = inner.strip()
            display = None

        # Look up wikilink
        target_file = WIKILINK_MAP.get(link_part)
        if target_file is None:
            # Unknown wikilink — keep as-is (will be a broken link to fix manually)
            return full_match

        target_cat = CONCEPT_FILES.get(target_file, "")
        target_category = target_cat.split("/")[0] if target_cat else ""

        # Build relative path from current file's category
        # We'll figure out source category from content (passed via closure)
        return f"[{display or link_part}]({target_file})"

    return re.sub(r'\[\[([^\]]+)\]\]', replacer, content)


# Process each source file
processed = []
for short_name, cat_path in CONCEPT_FILES.items():
    src_file = SRC / "concepts" / short_name
    if not src_file.exists():
        print(f"  MISSING: {src_file}")
        continue

    content = src_file.read_text()
    category = cat_path.split("/")[0]
    subcategory = cat_path.split("/")[1] if "/" in cat_path else ""

    # Determine output path
    out_dir = DOCS / "concepts" / category / subcategory if subcategory else DOCS / "concepts" / category
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / short_name

    # Rewrite wikilinks in content
    new_content = rewrite_wikilinks(content)

    out_file.write_text(new_content)
    processed.append((short_name, cat_path, out_file))

print(f"\nProcessed {len(processed)} concept files")
for name, cat, out in processed[:5]:
    print(f"  {name} → {cat}/{name}")
