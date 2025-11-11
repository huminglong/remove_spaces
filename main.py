#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名: main.py
功能描述: Word文档中英文空格清理工具的主程序入口文件，负责启动GUI应用程序
主要函数:
  - main(): 主函数，启动GUI应用程序
主要类: 无
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