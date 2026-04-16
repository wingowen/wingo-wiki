import os
import re
import json
from mkdocs.plugins import BasePlugin
from mkdocs.config import Config


class WikiGraphPlugin(BasePlugin):
    config_scheme = ()

    def on_config(self, config: Config) -> Config:
        self.docs_dir = config['docs_dir']
        self.site_dir = config['site_dir']
        self.pages = {}
        self.links = []
        return config

    def on_files(self, files, config: Config):
        for file in files:
            if file.is_documentation_page() and file.name.endswith('.md'):
                page_name = self._get_page_name(file.path)
                self.pages[page_name] = {
                    'path': file.path,
                    'url': file.url,
                    'name': page_name
                }
        return files

    def on_page_markdown(self, markdown, page, config: Config, files):
        page_name = self._get_page_name(page.file.path)
        
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', markdown)
        
        for link in wikilinks:
            link_parts = link.split('|')
            target_name = link_parts[0].strip()
            
            if target_name in self.pages:
                link_exists = any(
                    l['source'] == page_name and l['target'] == target_name
                    for l in self.links
                )
                if not link_exists:
                    self.links.append({
                        'source': page_name,
                        'target': target_name
                    })
        
        return markdown

    def on_post_build(self, config: Config):
        graph_data = {
            'nodes': [],
            'links': self.links
        }
        
        for page_name, page_info in self.pages.items():
            category = self._get_category(page_info['path'])
            graph_data['nodes'].append({
                'name': page_name,
                'url': page_info['url'],
                'category': category
            })
        
        output_dir = os.path.join(self.site_dir, 'assets')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'graph-data.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        print(f"[WikiGraph] Generated graph data with {len(graph_data['nodes'])} nodes and {len(graph_data['links'])} links")

    def _get_page_name(self, path):
        base = os.path.basename(path)
        name = os.path.splitext(base)[0]
        return name.replace('-', ' ').title()

    def _get_category(self, path):
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
