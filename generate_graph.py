#!/usr/bin/env python3
import os
import re
import json
import sys


def main():
    docs_dir = 'docs'
    site_dir = 'site'
    
    pages = {}
    links = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, docs_dir)
                
                page_name = get_page_name(rel_path)
                url_path = get_url_path(rel_path)
                
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
                        target_name = link_parts[0].strip()
                        
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
    
    output_dir = os.path.join(site_dir, 'assets')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'graph-data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    
    print(f"[WikiGraph] Generated graph data with {len(graph_data['nodes'])} nodes and {len(graph_data['links'])} links")


def get_page_name(path):
    base = os.path.basename(path)
    name = os.path.splitext(base)[0]
    return name.replace('-', ' ').title()


def get_url_path(path):
    name = os.path.splitext(path)[0]
    return name + '/'


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
