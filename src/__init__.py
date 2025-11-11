"""
文件名: src/__init__.py
功能描述: 核心模块的初始化文件，导出主要的文档处理和文本分析类
主要函数: 无
主要类: 无
"""

# 项目主目录
from .document_processor import DocumentProcessor
from .text_analyzer import TextAnalyzer
from .space_cleaner import SpaceCleaner

__version__ = "1.0.0"
__author__ = "Word Space Cleaner Tool"