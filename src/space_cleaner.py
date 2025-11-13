"""
文件名: src/space_cleaner.py
功能描述: 空格清理器，负责识别和移除中英文边界处的多余空格，同时保留英文单词间的正常空格
主要函数:
  - clean_text(): 清理单个文本中的中英文边界空格
  - clean_multiple_texts(): 批量清理多个文本
  - get_processing_statistics(): 获取处理统计信息
主要类:
  - SpaceCleaner: 空格清理核心类
"""

from typing import List, Dict, Tuple, Optional
from src.text_analyzer import TextAnalyzer
from src.exceptions import InvalidTextError
from src.logger_config import setup_logger


class SpaceCleaner:
    """
    空格清理器，负责移除中英文边界的多余空格

    该类使用文本分析器识别中英文边界处的多余空格，并进行清理，
    同时保留英文单词间的正常空格。

    Attributes:
        analyzer: TextAnalyzer实例，用于文本分析
    """

    def __init__(self):
        """
        初始化空格清理器

        创建SpaceCleaner实例并初始化文本分析器。
        """
        self.analyzer = TextAnalyzer()
        self.logger = setup_logger(__name__)
    
    def clean_text(self, text: str) -> Dict:
        """
        清理文本中的中英文边界空格
        
        执行输入验证并清理文本中中英文边界的多余空格。
        
        Args:
            text: 输入文本
            
        Returns:
            Dict: 处理结果，包含清理后的文本和统计信息
            
        Raises:
            InvalidTextError: 当输入文本无效时抛出
            
        Examples:
            >>> cleaner = SpaceCleaner()
            >>> result = cleaner.clean_text("你好 world")
            >>> print(result['cleaned_text'])
            '你好world'
        """
        # 输入验证
        if text is None:
            self.logger.error("输入文本不能为None")
            raise InvalidTextError("输入文本不能为None")
        
        if not isinstance(text, str):
            self.logger.error(f"输入必须是字符串类型，实际类型: {type(text)}")
            raise InvalidTextError(f"输入必须是字符串类型，实际类型: {type(text)}")
        
        if not text:
            self.logger.debug("输入为空字符串，直接返回")
            return {
                'original_text': text,
                'cleaned_text': text,
                'spaces_removed': 0,
                'changes': []
            }
        
        try:
            self.logger.debug(f"开始清理文本，长度: {len(text)}")
            
            # 分析文本
            analysis = self.analyzer.analyze_text(text)
            boundaries = analysis['boundaries']
            
            if not boundaries:
                self.logger.debug("未发现需要清理的边界空格")
                return {
                    'original_text': text,
                    'cleaned_text': text,
                    'spaces_removed': 0,
                    'changes': []
                }
            
            # 清理空格
            cleaned_text, changes = self._remove_boundary_spaces(text, boundaries)
            
            self.logger.debug(f"清理完成，移除了 {len(changes)} 处空格")
            return {
                'original_text': text,
                'cleaned_text': cleaned_text,
                'spaces_removed': len(changes),
                'changes': changes,
                'analysis': analysis
            }
            
        except InvalidTextError:
            # 重新抛出验证错误
            raise
        except Exception as e:
            self.logger.error(f"清理文本时发生错误: {str(e)}", exc_info=True)
            # 发生错误时返回原文本
            return {
                'original_text': text,
                'cleaned_text': text,
                'spaces_removed': 0,
                'changes': [],
                'error': str(e)
            }
    
    def _remove_boundary_spaces(self, text: str, boundaries: List[Dict]) -> Tuple[str, List[Dict]]:
        """
        移除边界空格(内存优化版本)

        使用字符串分段和join替代完整字符列表,减少内存占用。
        对于大文档,这种方法比创建完整字符列表更高效。

        Args:
            text: 原始文本
            boundaries: 边界信息列表，每个元素包含start、end等字段

        Returns:
            Tuple[str, List[Dict]]: 元组(清理后的文本, 变更记录列表)
            
        Examples:
            >>> cleaner = SpaceCleaner()
            >>> text = "你好 world"
            >>> boundaries = [{'start': 2, 'end': 3, 'type': 'boundary', 'description': 'test'}]
            >>> cleaned, changes = cleaner._remove_boundary_spaces(text, boundaries)
        """
        if not boundaries:
            return text, []
        
        # 按起始位置排序边界
        sorted_boundaries = sorted(boundaries, key=lambda x: x['start'])
        
        # 使用字符串分段,避免创建完整字符列表
        segments = []
        changes = []
        last_end = 0
        
        for boundary in sorted_boundaries:
            start = boundary['start']
            end = boundary['end']
            
            # 添加上一个边界结束到当前边界开始之间的文本
            if start > last_end:
                segments.append(text[last_end:start])
            
            # 记录变更
            removed_spaces = text[start:end]
            if removed_spaces.strip():  # 只记录非空的移除
                changes.append({
                    'position': start,
                    'removed': removed_spaces,
                    'type': boundary.get('type', 'boundary'),
                    'description': boundary.get('description', 'Removed space')
                })
            
            # 跳过边界空格(不添加到segments中)
            last_end = end
        
        # 添加最后一个边界之后的文本
        if last_end < len(text):
            segments.append(text[last_end:])
        
        # 合并所有段落
        cleaned_text = ''.join(segments)
        
        # 清理可能产生的多余空格
        cleaned_text = self._normalize_spaces(cleaned_text)
        
        return cleaned_text, changes
    
    def _normalize_spaces(self, text: str) -> str:
        """
        规范化空格，确保英文单词间有适当的空格

        处理多个连续空格的情况，并确保中英文边界处没有空格，
        但保留英文单词之间的必要空格。

        Args:
            text: 输入文本

        Returns:
            str: 规范化后的文本
        """
        if not text:
            return text
        
        # 简单的空格规范化：将多个连续空格替换为单个空格
        # 但保留英文单词间的必要空格
        import re
        
        # 首先处理多个连续空格的情况
        text = re.sub(r'\s+', ' ', text)
        
        # 然后处理特定的边界情况
        # 移除中英文边界处的空格，但保留英文单词间的空格
        result = ""
        i = 0
        while i < len(text):
            if text[i].isspace():
                # 检查这个空格是否在中英文边界
                prev_char = text[i-1] if i > 0 else ''
                next_char = text[i+1] if i+1 < len(text) else ''
                
                # 如果是中英文边界处的空格，移除它
                if prev_char and next_char and ((self.analyzer.is_chinese_char(prev_char) and self.analyzer.is_english_char(next_char)) or \
                   (self.analyzer.is_english_char(prev_char) and self.analyzer.is_chinese_char(next_char))):
                    # 跳过这个空格
                    i += 1
                    continue
            
            result += text[i]
            i += 1
        
        return result
    
    def clean_multiple_texts(self, texts: List[str]) -> List[Dict]:
        """
        批量清理多个文本
        
        Args:
            texts: 文本列表
            
        Returns:
            List[Dict]: 每个文本的处理结果
        """
        results = []
        
        for text in texts:
            result = self.clean_text(text)
            results.append(result)
        
        return results
    
    def get_processing_statistics(self, results: List[Dict]) -> Dict:
        """
        获取处理统计信息
        
        Args:
            results: 处理结果列表
            
        Returns:
            Dict: 统计信息
        """
        if not results:
            return {
                'total_texts': 0,
                'texts_with_changes': 0,
                'total_spaces_removed': 0,
                'average_spaces_per_text': 0
            }
        
        total_texts = len(results)
        texts_with_changes = sum(1 for r in results if r['spaces_removed'] > 0)
        total_spaces_removed = sum(r['spaces_removed'] for r in results)
        average_spaces_per_text = total_spaces_removed / total_texts if total_texts > 0 else 0
        
        return {
            'total_texts': total_texts,
            'texts_with_changes': texts_with_changes,
            'total_spaces_removed': total_spaces_removed,
            'average_spaces_per_text': average_spaces_per_text,
            'change_rate': (texts_with_changes / total_texts * 100) if total_texts > 0 else 0
        }