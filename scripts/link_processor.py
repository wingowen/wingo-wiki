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
