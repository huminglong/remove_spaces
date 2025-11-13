"""
文件名: tests/test_processor.py
功能描述: 使用pytest框架的单元测试文件，包含文本分析器、空格清理器、文档处理器和集成测试
主要函数: 无（pytest测试方法）
主要类:
  - TestTextAnalyzer: 文本分析器测试类
  - TestSpaceCleaner: 空格清理器测试类
  - TestDocumentProcessor: 文档处理器测试类
  - TestIntegration: 集成测试类
"""

import pytest
import sys
import os

# 将项目根目录添加到Python路径，以便导入src包
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.text_analyzer import TextAnalyzer
from src.space_cleaner import SpaceCleaner
from src.document_processor import DocumentProcessor


class TestTextAnalyzer:
    """
    测试文本分析器

    包含文本分析器的所有单元测试，包括字符识别、边界检测等功能。
    """

    def setup_method(self):
        """
        设置测试方法

        在每个测试方法执行前创建TextAnalyzer实例。
        """
        self.analyzer = TextAnalyzer()
    
    def test_chinese_char_detection(self):
        """测试中文字符检测"""
        assert self.analyzer.is_chinese_char('中') == True
        assert self.analyzer.is_chinese_char('国') == True
        assert self.analyzer.is_chinese_char('a') == False
        assert self.analyzer.is_chinese_char('1') == False
        assert self.analyzer.is_chinese_char(' ') == False
    
    def test_english_char_detection(self):
        """测试英文字符检测"""
        assert self.analyzer.is_english_char('a') == True
        assert self.analyzer.is_english_char('Z') == True
        assert self.analyzer.is_english_char('1') == True
        assert self.analyzer.is_english_char('!') == True
        assert self.analyzer.is_chinese_char('中') == True  # 中文不属于英文
        assert self.analyzer.is_english_char('中') == False
    
    def test_whitespace_detection(self):
        """测试空格检测"""
        assert self.analyzer.is_whitespace(' ') == True
        assert self.analyzer.is_whitespace('\t') == True
        assert self.analyzer.is_whitespace('\n') == True
        assert self.analyzer.is_whitespace('a') == False
        assert self.analyzer.is_whitespace('中') == False
    
    def test_find_chinese_english_boundaries(self):
        """测试中英文边界检测"""
        # 测试基本的中英文边界
        text = "你好 hello world"
        boundaries = self.analyzer.find_chinese_english_boundaries(text)
        assert len(boundaries) == 1
        assert boundaries[0]['start'] == 2  # "好"后面的空格位置
        assert boundaries[0]['end'] == 3
        
        # 测试多个边界
        text2 = "hello 你好 world 世界"
        boundaries2 = self.analyzer.find_chinese_english_boundaries(text2)
        assert len(boundaries2) == 3  # 有3个中英文边界
        
        # 测试没有边界的情况
        text3 = "hello world"
        boundaries3 = self.analyzer.find_chinese_english_boundaries(text3)
        assert len(boundaries3) == 0
    
    def test_analyze_text(self):
        """测试文本分析"""
        text = "你好 hello world"
        analysis = self.analyzer.analyze_text(text)
        
        assert analysis['text'] == text
        assert analysis['chinese_chars'] == 2
        assert analysis['english_chars'] == 10  # "hello world" (不包括空格)
        assert analysis['spaces'] == 2
        assert analysis['has_mixed_content'] == True
        assert analysis['total_boundary_spaces'] == 1
    
    def test_get_text_segments(self):
        """测试文本段分割"""
        text = "你好hello world"
        segments = self.analyzer.get_text_segments(text)
        
        assert len(segments) >= 2  # 至少应该有中文和英文段
        
        # 检查是否包含中文段
        chinese_segments = [s for s in segments if s['type'] == 'chinese']
        assert len(chinese_segments) > 0
        
        # 检查是否包含英文段
        english_segments = [s for s in segments if s['type'] == 'english']
        assert len(english_segments) > 0
    



class TestSpaceCleaner:
    """测试空格清理器"""
    
    def setup_method(self):
        """设置测试方法"""
        self.cleaner = SpaceCleaner()
    
    def test_clean_text_basic(self):
        """测试基本的文本清理"""
        text = "你好 hello world"
        result = self.cleaner.clean_text(text)
        
        assert result['original_text'] == text
        assert result['cleaned_text'] == "你好hello world"
        assert result['spaces_removed'] == 1
        assert len(result['changes']) == 1
    
    def test_clean_text_multiple_boundaries(self):
        """测试多个边界的清理"""
        text = "hello 你好 world 世界 test"
        result = self.cleaner.clean_text(text)
        
        # 应该移除中英文之间的空格
        assert "你好world" in result['cleaned_text']
        assert "世界test" in result['cleaned_text']
        assert result['spaces_removed'] >= 2
    
    def test_clean_text_no_changes(self):
        """测试不需要清理的文本"""
        text = "hello world"
        result = self.cleaner.clean_text(text)
        
        assert result['original_text'] == text
        assert result['cleaned_text'] == text
        assert result['spaces_removed'] == 0
        assert len(result['changes']) == 0
    
    def test_clean_text_preserve_english_spaces(self):
        """测试保留英文单词间的空格"""
        text = "你好 hello beautiful world"
        result = self.cleaner.clean_text(text)
        
        # 应该保留 "hello beautiful" 之间的空格
        assert "hello beautiful" in result['cleaned_text']
        # 但移除 "好" 和 "h" 之间的空格
        assert "你好hello" in result['cleaned_text']
    
    def test_clean_multiple_texts(self):
        """测试批量清理"""
        texts = [
            "你好 hello",
            "world 世界",
            "test text"
        ]
        
        results = self.cleaner.clean_multiple_texts(texts)
        
        assert len(results) == 3
        assert results[0]['spaces_removed'] == 1  # 第一个有变更
        assert results[1]['spaces_removed'] == 1  # 第二个有变更
        assert results[2]['spaces_removed'] == 0  # 第三个无变更
    
    def test_get_processing_statistics(self):
        """测试处理统计"""
        results = [
            {'spaces_removed': 2},
            {'spaces_removed': 0},
            {'spaces_removed': 1}
        ]
        
        stats = self.cleaner.get_processing_statistics(results)
        
        assert stats['total_texts'] == 3
        assert stats['texts_with_changes'] == 2
        assert stats['total_spaces_removed'] == 3
        assert stats['average_spaces_per_text'] == 1.0
        assert stats['change_rate'] == (2/3 * 100)
    



class TestDocumentProcessor:
    """测试文档处理器"""
    
    def setup_method(self):
        """设置测试方法"""
        self.processor = DocumentProcessor()
    
    def test_load_nonexistent_document(self):
        """测试加载不存在的文档"""
        result = self.processor.load_document("nonexistent.docx")
        assert result == False
    
    def test_get_document_info_empty(self):
        """测试空文档信息"""
        info = self.processor.get_document_info()
        assert info == {}
    
    def test_extract_runs_empty_paragraph(self):
        """测试空段落的runs提取"""
        # 这里需要模拟一个段落对象，但由于没有实际的Word文档，
        # 我们只能测试空输入的情况
        runs = self.processor._extract_runs(None)
        # 对于None输入，方法应该返回空列表或处理错误
        assert isinstance(runs, list)


class TestIntegration:
    """集成测试"""
    
    def setup_method(self):
        """设置测试方法"""
        self.analyzer = TextAnalyzer()
        self.cleaner = SpaceCleaner()
    
    def test_complete_workflow(self):
        """测试完整工作流程"""
        # 模拟包含中英文混合的文本
        test_texts = [
            "这是一个测试 hello world",
            "Python 编程语言",
            "机器学习 machine learning 很有趣",
            "No Chinese here",
            "只有中文没有英文"
        ]
        
        for text in test_texts:
            # 分析文本
            analysis = self.analyzer.analyze_text(text)
            
            # 清理文本
            cleaned = self.cleaner.clean_text(text)
            
            # 验证结果
            assert 'original_text' in cleaned
            assert 'cleaned_text' in cleaned
            assert 'spaces_removed' in cleaned
            assert 'changes' in cleaned
            
            # 验证清理逻辑
            if analysis['has_mixed_content'] and analysis['total_boundary_spaces'] > 0:
                assert cleaned['spaces_removed'] > 0
                assert cleaned['cleaned_text'] != text
            else:
                assert cleaned['spaces_removed'] == 0
                assert cleaned['cleaned_text'] == text
    
    def test_complex_mixed_content(self):
        """测试复杂的中英文混合内容"""
        complex_text = "人工智能 AI 和 machine learning 机器学习 是 current hot topics 热门话题"
        
        # 分析
        analysis = self.analyzer.analyze_text(complex_text)
        
        # 清理
        cleaned = self.cleaner.clean_text(complex_text)
        
        # 验证
        assert analysis['has_mixed_content'] == True
        assert analysis['total_boundary_spaces'] > 0
        assert cleaned['spaces_removed'] > 0
        
        # 验证英文单词间的空格被保留
        cleaned_text = cleaned['cleaned_text']
        assert "AI和" in cleaned_text  # 移除了中英文间的空格
        assert "和machine" in cleaned_text  # 移除了中英文间的空格
        assert "machine learning" in cleaned_text  # 保留了英文单词间的空格
        assert "learning机器学习" in cleaned_text  # 移除了中英文间的空格


if __name__ == '__main__':
    # 运行测试
    pytest.main([__file__, '-v'])