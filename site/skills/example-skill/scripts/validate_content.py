#!/usr/bin/env python3
"""
内容验证脚本，检查技能内容的完整性和规范性

该脚本用于验证技能内容是否符合 LLM Wiki Skill 维护规范，包括：
1. 检查技能目录结构是否符合规范
2. 验证 SKILL.md 文件是否存在且格式正确
3. 检查 frontmatter 中的必要字段
4. 验证内容的完整性
5. 检查链接的有效性
"""

import os
import re
import logging
import sys
import yaml

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 技能目录结构规范
REQUIRED_DIRS = ['scripts', 'examples', 'resources']
REQUIRED_FILES = ['SKILL.md']

# Frontmatter 必要字段
REQUIRED_FIELDS = ['title', 'created', 'updated', 'version', 'type', 'tags', 'description']


def validate_skill_structure(skill_dir):
    """验证技能目录结构"""
    logger.info(f"验证技能目录结构: {skill_dir}")
    
    # 检查技能目录是否存在
    if not os.path.exists(skill_dir):
        logger.error(f"技能目录不存在: {skill_dir}")
        return False
    
    # 检查必要的子目录
    for dir_name in REQUIRED_DIRS:
        dir_path = os.path.join(skill_dir, dir_name)
        if not os.path.exists(dir_path):
            logger.warning(f"缺少必要的子目录: {dir_name}")
        elif not os.path.isdir(dir_path):
            logger.error(f"{dir_name} 不是目录: {dir_path}")
            return False
    
    # 检查必要的文件
    for file_name in REQUIRED_FILES:
        file_path = os.path.join(skill_dir, file_name)
        if not os.path.exists(file_path):
            logger.error(f"缺少必要的文件: {file_name}")
            return False
        elif not os.path.isfile(file_path):
            logger.error(f"{file_name} 不是文件: {file_path}")
            return False
    
    return True


def validate_frontmatter(skill_file):
    """验证 SKILL.md 文件的 frontmatter"""
    logger.info(f"验证 frontmatter: {skill_file}")
    
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取 frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not frontmatter_match:
            logger.error("缺少 frontmatter")
            return False
        
        frontmatter_str = frontmatter_match.group(1)
        frontmatter = yaml.safe_load(frontmatter_str)
        
        # 检查必要字段
        missing_fields = []
        for field in REQUIRED_FIELDS:
            if field not in frontmatter:
                missing_fields.append(field)
        
        if missing_fields:
            logger.error(f"缺少必要的 frontmatter 字段: {', '.join(missing_fields)}")
            return False
        
        # 验证字段格式
        # 验证日期格式
        for date_field in ['created', 'updated']:
            date_str = frontmatter.get(date_field)
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                logger.error(f"日期格式错误 ({date_field}): {date_str}")
                return False
        
        # 验证版本格式
        version = frontmatter.get('version')
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            logger.error(f"版本格式错误: {version}")
            return False
        
        # 验证类型
        skill_type = frontmatter.get('type')
        if skill_type != 'skill':
            logger.warning(f"类型建议为 'skill'，当前为: {skill_type}")
        
        return True
    except Exception as e:
        logger.error(f"解析 frontmatter 时发生错误: {e}")
        return False


def validate_content(skill_file):
    """验证 SKILL.md 文件的内容"""
    logger.info(f"验证内容: {skill_file}")
    
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查内容长度
        if len(content) < 100:
            logger.warning("内容过短")
        
        # 检查必要的章节
        required_sections = [
            '技能介绍',
            '使用指南',
            '核心功能',
            '技术实现',
            '安全注意事项',
            '维护和更新'
        ]
        
        missing_sections = []
        for section in required_sections:
            if f"## {section}" not in content:
                missing_sections.append(section)
        
        if missing_sections:
            logger.warning(f"缺少建议的章节: {', '.join(missing_sections)}")
        
        # 检查链接格式
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for link_text, link_url in links:
            if not link_url.startswith(('http://', 'https://', 'file:///')):
                logger.warning(f"链接格式可能不正确: {link_url}")
        
        return True
    except Exception as e:
        logger.error(f"验证内容时发生错误: {e}")
        return False


def main(skill_dir):
    """脚本主函数"""
    try:
        logger.info(f"开始验证技能: {skill_dir}")
        
        # 验证目录结构
        if not validate_skill_structure(skill_dir):
            return 1
        
        # 验证 SKILL.md 文件
        skill_file = os.path.join(skill_dir, 'SKILL.md')
        
        # 验证 frontmatter
        if not validate_frontmatter(skill_file):
            return 1
        
        # 验证内容
        if not validate_content(skill_file):
            return 1
        
        logger.info("技能验证通过！")
        print("技能验证通过！")
        return 0
    except Exception as e:
        logger.error(f"验证过程中发生错误: {e}")
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"用法: {sys.argv[0]} <skill_directory>")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    sys.exit(main(skill_dir))
