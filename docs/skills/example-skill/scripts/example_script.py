#!/usr/bin/env python3
"""
示例脚本，展示如何编写技能相关脚本

该脚本演示了技能脚本的基本结构和功能，包括：
1. 基本的脚本结构
2. 命令行参数处理
3. 日志记录
4. 错误处理
5. 基本功能实现
"""

import argparse
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main(args):
    """脚本主函数"""
    try:
        logger.info(f"开始执行示例脚本，参数: {args}")
        
        # 模拟执行一些操作
        result = process_data(args.input)
        
        # 输出结果
        logger.info(f"执行结果: {result}")
        print(f"处理结果: {result}")
        
        return 0
    except Exception as e:
        logger.error(f"执行过程中发生错误: {e}")
        print(f"错误: {e}", file=sys.stderr)
        return 1


def process_data(input_data):
    """处理输入数据"""
    logger.info(f"处理输入数据: {input_data}")
    # 简单的处理逻辑
    return f"处理后的结果: {input_data.upper()}"


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="示例脚本")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="输入数据"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="启用详细输出"
    )
    
    args = parser.parse_args()
    
    # 如果启用详细输出，设置日志级别为DEBUG
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 执行主函数并返回退出码
    sys.exit(main(args))
