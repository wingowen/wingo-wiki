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
