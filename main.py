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

# PyInstaller运行时的资源路径处理
if getattr(sys, 'frozen', False):
    # 打包后的exe运行环境
    application_path = sys._MEIPASS
else:
    # 开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))

# 将必要的目录添加到Python路径
sys.path.insert(0, os.path.join(application_path, 'src'))
sys.path.insert(0, application_path)

try:
    from gui.main_window import main
except ImportError as e:
    print(f"导入错误: {e}")
    import traceback
    traceback.print_exc()
    input("按Enter键退出...")
    sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按Enter键退出...")
        sys.exit(1)