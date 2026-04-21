# Wingo Wiki 项目结构优化实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 优化 Wingo Wiki 项目结构，提高可维护性和可扩展性

**Architecture:** 采用模块化设计，将构建脚本拆分为多个功能明确的模块，分离配置和数据，优化目录结构和构建流程

**Tech Stack:** Python, Markdown, MkDocs, Hugo, JavaScript/TypeScript, Tailwind CSS, Netlify

---

## 文件结构规划

### 核心目录结构

```
├── config/                  # 配置文件目录
│   ├── mappings.py          # 链接和分类映射配置
│   └── settings.py          # 项目设置
├── scripts/                 # 模块化构建脚本
│   ├── __init__.py
│   ├── link_processor.py    # 链接处理模块
│   ├── nav_generator.py     # 导航配置生成
│   ├── graph_generator.py   # 知识图谱生成
│   ├── build.py             # 主构建脚本
│   └── utils.py             # 工具函数
├── src/                     # 源文档目录
│   └── concepts/            # 扁平 Markdown 文件
├── docs/                    # 构建输出目录
│   ├── concepts/            # 层次化文档结构
│   ├── assets/              # 静态资源
│   ├── mkdocs.yml           # 自动生成的配置
│   └── index.md             # 索引文件
├── site/                    # MkDocs 构建输出
├── requirements.txt         # Python 依赖
└── README.md                # 项目说明
```

---

## 任务分解

### 任务 1: 创建配置目录和映射文件

**Files:**
- Create: `config/mappings.py`
- Modify: `build.py:23-114`

- [ ] **Step 1: 创建 config 目录**

```bash
mkdir -p config
```

- [ ] **Step 2: 提取映射配置到单独文件**

```python
# config/mappings.py

# WIKILINK_MAP: wikilink stem → short_filename
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

# CATEGORY_MAP: short_filename → (category, subcategory)
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
```

- [ ] **Step 3: 修改 build.py 导入映射配置**

```python
# 修改 build.py 顶部导入
from config.mappings import WIKILINK_MAP, CATEGORY_MAP

# 移除文件中的 WIKILINK_MAP 和 CATEGORY_MAP 定义
```

- [ ] **Step 4: 测试构建脚本**

```bash
python build.py
```

- [ ] **Step 5: 提交更改**

```bash
git add config/mappings.py build.py
git commit -m "refactor: move mappings to separate config file"
```

### 任务 2: 创建脚本目录和模块化构建脚本

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/utils.py`
- Create: `scripts/link_processor.py`
- Create: `scripts/nav_generator.py`
- Create: `scripts/graph_generator.py`
- Create: `scripts/build.py`
- Modify: `build.py`

- [ ] **Step 1: 创建 scripts 目录**

```bash
mkdir -p scripts
```

- [ ] **Step 2: 创建工具函数文件**

```python
# scripts/utils.py
import os
from pathlib import Path
import re

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

def path_to_url(rel_path):
    """Convert a relative markdown path to a canonical wiki URL."""
    # Remove .md extension and normalize
    if rel_path.endswith(".md"):
        rel_path = rel_path[:-3]
    # Normalize path (remove leading ./, fix backslashes)
    rel_path = rel_path.replace("\\", "/")
    rel_path = rel_path.lstrip("./")
    # Remove docs/ prefix if present
    if rel_path.startswith("docs/"):
        rel_path = rel_path[5:]
    # Remove index.md
    if rel_path.endswith("/index"):
        rel_path = rel_path[:-6]
    # Ensure trailing slash
    if not rel_path.endswith("/"):
        rel_path += "/"
    return rel_path
```

- [ ] **Step 3: 创建链接处理模块**

```python
# scripts/link_processor.py
import os
from pathlib import Path
import re
from config.mappings import WIKILINK_MAP, CATEGORY_MAP

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

        # For entities/queries/comparisons, treat them as being under concepts/
        # for relative path calculation, so links to concept pages get correct path
        if source_cat in ("entities", "queries", "comparisons"):
            source_dir = Path(source_cat)
        elif source_sub == "":
            source_dir = Path("concepts") / source_cat
        else:
            source_dir = Path("concepts") / source_cat / source_sub

        if target_cat in ("entities", "queries", "comparisons"):
            target_dir = Path(target_cat)
        elif target_sub == "":
            target_dir = Path("concepts") / target_cat
        else:
            target_dir = Path("concepts") / target_cat / target_sub

        rel = os.path.relpath(target_dir / target_file, source_dir).replace("\\", "/")
        return f"[{display}]({rel})"

    return re.sub(r'\[\[([^\]]+)\]\]', replacer, content)

def rewrite_index_wikilinks(content, index_wikilink_map):
    """Rewrite wikilinks in index.md."""
    def replacer(m):
        inner = m.group(1)
        if "|" in inner:
            link_part, display = inner.split("|", 1)
            link_part = link_part.strip()
            display = display.strip()
        else:
            link_part = inner.strip()
            display = link_part
        target = index_wikilink_map.get(link_part)
        if target:
            # Strip interview-category prefixes from display text
            display = re.sub(r'^【[^】]+】\s*', '', display)
            return f"[{display}]({target})"
        return f"[[{link_part}]]"
    return re.sub(r'\[\[([^\]]+)\]\]', replacer, content)
```

- [ ] **Step 4: 创建导航生成模块**

```python
# scripts/nav_generator.py
from pathlib import Path
from config.mappings import CATEGORY_MAP
from scripts.utils import get_title

def generate_mkdocs_nav(src_concepts, wiki_path):
    """Generate mkdocs.yml navigation configuration."""
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
        cat_files = [(sn, get_title(src_concepts / sn)) for sn, (c, sc) in CATEGORY_MAP.items() if c == cat]
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
    nav_lines.append("    - LangGraph vs React: comparisons/langgraph-vs-react")

    # Entities
    nav_lines.append("  - Entities:")
    for sn in ["ai-agent.md", "anthropic.md", "claude-code.md"]:
        title = get_title(wiki_path / "entities" / sn)
        path_sn = sn[:-3] if sn.endswith(".md") else sn
        nav_lines.append(f"    - \"{title}\": entities/{path_sn}")

    # Queries
    nav_lines.append("  - Queries:")
    for sn in ["interview-overview.md", "interview-qa-overview.md", "session-context.md"]:
        title = get_title(wiki_path / "queries" / sn)
        path_sn = sn[:-3] if sn.endswith(".md") else sn
        nav_lines.append(f"    - \"{title}\": queries/{path_sn}")

    return "\n".join(nav_lines)
```

- [ ] **Step 5: 创建知识图谱生成模块**

```python
# scripts/graph_generator.py
import json
import os
from pathlib import Path
from config.mappings import CATEGORY_MAP
from scripts.utils import get_title, path_to_url

def generate_knowledge_graph(docs_path, src_concepts, wiki_path):
    """Generate knowledge graph data from wikilinks."""
    # Build reverse map: URL path → node name
    # Also build forward map: short_filename → (name, url, category)
    URL_TO_NAME = {}
    FILENAME_TO_NODE = {}
    nodes = {}  # url → node dict (pre-populated from CATEGORY_MAP)
    for short_name, (cat, subcat) in CATEGORY_MAP.items():
        # Get the title from source file
        src_file = src_concepts / short_name
        if not src_file.exists():
            src_file = wiki_path / "entities" / short_name
        if not src_file.exists():
            src_file = wiki_path / "queries" / short_name
        if not src_file.exists():
            src_file = wiki_path / "comparisons" / short_name
        if not src_file.exists():
            src_file = wiki_path / "concepts" / short_name  # root-level concepts dir

        name = get_title(src_file) if src_file.exists() else short_name.replace(".md", "").replace("-", " ").title()

        if cat == "entities":
            url = f"entities/{short_name[:-3]}/"
            category = 1
        elif cat == "comparisons":
            url = f"comparisons/{short_name[:-3]}/"
            category = 2
        elif cat == "queries":
            url = f"queries/{short_name[:-3]}/"
            category = 3
        else:
            # concepts
            if subcat:
                url = f"concepts/{cat}/{subcat}/{short_name[:-3]}/"
            else:
                url = f"concepts/{cat}/{short_name[:-3]}/"
            category = 0

        nodes[url] = {"name": name, "url": url, "category": category}
        URL_TO_NAME[url] = name
        FILENAME_TO_NODE[short_name] = {"name": name, "url": url, "category": category}

    # Also add nodes for entities, queries, comparisons from their source dirs
    # (in case some files are not in CATEGORY_MAP)
    for rd, cat_idx in [("entities", 1), ("queries", 3), ("comparisons", 2)]:
        src_dir = wiki_path / rd
        if src_dir.is_dir():
            for src_file in src_dir.glob("*.md"):
                short_name = src_file.name
                if short_name in FILENAME_TO_NODE:
                    continue
                name = get_title(src_file)
                url = f"{rd}/{short_name[:-3]}/"
                URL_TO_NAME[url] = name
                FILENAME_TO_NODE[short_name] = {"name": name, "url": url, "category": cat_idx}
                nodes[url] = {"name": name, "url": url, "category": cat_idx}

    # Now scan all markdown files in docs/ and extract links
    DOCS_DIRS = ["concepts", "entities", "queries", "comparisons"]
    CAT_INDEX = {"concepts": 0, "entities": 1, "comparisons": 2, "queries": 3}

    links_set = set()  # (source_name, target_name)

    def get_node_for_file(doc_file):
        """Get or create node for a doc file path."""
        rel = doc_file.relative_to(docs_path)
        rel_str = str(rel).replace("\\", "/")
        if rel_str.endswith(".md"):
            url = rel_str[:-3] + "/"
        else:
            url = rel_str + "/"

        if url in URL_TO_NAME:
            name = URL_TO_NAME[url]
        else:
            # Derive from filename
            name = doc_file.stem.replace("-", " ").title()

        # Determine category from path
        parts = url.strip("/").split("/")
        if parts[0] in CAT_INDEX:
            category = CAT_INDEX[parts[0]]
        else:
            category = 0

        return {"name": name, "url": url, "category": category}

    for dir_name in DOCS_DIRS:
        scan_dir = docs_path / dir_name
        if not scan_dir.is_dir():
            continue

        for doc_file in scan_dir.rglob("*.md"):
            # Skip _index.md files
            if doc_file.name == "_index.md" or doc_file.name == "index.md":
                continue

            node = get_node_for_file(doc_file)
            nodes[node["url"]] = node

            # Extract markdown links from content
            content = doc_file.read_text()
            # Find all ](path) patterns
            link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+\.md)\)')
            for match in link_pattern.finditer(content):
                link_text = match.group(1)
                link_path = match.group(2)

                # Skip external URLs
                if link_path.startswith("http://") or link_path.startswith("https://"):
                    continue
                if link_path.startswith("mailto:"):
                    continue

                # Resolve relative path to canonical URL
                link_url = path_to_url(os.path.relpath(os.path.join(os.path.dirname(doc_file), link_path), docs_path))

                if link_url in URL_TO_NAME:
                    target_name = URL_TO_NAME[link_url]
                    source_name = node["name"]
                    if source_name != target_name:  # No self-links
                        links_set.add((source_name, target_name))
                # else: link target not in wiki (external or broken link), skip

    # Build final nodes list (in deterministc order)
    nodes_list = sorted(nodes.values(), key=lambda x: x["name"])

    # Build links list
    links_list = [{"source": s, "target": t} for s, t in sorted(links_set)]

    return {"nodes": nodes_list, "links": links_list}
```

- [ ] **Step 6: 创建主构建脚本**

```python
# scripts/build.py
#!/usr/bin/env python3
"""
Build Script: src/concepts/ (flat) → docs/concepts/ (hierarchical)
              + mkdocs.yml generation
              + index.md generation

Wikilinks (flat) → Markdown relative links (hierarchical)
"""

import os
import shutil
from pathlib import Path
from config.mappings import WIKILINK_MAP, CATEGORY_MAP
from scripts.link_processor import rewrite_wikilinks, rewrite_index_wikilinks
from scripts.nav_generator import generate_mkdocs_nav
from scripts.graph_generator import generate_knowledge_graph
from scripts.utils import get_title

WIKI = Path(os.path.expanduser("~/wingo-wiki"))
SRC_CONCEPTS = WIKI / "src" / "concepts"
DOCS_CONCEPTS = WIKI / "docs" / "concepts"
DOCS = WIKI / "docs"

def main():
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

    mkdocs_content = generate_mkdocs_nav(SRC_CONCEPTS, WIKI)
    mkdocs_path = WIKI / "mkdocs.yml"
    mkdocs_path.write_text(mkdocs_content)
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
        "【面试专题】Agent 架构设计：从传统开发到智能体": "concepts/agent-architecture/interview/interview-agent-arch/",
        "【面试专题】上下文管理：短期记忆与长期记忆": "concepts/context-engineering/interview/interview-context-mgmt/",
        "【面试专题】HyDE 假设文档嵌入与高级检索策略": "concepts/rag/interview/interview-hyde/",
        "LangGraph 核心原理与 ReAct 对比": "comparisons/langgraph-vs-react/",
        "AI Agent 面试复盘总览": "queries/interview-overview/",
        "【面试复盘】AI Agent 面试突击问答清单（总览）": "queries/interview-qa-overview/",
        "Session Context 影响技能选择的问题分析与解决方案": "queries/session-context/",
    }

    index_content = rewrite_index_wikilinks(index_content, INDEX_WIKILINK_MAP)

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
    # Step 5: Generate knowledge graph data from actual wikilinks
    # -------------------------------------------------------------------

    print("\n=== Step 5: Generating knowledge graph from wikilinks ===")

    graph_data = generate_knowledge_graph(DOCS, SRC_CONCEPTS, WIKI)

    graph_path = DOCS / "assets" / "graph-data.json"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph_data, indent=2, ensure_ascii=False))

    print(f"  Generated {len(graph_data['nodes'])} nodes and {len(graph_data['links'])} links")
    print(f"  Written {graph_path}")


    # -------------------------------------------------------------------
    # Step 6: Summary
    # -------------------------------------------------------------------

    print(f"""
    === Build Complete ===

    Source:      src/concepts/ ({len(processed)} flat .md files)
    Published:   docs/concepts/ (hierarchical for MkDocs)
    Nav:         mkdocs.yml (auto-generated)
    Index:       docs/index.md (auto-generated)
    Graph:       docs/assets/graph-data.json ({len(graph_data['nodes'])} nodes, {len(graph_data['links'])} links)

    To publish:
      1. cd ~/wingo-wiki && python build.py
      2. mkdocs build
      3. git push → Netlify deploys
    """)

if __name__ == "__main__":
    main()
```

- [ ] **Step 7: 更新根目录 build.py 为包装脚本**

```python
#!/usr/bin/env python3
"""
Wrapper script to run the modular build system
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.build import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 8: 测试模块化构建脚本**

```bash
python build.py
```

- [ ] **Step 9: 提交更改**

```bash
git add scripts/ build.py
git commit -m "refactor: modularize build scripts"
```

### 任务 3: 实现增量构建功能

**Files:**
- Create: `scripts/incremental_build.py`
- Modify: `scripts/build.py`

- [ ] **Step 1: 创建增量构建模块**

```python
# scripts/incremental_build.py
import os
import hashlib
from pathlib import Path
import json

def get_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def load_hash_cache(cache_path):
    """Load hash cache from file."""
    if not cache_path.exists():
        return {}
    try:
        with open(cache_path, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_hash_cache(cache_path, cache):
    """Save hash cache to file."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w") as f:
        json.dump(cache, f, indent=2)

def needs_processing(file_path, cache):
    """Check if a file needs processing based on hash."""
    file_hash = get_file_hash(file_path)
    if file_path in cache:
        return cache[file_path] != file_hash
    return True

def update_cache(file_path, cache):
    """Update cache with current file hash."""
    cache[str(file_path)] = get_file_hash(file_path)
    return cache
```

- [ ] **Step 2: 修改 build.py 集成增量构建**

```python
# 在 scripts/build.py 中添加
from scripts.incremental_build import load_hash_cache, save_hash_cache, needs_processing, update_cache

# 在 main() 函数开始添加
CACHE_PATH = WIKI / ".build_cache.json"
cache = load_hash_cache(CACHE_PATH)

# 在处理每个文件时检查是否需要处理
for src_file in sorted(SRC_CONCEPTS.glob("*.md")):
    short_name = src_file.name
    if not needs_processing(src_file, cache):
        print(f"  {short_name} → unchanged, skipping")
        processed.append(short_name)
        continue
    # 处理文件...
    # 处理完成后更新缓存
    cache = update_cache(src_file, cache)

# 在函数结束时保存缓存
save_hash_cache(CACHE_PATH, cache)
```

- [ ] **Step 3: 测试增量构建**

```bash
# 第一次构建（全量）
python build.py
# 第二次构建（增量）
python build.py
```

- [ ] **Step 4: 提交更改**

```bash
git add scripts/incremental_build.py scripts/build.py
git commit -m "feat: add incremental build support"
```

### 任务 4: 优化知识图谱前端展示

**Files:**
- Modify: `docs/assets/javascripts/graph.js`

- [ ] **Step 1: 增强知识图谱交互功能**

```javascript
// docs/assets/javascripts/graph.js
// 增强版知识图谱可视化

function initGraph() {
    // 初始化 ECharts 实例
    var chart = echarts.init(document.getElementById('graph-container'));
    
    // 加载图谱数据
    fetch('assets/graph-data.json')
        .then(response => response.json())
        .then(data => {
            // 配置选项
            var option = {
                title: {
                    text: '知识图谱',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        if (params.dataType === 'node') {
                            return `<div><b>${params.data.name}</b></div><div>类别: ${getCategoryName(params.data.category)}</div>`;
                        } else {
                            return `<div>关联: ${params.data.source} → ${params.data.target}</div>`;
                        }
                    }
                },
                legend: {
                    data: ['概念', '实体', '比较', '查询'],
                    orient: 'horizontal',
                    bottom: 10
                },
                toolbox: {
                    feature: {
                        zoom: {
                            show: true
                        },
                        dataZoom: {
                            show: true
                        },
                        restore: {
                            show: true
                        }
                    }
                },
                animationDurationUpdate: 1500,
                animationEasingUpdate: 'quinticInOut',
                series: [
                    {
                        type: 'graph',
                        layout: 'force',
                        data: data.nodes,
                        links: data.links,
                        categories: [
                            { name: '概念', itemStyle: { color: '#5470c6' } },
                            { name: '实体', itemStyle: { color: '#91cc75' } },
                            { name: '比较', itemStyle: { color: '#fac858' } },
                            { name: '查询', itemStyle: { color: '#ee6666' } }
                        ],
                        roam: true,
                        label: {
                            show: true,
                            position: 'right',
                            formatter: '{b}'
                        },
                        labelLayout: {
                            hideOverlap: true
                        },
                        scaleLimit: {
                            min: 0.4,
                            max: 2
                        },
                        lineStyle: {
                            color: 'source',
                            curveness: 0.3
                        },
                        emphasis: {
                            focus: 'adjacency',
                            lineStyle: {
                                width: 4
                            }
                        },
                        force: {
                            repulsion: 100,
                            edgeLength: [80, 120]
                        }
                    }
                ]
            };
            
            // 设置选项
            chart.setOption(option);
            
            // 响应式
            window.addEventListener('resize', function() {
                chart.resize();
            });
        });
}

function getCategoryName(category) {
    const names = ['概念', '实体', '比较', '查询'];
    return names[category] || '未知';
}

// 页面加载完成后初始化
window.addEventListener('load', initGraph);
```

- [ ] **Step 2: 测试知识图谱展示**

```bash
# 构建项目
python build.py
# 启动本地服务器
python -m http.server 8000
```

- [ ] **Step 3: 提交更改**

```bash
git add docs/assets/javascripts/graph.js
git commit -m "feat: enhance knowledge graph visualization"
```

### 任务 5: 清理和统一构建输出目录

**Files:**
- Modify: `netlify.toml`
- Modify: `README.md`

- [ ] **Step 1: 更新 Netlify 配置**

```toml
# netlify.toml
[build]
  command = "python build.py && mkdocs build"
  publish = "site"
```

- [ ] **Step 2: 更新 README.md**

```markdown
# Wingo Wiki

AI Agent 技术与工程实践知识库

## 项目结构

- `src/concepts/` - 扁平化的 Markdown 源文件
- `docs/` - 构建输出目录（层次化结构）
- `site/` - MkDocs 构建输出（最终网站）
- `scripts/` - 模块化构建脚本
- `config/` - 配置文件

## 构建流程

1. 运行构建脚本：`python build.py`
2. 构建 MkDocs 网站：`mkdocs build`
3. 部署到 Netlify：`git push`

## 技术栈

- Python - 构建脚本
- Markdown - 文档格式
- MkDocs - 静态站点生成
- ECharts - 知识图谱可视化
- Tailwind CSS - 样式
- Netlify - 部署
```

- [ ] **Step 3: 提交更改**

```bash
git add netlify.toml README.md
git commit -m "chore: update deployment configuration"
```

---

## 计划执行

**Plan complete and saved to `docs/superpowers/plans/2026-04-21-project-structure-implementation.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**