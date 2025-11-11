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


def main():
    """
    主函数，启动GUI应用程序

    该函数负责启动Word文档中英文空格清理工具的图形用户界面，
    包括创建应用程序实例和显示主窗口。

    Returns:
        无返回值，程序正常退出时返回0，异常时返回1
    """
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle('Fusion')

    # 创建并显示主窗口
    main_window = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"程序运行出错: {e}")
        sys.exit(1)