import json
import os
from pathlib import Path
import re
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
