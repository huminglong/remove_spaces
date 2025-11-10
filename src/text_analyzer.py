import re
from typing import List, Tuple, Dict


class TextAnalyzer:
    """文本分析器，负责识别中英文边界"""
    
    def __init__(self):
        # 中文字符范围（Unicode编码）- 简化的常用中文字符范围
        self.chinese_pattern = r'[\u4e00-\u9fff]'
        
        # 英文字符（包括字母、数字、常见符号）
        self.english_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?')
        
        # 编译正则表达式以提高性能
        self.chinese_regex = re.compile(self.chinese_pattern)
        self.whitespace_regex = re.compile(r'\s+')
    
    def is_chinese_char(self, char: str) -> bool:
        """判断字符是否为中文"""
        if len(char) != 1:
            return False
        return bool(self.chinese_regex.match(char))
    
    def is_english_char(self, char: str) -> bool:
        """判断字符是否为英文（包括字母、数字）"""
        if len(char) != 1:
            return False
        return char in self.english_chars
    
    def is_whitespace(self, char: str) -> bool:
        """判断字符是否为空格"""
        return char.isspace()
    
    def find_chinese_english_boundaries(self, text: str) -> List[Dict[str, int]]:
        """
        找到中英文边界处的空格位置
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict]: 边界位置列表
        """
        boundaries = []
        
        # 扫描整个文本，查找中英文之间的空格
        i = 0
        while i < len(text):
            if text[i].isspace():
                # 找到空格序列的开始
                space_start = i
                
                # 找到空格序列的结束
                while i < len(text) and text[i].isspace():
                    i += 1
                space_end = i
                
                # 检查前一个字符（空格序列前的字符）
                prev_char = text[space_start-1] if space_start > 0 else ''
                # 检查后一个字符（空格序列后的字符）
                next_char = text[space_end] if space_end < len(text) else ''
                
                if prev_char and next_char:  # 确保前后都有字符
                    # 检测中英文转换
                    if (self.is_chinese_char(prev_char) and self.is_english_char(next_char)) or \
                       (self.is_english_char(prev_char) and self.is_chinese_char(next_char)):
                        
                        # 记录整个空格序列
                        boundaries.append({
                            'start': space_start,
                            'end': space_end,
                            'type': 'chinese_english_boundary',
                            'description': f'Removed {space_end - space_start} space(s) between {prev_char} and {next_char}'
                        })
            else:
                i += 1
        
        return boundaries
    
    def analyze_text(self, text: str) -> Dict:
        """
        分析文本，返回详细的分析结果
        
        Args:
            text: 输入文本
            
        Returns:
            Dict: 分析结果，包含边界信息、统计信息等
        """
        if not text:
            return {
                'text': text,
                'boundaries': [],
                'chinese_chars': 0,
                'english_chars': 0,
                'spaces': 0,
                'has_mixed_content': False
            }
        
        boundaries = self.find_chinese_english_boundaries(text)
        
        # 统计字符类型
        chinese_chars = sum(1 for char in text if self.is_chinese_char(char))
        english_chars = sum(1 for char in text if self.is_english_char(char))
        spaces = sum(1 for char in text if self.is_whitespace(char))
        
        # 判断是否包含混合内容
        has_mixed_content = chinese_chars > 0 and english_chars > 0
        
        return {
            'text': text,
            'boundaries': boundaries,
            'chinese_chars': chinese_chars,
            'english_chars': english_chars,
            'spaces': spaces,
            'has_mixed_content': has_mixed_content,
            'total_boundary_spaces': len(boundaries)
        }
    
    def get_text_segments(self, text: str) -> List[Dict]:
        """
        将文本分割为不同的段，标记中英文部分
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict]: 文本段列表
        """
        segments = []
        current_segment = ""
        current_type = None
        
        for i, char in enumerate(text):
            if self.is_whitespace(char):
                # 空格字符，保持当前段类型
                if current_type is not None:
                    current_segment += char
                continue
            
            char_type = None
            if self.is_chinese_char(char):
                char_type = 'chinese'
            elif self.is_english_char(char):
                char_type = 'english'
            else:
                char_type = 'other'
            
            if current_type is None:
                # 第一个字符
                current_type = char_type
                current_segment = char
            elif current_type == char_type:
                # 相同类型，继续当前段
                current_segment += char
            else:
                # 类型改变，保存当前段并开始新段
                if current_segment:
                    segments.append({
                        'text': current_segment,
                        'type': current_type,
                        'start': i - len(current_segment),
                        'end': i - 1
                    })
                
                current_type = char_type
                current_segment = char
        
        # 保存最后一个段
        if current_segment:
            segments.append({
                'text': current_segment,
                'type': current_type,
                'start': len(text) - len(current_segment),
                'end': len(text) - 1
            })
        
        return segments
    
    def _simulate_processing(self, text: str, boundaries: List[Dict]) -> str:
        """模拟处理过程，用于预览"""
        if not boundaries:
            return text
        
        # 创建字符列表以便修改
        chars = list(text)
        
        # 从后向前处理，避免位置偏移
        for boundary in reversed(boundaries):
            start = boundary['start']
            end = boundary['end']
            
            # 移除边界空格
            for i in range(start, end):
                if i < len(chars):
                    chars[i] = ''
        
        return ''.join(chars)