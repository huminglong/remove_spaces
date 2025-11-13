"""
快速验证脚本
测试优化后的核心功能是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """测试所有模块能否正常导入"""
    print("测试模块导入...")
    try:
        from src.exceptions import (
            DocumentLoadError, DocumentSaveError, 
            InvalidTextError, TextCleanerError
        )
        print("  ✓ exceptions 模块导入成功")
        
        from src.logger_config import setup_logger, get_logger
        print("  ✓ logger_config 模块导入成功")
        
        from config.settings import settings, Settings
        print("  ✓ settings 模块导入成功")
        
        from src.text_analyzer import TextAnalyzer
        print("  ✓ text_analyzer 模块导入成功")
        
        from src.space_cleaner import SpaceCleaner
        print("  ✓ space_cleaner 模块导入成功")
        
        from src.document_processor import DocumentProcessor
        print("  ✓ document_processor 模块导入成功")
        
        return True
    except Exception as e:
        print(f"  ✗ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_text_analyzer():
    """测试文本分析器"""
    print("\n测试文本分析器...")
    try:
        from src.text_analyzer import TextAnalyzer
        
        analyzer = TextAnalyzer()
        
        # 测试中文字符识别
        assert analyzer.is_chinese_char('中') == True
        assert analyzer.is_chinese_char('a') == False
        print("  ✓ 中文字符识别正常")
        
        # 测试英文字符识别
        assert analyzer.is_english_char('a') == True
        assert analyzer.is_english_char('Z') == True
        assert analyzer.is_english_char('5') == True
        assert analyzer.is_english_char('中') == False
        print("  ✓ 英文字符识别正常")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_space_cleaner():
    """测试空格清理器"""
    print("\n测试空格清理器...")
    try:
        from src.space_cleaner import SpaceCleaner
        from src.exceptions import InvalidTextError
        
        cleaner = SpaceCleaner()
        
        # 测试基本清理功能
        result = cleaner.clean_text("你好 world")
        assert 'cleaned_text' in result
        assert 'spaces_removed' in result
        print("  ✓ 基本清理功能正常")
        
        # 测试空字符串处理
        result = cleaner.clean_text("")
        assert result['cleaned_text'] == ""
        print("  ✓ 空字符串处理正常")
        
        # 测试输入验证
        try:
            cleaner.clean_text(None)
            print("  ✗ 应该抛出InvalidTextError")
            return False
        except InvalidTextError:
            print("  ✓ 输入验证正常")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_processor():
    """测试文档处理器"""
    print("\n测试文档处理器...")
    try:
        from src.document_processor import DocumentProcessor
        from src.exceptions import DocumentLoadError
        
        processor = DocumentProcessor()
        
        # 测试上下文管理器
        with DocumentProcessor() as proc:
            pass
        print("  ✓ 上下文管理器正常")
        
        # 测试输入验证
        try:
            processor.load_document("")
            print("  ✗ 应该抛出ValueError")
            return False
        except ValueError:
            print("  ✓ 空路径验证正常")
        
        try:
            processor.load_document("nonexistent.docx")
            print("  ✗ 应该抛出FileNotFoundError")
            return False
        except FileNotFoundError:
            print("  ✓ 文件存在性验证正常")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_settings():
    """测试配置系统"""
    print("\n测试配置系统...")
    try:
        from config.settings import settings
        
        # 测试窗口配置
        assert hasattr(settings.Window, 'WIDTH')
        assert hasattr(settings.Window, 'HEIGHT')
        print("  ✓ 窗口配置正常")
        
        # 测试文本分析配置
        assert hasattr(settings.TextAnalysis, 'CHINESE_RANGES')
        assert len(settings.TextAnalysis.CHINESE_RANGES) > 0
        print("  ✓ 文本分析配置正常")
        
        # 测试路径配置
        assert hasattr(settings.Paths, 'OUTPUT_DIR')
        print("  ✓ 路径配置正常")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logger():
    """测试日志系统"""
    print("\n测试日志系统...")
    try:
        from src.logger_config import setup_logger, get_logger
        
        # 创建logger
        logger = setup_logger("test_logger")
        assert logger is not None
        print("  ✓ Logger创建成功")
        
        # 测试日志记录
        logger.info("这是一条测试日志")
        logger.debug("这是一条调试日志")
        logger.warning("这是一条警告日志")
        print("  ✓ 日志记录功能正常")
        
        return True
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("开始验证优化后的代码")
    print("=" * 60)
    
    results = []
    
    results.append(("模块导入", test_imports()))
    results.append(("配置系统", test_settings()))
    results.append(("日志系统", test_logger()))
    results.append(("文本分析器", test_text_analyzer()))
    results.append(("空格清理器", test_space_cleaner()))
    results.append(("文档处理器", test_document_processor()))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n总计: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("\n🎉 所有测试通过! 优化成功!")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败,需要修复")
        return 1


if __name__ == "__main__":
    sys.exit(main())
