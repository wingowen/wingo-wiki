from setuptools import setup, find_packages

setup(
    name="mkdocs-wiki-graph-plugin",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'wiki_graph = wiki_graph.plugin:WikiGraphPlugin',
        ]
    },
    install_requires=[
        'mkdocs>=1.0',
    ],
)
