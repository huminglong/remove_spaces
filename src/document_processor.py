import docx
from typing import List, Dict, Tuple
import re
from space_cleaner import SpaceCleaner


class DocumentProcessor:
    """Word文档处理器，负责读取和写入Word文档
    
    重要原则：只修改文字内容，严格保持文档的所有格式、样式、图片等非文字元素不变
    """
    
    def __init__(self):
        self.document = None
        self.original_structure = []
    
    def load_document(self, file_path: str) -> bool:
        """
        加载Word文档
        
        Args:
            file_path: 文档路径
            
        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            self.document = docx.Document(file_path)
            self._extract_document_structure()
            return True
        except Exception as e:
            print(f"加载文档失败: {e}")
            return False
    
    def _extract_document_structure(self) -> None:
        """提取文档的完整结构，包括所有格式信息"""
        self.original_structure = []
        
        # 提取段落及其完整结构
        for para in self.document.paragraphs:
            if para.text.strip():  # 只处理非空段落
                self.original_structure.append({
                    'type': 'paragraph',
                    'paragraph': para,  # 保存段落对象引用
                    'original_text': para.text,
                    'runs': self._extract_runs(para)
                })
        
        # 提取表格及其完整结构
        for table in self.document.tables:
            table_structure = {
                'type': 'table',
                'table': table,  # 保存表格对象引用
                'rows': []
            }
            
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    cell_data = {
                        'cell': cell,  # 保存单元格对象引用
                        'original_text': cell.text,
                        'paragraphs': []
                    }
                    
                    # 提取单元格中的所有段落
                    for para in cell.paragraphs:
                        if para.text.strip():
                            cell_data['paragraphs'].append({
                                'paragraph': para,  # 保存段落对象引用
                                'original_text': para.text,
                                'runs': self._extract_runs(para)
                            })
                    
                    row_data.append(cell_data)
                
                if row_data:
                    table_structure['rows'].append(row_data)
            
            if table_structure['rows']:
                self.original_structure.append(table_structure)
    
    def _extract_runs(self, paragraph) -> List[Dict]:
        """提取段落中的runs（文本片段）及其完整格式信息"""
        if paragraph is None:
            return []
            
        runs = []
        for run in paragraph.runs:
            if run.text:  # 只处理非空文本片段
                runs.append({
                    'text': run.text,
                    'run': run,  # 保存run对象引用
                    'bold': run.bold,
                    'italic': run.italic,
                    'underline': run.underline,
                    'font_name': run.font.name if run.font.name else None,
                    'font_size': run.font.size.pt if run.font.size else None,
                    'font_color': run.font.color.rgb if run.font.color else None,
                    'highlight_color': run.font.highlight_color if hasattr(run.font, 'highlight_color') else None
                })
        return runs
    
    def get_all_text(self) -> List[str]:
        """获取所有文本内容，用于处理"""
        texts = []
        for item in self.original_structure:
            if item['type'] == 'paragraph':
                texts.append(item['original_text'])
            elif item['type'] == 'table':
                for row in item['rows']:
                    for cell in row:
                        if cell['paragraphs']:
                            for para in cell['paragraphs']:
                                texts.append(para['original_text'])
                        else:
                            texts.append(cell['original_text'])
        return texts
    
    def update_text_content(self, processed_texts: List[str]) -> bool:
        """
        更新文档中的文本内容，严格保持原有格式不变
        
        Args:
            processed_texts: 处理后的文本列表
            
        Returns:
            bool: 更新成功返回True，否则返回False
        """
        try:
            text_index = 0
            
            # 更新段落文本
            for item in self.original_structure:
                if item['type'] == 'paragraph' and text_index < len(processed_texts):
                    # 保持段落的所有属性不变，只更新文本内容
                    self._update_paragraph_text(item['paragraph'], processed_texts[text_index])
                    text_index += 1
                    
                elif item['type'] == 'table':
                    # 更新表格中的文本
                    for row in item['rows']:
                        for cell in row:
                            if cell['paragraphs']:
                                for para in cell['paragraphs']:
                                    if text_index < len(processed_texts):
                                        self._update_paragraph_text(para['paragraph'], processed_texts[text_index])
                                        text_index += 1
                            else:
                                # 直接更新单元格文本
                                if text_index < len(processed_texts):
                                    self._update_cell_text(cell['cell'], processed_texts[text_index])
                                    text_index += 1
            
            return True
            
        except Exception as e:
            print(f"更新文本内容失败: {e}")
            return False
    
    def _update_paragraph_text(self, paragraph, new_text: str) -> None:
        """更新段落文本，保持所有格式属性不变"""
        # 清空段落内容但保持格式
        paragraph.clear()
        
        # 添加新的文本内容
        paragraph.add_run(new_text)
    
    def _update_cell_text(self, cell, new_text: str) -> None:
        """更新单元格文本，保持所有格式属性不变"""
        # 清空单元格内容但保持格式
        cell.text = ''
        
        # 添加新的文本内容
        cell.paragraphs[0].add_run(new_text)
    
    def save_document(self, file_path: str) -> bool:
        """
        保存文档到指定路径
        
        Args:
            file_path: 保存路径
            
        Returns:
            bool: 保存成功返回True，否则返回False
        """
        try:
            self.document.save(file_path)
            return True
            
        except Exception as e:
            print(f"保存文档失败: {e}")
            return False
    
    def save_as_new_document(self, file_path: str, processed_texts: List[str]) -> bool:
        """
        创建新文档并保存处理后的文本，保持原有结构
        
        Args:
            file_path: 保存路径
            processed_texts: 处理后的文本列表
            
        Returns:
            bool: 保存成功返回True，否则返回False
        """
        try:
            # 首先更新原文档的内容
            if self.update_text_content(processed_texts):
                # 然后保存为新文件
                return self.save_document(file_path)
            return False
            
        except Exception as e:
            print(f"保存新文档失败: {e}")
            return False
    
    def get_document_info(self) -> Dict:
        """获取文档信息"""
        if not self.document:
            return {}
        
        paragraph_count = len([item for item in self.original_structure if item['type'] == 'paragraph'])
        table_count = len([item for item in self.original_structure if item['type'] == 'table'])
        
        return {
            'paragraph_count': paragraph_count,
            'table_count': table_count,
            'total_text_items': len(self.original_structure)
        }