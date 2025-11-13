"""
项目配置管理

统一管理项目中的各种配置参数,避免硬编码。
"""

from typing import Tuple, List


class Settings:
    """项目全局配置类"""
    
    # ==================== 窗口配置 ====================
    class Window:
        """GUI窗口配置"""
        WIDTH = 1200
        HEIGHT = 800
        X_POSITION = 100
        Y_POSITION = 100
        TITLE = 'Word文档中英文空格清理工具'
    
    # ==================== UI配置 ====================
    class UI:
        """UI组件配置"""
        # 分割器配置
        SPLITTER_LEFT_WIDTH = 600
        SPLITTER_RIGHT_WIDTH = 600
        
        # 文本预览配置
        TEXT_PREVIEW_MAX_LENGTH = 100
        
        # 字体配置
        DEFAULT_FONT_FAMILY = 'Microsoft YaHei'
        DEFAULT_FONT_SIZE = 10
        CODE_FONT_FAMILY = 'Consolas'
        CODE_FONT_SIZE = 10
    
    # ==================== 路径配置 ====================
    class Paths:
        """文件路径配置"""
        OUTPUT_DIR = 'processed_documents'
        TEMP_DIR = 'temp'
        LOG_DIR = 'logs'
        LOG_FILE = 'logs/app.log'
    
    # ==================== 文本分析配置 ====================
    class TextAnalysis:
        """文本分析相关配置"""
        # 中文字符Unicode范围
        CHINESE_RANGES: List[Tuple[int, int]] = [
            (0x4E00, 0x9FFF),    # CJK Unified Ideographs (基本汉字)
            (0x3400, 0x4DBF),    # CJK Unified Ideographs Extension A (扩展A)
            (0x20000, 0x2A6DF),  # CJK Unified Ideographs Extension B (扩展B)
            (0x2A700, 0x2B73F),  # CJK Unified Ideographs Extension C (扩展C)
            (0x2B740, 0x2B81F),  # CJK Unified Ideographs Extension D (扩展D)
            (0x2B820, 0x2CEAF),  # CJK Unified Ideographs Extension E (扩展E)
            (0xF900, 0xFAFF),    # CJK Compatibility Ideographs (兼容汉字)
            (0x2F800, 0x2FA1F),  # CJK Compatibility Ideographs Supplement (兼容汉字补充)
        ]
        
        # 英文字符Unicode范围
        ENGLISH_RANGES: List[Tuple[int, int]] = [
            (0x0041, 0x005A),  # 大写字母 A-Z
            (0x0061, 0x007A),  # 小写字母 a-z
        ]
        
        # 数字字符Unicode范围
        DIGIT_RANGES: List[Tuple[int, int]] = [
            (0x0030, 0x0039),  # 数字 0-9
        ]
    
    # ==================== 文档处理配置 ====================
    class DocumentProcessing:
        """文档处理相关配置"""
        # 支持的文件扩展名
        SUPPORTED_EXTENSIONS = ['.docx']
        
        # 最大文档大小 (字节)
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
        
        # 批处理配置
        BATCH_SIZE = 10
        MAX_WORKERS = 4  # 并发处理的最大线程数
    
    # ==================== 日志配置 ====================
    class Logging:
        """日志配置"""
        LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        
        # 是否输出到控制台
        CONSOLE_OUTPUT = True
        
        # 是否输出到文件
        FILE_OUTPUT = True
        
        # 日志文件最大大小 (字节)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        
        # 保留的日志文件数量
        BACKUP_COUNT = 5


# 创建全局配置实例
settings = Settings()
