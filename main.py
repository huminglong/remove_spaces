#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word文档中英文空格清理工具 - 主程序入口

该工具用于检测并去除Word文档中英文与中文文本之间的多余空格，
同时严格保留英文单词之间的正常空格。
"""

import sys
import os

# 将src目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui.main_window import main
except ImportError as e:
    print(f"导入错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"程序运行出错: {e}")
        sys.exit(1)