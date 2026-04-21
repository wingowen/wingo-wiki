#!/usr/bin/env python3
"""
检查所有 Markdown 文件中的标题重复问题
"""

import os
import re


def find_markdown_files(directory):
    """查找目录下所有 Markdown 文件"""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        # 跳过一些不需要检查的目录
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', 'public', 'site']]
        
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files


def extract_titles(file_path):
    """从 Markdown 文件中提取所有标题"""
    titles = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 匹配标题：# 开头，后面跟着空格和标题内容
        title_pattern = r'^(#{1,6})\s+(.*)$'
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            match = re.match(title_pattern, line.strip())
            if match:
                level = len(match.group(1))
                title_text = match.group(2).strip()
                titles.append((line_num, level, title_text))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return titles


def check_duplicate_titles(titles):
    """检查是否存在重复的标题"""
    duplicates = []
    title_dict = {}
    
    for line_num, level, title_text in titles:
        if title_text in title_dict:
            # 找到重复的标题
            prev_line_num, prev_level = title_dict[title_text]
            duplicates.append((prev_line_num, prev_level, line_num, level, title_text))
        else:
            title_dict[title_text] = (line_num, level)
    
    return duplicates


def main():
    """主函数"""
    print("开始检查 Markdown 文件中的标题重复问题...")
    
    # 查找所有 Markdown 文件
    markdown_files = find_markdown_files('.')
    print(f"找到 {len(markdown_files)} 个 Markdown 文件")
    
    # 检查每个文件
    total_duplicates = 0
    problematic_files = []
    
    for file_path in markdown_files:
        titles = extract_titles(file_path)
        duplicates = check_duplicate_titles(titles)
        
        if duplicates:
            total_duplicates += len(duplicates)
            problematic_files.append((file_path, duplicates))
            print(f"\n{file_path}:")
            for prev_line, prev_level, curr_line, curr_level, title in duplicates:
                print(f"  重复标题: '{title}'")
                print(f"    - 第一次出现: 第 {prev_line} 行 (H{prev_level})")
                print(f"    - 第二次出现: 第 {curr_line} 行 (H{curr_level})")
    
    # 生成报告
    print(f"\n=== 检查报告 ===")
    print(f"总检查文件数: {len(markdown_files)}")
    print(f"发现问题文件数: {len(problematic_files)}")
    print(f"总重复标题数: {total_duplicates}")
    
    if not problematic_files:
        print("\n✅ 未发现标题重复问题！")


if __name__ == "__main__":
    main()
