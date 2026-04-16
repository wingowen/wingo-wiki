# Wingo Wiki

Wingo's personal wiki built with MkDocs and Material for MkDocs, supporting Obsidian-style wikilinks.

## Features

- **Obsidian-style wikilinks**: Use `[[link]]` syntax to link between pages
- **Material for MkDocs**: Modern, responsive theme with dark mode support
- **Netlify deployment**: Automatic deployment to Netlify
- **Easy navigation**: Organized by categories (Concepts, Comparisons, Entities, Queries, Skills)
- **LLM Wiki Skill system**: Structured skills following Anthropic's Agent Skills best practices

## Setup

### Prerequisites

- Python 3.8+
- Pip

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install mkdocs mkdocs-material mkdocs-roamlinks-plugin
   ```

3. Run the development server:
   ```bash
   mkdocs serve
   ```

4. Build for production:
   ```bash
   mkdocs build
   ```

## Directory Structure

```
workspace/
├── docs/              # MkDocs content directory
│   ├── concepts/      # Core concepts and theories
│   ├── comparisons/   # Comparisons between technologies
│   ├── entities/      # Key entities
│   ├── queries/       # Interview questions and answers
│   ├── skills/        # LLM Wiki Skills
│   ├── llm-wiki-skill-maintenance.md  # LLM Wiki Skill maintenance guidelines
│   └── index.md       # Site homepage
├── mkdocs.yml         # MkDocs configuration
├── netlify.toml       # Netlify deployment configuration
└── README.md          # This file
```

## Writing Content

- Write in Markdown format
- Use Obsidian-style wikilinks: `[[page-name]]`
- Organize content in the appropriate subdirectory under `docs/`
- Update the `nav` section in `mkdocs.yml` to include new pages

## Deployment

The site is automatically deployed to Netlify when changes are pushed to the repository. The deployment configuration is in `netlify.toml`.

## Contributing

To contribute to this wiki:
1. Fork the repository
2. Make your changes
3. Push to your fork
4. Create a pull request
