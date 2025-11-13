"""
文件名: tests/run_tests.py
功能描述: 测试运行脚本，用于快速测试核心功能和验证工具运行状态
主要函数:
  - test_basic_functionality(): 测试基本功能
  - test_edge_cases(): 测试边界情况
  - test_batch_processing(): 测试批量处理
  - main(): 主函数，运行所有测试
主要类: 无
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本 - 用于快速测试核心功能
"""

import sys
import os

# 将项目根目录添加到Python路径，以便导入src包
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.text_analyzer import TextAnalyzer
from src.space_cleaner import SpaceCleaner


def test_basic_functionality():
    """
    测试基本功能

    测试文本分析和空格清理的核心功能，包括中英文混合文本的处理。
    """
    print("=== 测试基本功能 ===")

    # 创建分析器和清理器
    analyzer = TextAnalyzer()
    cleaner = SpaceCleaner()

    # 测试用例
    test_cases = [
        "你好 hello world",
        "人工智能 AI 技术",
        "Python 编程语言",
        "机器学习 machine learning 很有趣",
        "hello world",  # 纯英文
        "只有中文",     # 纯中文
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"\n--- 测试用例 {i}: {text} ---")

        # 分析文本
        analysis = analyzer.analyze_text(text)
        print(f"中文字符数: {analysis['chinese_chars']}")
        print(f"英文字符数: {analysis['english_chars']}")
        print(f"空格数: {analysis['spaces']}")
        print(f"混合内容: {'是' if analysis['has_mixed_content'] else '否'}")
        print(f"边界空格数: {analysis['total_boundary_spaces']}")

        # 清理文本
        cleaned = cleaner.clean_text(text)
        print(f"原始文本: '{text}'")
        print(f"清理后文本: '{cleaned['cleaned_text']}'")
        print(f"移除空格数: {cleaned['spaces_removed']}")

        if cleaned['changes']:
            print("变更详情:")
            for change in cleaned['changes']:
                print(f"  - {change['description']}")


def test_edge_cases():
    """
    测试边界情况

    测试各种边界场景，包括空字符串、只有空格、多个空格、
    包含特殊字符（制表符、换行符）和标点符号的文本。
    """
    print("\n\n=== 测试边界情况 ===")
    
    cleaner = SpaceCleaner()
    
    edge_cases = [
        "",                    # 空字符串
        "   ",                 # 只有空格
        "你好   hello",        # 多个空格
        "hello\t你好\nworld",   # 包含制表符和换行符
        "你好! hello? world.", # 包含标点符号
    ]
    
    for i, text in enumerate(edge_cases, 1):
        print(f"\n--- 边界用例 {i}: '{text}' ---")
        result = cleaner.clean_text(text)
        print(f"结果: '{result['cleaned_text']}'")
        print(f"变更数: {result['spaces_removed']}")


def test_batch_processing():
    """
    测试批量处理

    测试SpaceCleaner的批量处理能力，包括多个文本的同时处理
    和统计信息的生成。
    """
    print("\n\n=== 测试批量处理 ===")
    
    cleaner = SpaceCleaner()
    
    texts = [
        "你好 hello",
        "world 世界",
        "AI 人工智能",
        "纯英文文本 no chinese",
        "只有中文没有英文"
    ]
    
    results = cleaner.clean_multiple_texts(texts)
    stats = cleaner.get_processing_statistics(results)
    
    print(f"处理文本总数: {stats['total_texts']}")
    print(f"有变更的文本数: {stats['texts_with_changes']}")
    print(f"总移除空格数: {stats['total_spaces_removed']}")
    print(f"平均每个文本移除空格数: {stats['average_spaces_per_text']:.2f}")
    print(f"变更率: {stats['change_rate']:.1f}%")


def main():
    """
    主函数

    执行所有测试函数，包括基本功能测试、边界情况测试和批量处理测试。
    捕获并报告测试过程中的异常。

    Returns:
        int: 成功返回0，失败返回1
    """
    try:
        test_basic_functionality()
        test_edge_cases()
        test_batch_processing()
        
        print("\n=== 所有测试完成 ===")
        print("工具运行正常！")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())