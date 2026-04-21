#!/usr/bin/env python3
import re
import json
import sys
from pathlib import Path

# 导入 build.py 中的映射
sys.path.insert(0, str(Path(__file__).parent))
from build import CATEGORY_MAP, WIKILINK_MAP

def main():
    pages = {}
    links = []

    # Walk all source dirs: src/concepts/ + root entities/comparisons/queries
    # CATEGORY_MAP keys tell us every file that should appear in the graph
    src_concepts_dir = Path("src") / "concepts"
    root_wiki_dirs = ['entities', 'comparisons', 'queries']

    # Collect all .md source files
    all_source_files = []
    if src_concepts_dir.is_dir():
        all_source_files.extend(src_concepts_dir.glob('*.md'))
    for rd in root_wiki_dirs:
        rd_path = Path(rd)
        if rd_path.is_dir():
            all_source_files.extend(rd_path.glob('*.md'))

    for src_file in all_source_files:
        if src_file.name == 'index.md':
            continue

        # Resolve the short name (e.g. "agent-architecture.md")
        short_name = src_file.name

        # Get URL from CATEGORY_MAP (authoritative — same as build.py)
        url_path = get_url_path_from_map(short_name)
        if not url_path:
            continue  # not in CATEGORY_MAP, skip

        page_name = get_page_name(short_name)
        pages[short_name] = {
            'name': page_name,
            'url': url_path,
        }

        # Read content to find wikilinks
        try:
            content = src_file.read_text(encoding='utf-8')
        except Exception:
            continue

        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in wikilinks:
            link_parts = link.split('|')
            target_raw = link_parts[0].strip()
            # Use WIKILINK_MAP to resolve wikilink stem → filename
            target_file = WIKILINK_MAP.get(target_raw)
            if not target_file:
                continue

            # Get target page name
            target_name = get_page_name(target_file)

            link_exists = any(
                l['source'] == page_name and l['target'] == target_name
                for l in links
            )
            if not link_exists:
                links.append({
                    'source': page_name,
                    'target': target_name
                })
                
    graph_data = {
        "nodes": [],
        "links": links
    }

    for short_name, page_info in pages.items():
        cat, subcat = CATEGORY_MAP.get(short_name, (None, None))
        if cat == "entities":
            category = 1
        elif cat == "comparisons":
            category = 2
        elif cat == "queries":
            category = 3
        else:
            category = 0  # concepts

        graph_data["nodes"].append({
            "name": page_info["name"],
            "url": page_info["url"],
            "category": category
        })

    output_dir = Path("docs") / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "graph-data.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)

    print(f"[WikiGraph] Generated graph data with {len(graph_data['nodes'])} nodes and {len(graph_data['links'])} links")


def get_page_name(filename):
    """Get page display name from a short filename like 'agent-architecture.md'."""
    return filename.replace("-", " ").replace(".md", "").title()


def get_url_path_from_map(filename):
    """Get URL path using CATEGORY_MAP like build.py does."""
    if filename in CATEGORY_MAP:
        cat, subcat = CATEGORY_MAP[filename]
        if cat == "entities" or cat == "comparisons" or cat == "queries":
            return f"{cat}/{filename.replace('.md', '')}/"
        elif subcat:
            return f"concepts/{cat}/{subcat}/{filename.replace('.md', '')}/"
        else:
            return f"concepts/{cat}/{filename.replace('.md', '')}/"
    # Fallback
    return f"concepts/{filename.replace('.md', '')}/"


if __name__ == '__main__':
    main()
