#!/usr/bin/env python3
"""Analyze article length and suggest modularization using wikilinks"""
import os
import re
from pathlib import Path

RAW_DIR = Path("/workspace/raw/articles")
THRESHOLD = 10000  # Characters threshold for long articles


def analyze_article_lengths():
    """Analyze all articles and identify long ones"""
    long_articles = []
    
    for article_path in RAW_DIR.glob("*.md"):
        content = article_path.read_text(encoding="utf-8")
        # Remove frontmatter for length calculation
        content_without_frontmatter = re.sub(r'^---[\s\S]*?---\n', '', content)
        char_count = len(content_without_frontmatter)
        
        if char_count > THRESHOLD:
            long_articles.append({
                "path": article_path,
                "name": article_path.stem,
                "char_count": char_count
            })
    
    return long_articles


def analyze_article_structure(article_path):
    """Analyze article structure and identify potential sections for modularization"""
    content = article_path.read_text(encoding="utf-8")
    
    # Extract sections (h2 and h3 headings)
    sections = []
    lines = content.split('\n')
    
    current_section = None
    current_content = []
    
    for line in lines:
        # Check for h2 heading
        h2_match = re.match(r'^##\s+(.*)$', line)
        if h2_match:
            if current_section:
                sections.append({
                    "title": current_section,
                    "content": '\n'.join(current_content),
                    "level": 2
                })
            current_section = h2_match.group(1)
            current_content = [line]
        # Check for h3 heading
        elif re.match(r'^###\s+(.*)$', line):
            if current_section:
                sections.append({
                    "title": current_section,
                    "content": '\n'.join(current_content),
                    "level": 2
                })
            current_section = line
            current_content = [line]
        else:
            if current_section:
                current_content.append(line)
    
    # Add the last section
    if current_section:
        sections.append({
            "title": current_section,
            "content": '\n'.join(current_content),
            "level": 2
        })
    
    return sections


def generate_modularization_plan(long_articles):
    """Generate modularization plan for long articles"""
    for article in long_articles:
        print(f"\n=== Analyzing {article['name']} ===")
        print(f"Current length: {article['char_count']} characters")
        
        sections = analyze_article_structure(article['path'])
        print(f"Found {len(sections)} sections")
        
        # Calculate section lengths
        total_length = 0
        for i, section in enumerate(sections):
            section_length = len(section['content'])
            total_length += section_length
            print(f"  Section {i+1}: {section['title'][:50]}... ({section_length} chars)")
        
        # Suggest modularization
        print("\n=== Modularization Suggestion ===")
        print(f"Create a main article: {article['name']}.md")
        print("Create separate files for each section:")
        
        for i, section in enumerate(sections):
            # Generate slug for section
            slug = re.sub(r'[^\w\s-]', '', section['title'])
            slug = re.sub(r'[\s-]+', '-', slug).strip('-').lower()
            section_file = f"{article['name']}-{slug}.md"
            print(f"  - {section_file}")
        
        print("\n=== Implementation Steps ===")
        print("1. Create the section files")
        print("2. Update the main article to use wikilinks to sections")
        print("3. Add wikilinks between related sections")


def main():
    """Main function"""
    print("=== Article Modularization Analysis ===")
    print(f"Analyzing articles in {RAW_DIR}")
    print(f"Threshold for long articles: {THRESHOLD} characters")
    
    long_articles = analyze_article_lengths()
    
    if not long_articles:
        print("No articles exceed the length threshold.")
        return
    
    print(f"Found {len(long_articles)} long articles:")
    for article in long_articles:
        print(f"  - {article['name']}: {article['char_count']} characters")
    
    generate_modularization_plan(long_articles)


if __name__ == "__main__":
    main()
