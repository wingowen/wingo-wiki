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
