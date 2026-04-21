#!/usr/bin/env python3
import os
import re
import json
import sys
from pathlib import Path

# 导入 build.py 中的映射
sys.path.insert(0, str(Path(__file__).parent))
from build import CATEGORY_MAP, WIKILINK_MAP

def main():
    docs_dir = 'src'
    site_dir = 'site'
    
    pages = {}
    links = []
    
    for root, dirs, files in os.walk(docs_dir):
        # 跳过 superpowers 目录
        if 'superpowers' in root:
            continue
        
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, docs_dir)
                
                page_name = get_page_name(rel_path)
                url_path = get_url_path_from_map(file)
                
                pages[page_name] = {
                    'path': rel_path,
                    'url': url_path,
                    'name': page_name
                }
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
                    
                    for link in wikilinks:
                        link_parts = link.split('|')
                        target_raw = link_parts[0].strip()
                        # 使用 WIKILINK_MAP 转换为正确的文件名
                        target_file = WIKILINK_MAP.get(target_raw)
                        if not target_file:
                            continue
                        
                        # 获取目标页面的名称（用于匹配节点）
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
        'nodes': [],
        'links': links
    }
    
    for page_name, page_info in pages.items():
        category = get_category(page_info['path'])
        graph_data['nodes'].append({
            'name': page_name,
            'url': page_info['url'],
            'category': category
        })
    
    output_dir = os.path.join('docs', 'assets')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'graph-data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    
    print(f"[WikiGraph] Generated graph data with {len(graph_data['nodes'])} nodes and {len(graph_data['links'])} links")


def get_page_name(path):
    """Get page display name from file path or filename."""
    if path.endswith('.md'):
        base = os.path.basename(path)
        name = os.path.splitext(base)[0]
    else:
        name = os.path.basename(path)
    return name.replace('-', ' ').title()


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


def get_category(path):
    if 'concepts' in path:
        return 0
    elif 'entities' in path:
        return 1
    elif 'comparisons' in path:
        return 2
    elif 'queries' in path:
        return 3
    else:
        return 4


if __name__ == '__main__':
    main()
