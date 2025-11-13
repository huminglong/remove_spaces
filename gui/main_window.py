"""
文件名: gui/main_window.py
功能描述: 主窗口GUI实现，包含文档处理的用户界面和处理逻辑
主要函数:
  - main(): 应用程序主入口函数
主要类:
  - ProcessingThread: 后台文档处理线程
  - MainWindow: 主应用程序窗口类
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QTextEdit, QLabel,
                              QFileDialog, QMessageBox, QProgressBar,
                              QGroupBox, QSplitter, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from src.document_processor import DocumentProcessor
from src.space_cleaner import SpaceCleaner


class ProcessingThread(QThread):
    """
    处理线程，用于在后台处理文档

    该线程类负责在后台执行文档处理任务，包括加载文档、
    清理文本和生成统计信息，避免阻塞主UI线程。

    Attributes:
        progress_updated: 进度更新信号，参数为进度百分比(0-100)
        processing_completed: 处理完成信号，参数为(结果列表, 统计信息字典)
        error_occurred: 错误发生信号，参数为错误消息字符串
    """
    progress_updated = pyqtSignal(int)
    processing_completed = pyqtSignal(list, dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, processor, cleaner, file_path):
        """
        初始化处理线程

        Args:
            processor: DocumentProcessor实例，用于处理Word文档
            cleaner: SpaceCleaner实例，用于清理文本空格
            file_path: 要处理的文档文件路径
        """
        super().__init__()
        self.processor = processor
        self.cleaner = cleaner
        self.file_path = file_path
    
    def run(self):
        """
        执行文档处理任务

        该方法在后台线程中执行完整的文档处理流程：
        1. 加载Word文档
        2. 提取所有文本内容
        3. 清理中英文边界空格
        4. 生成处理统计信息

        处理过程中会通过信号实时报告进度，处理完成后发送结果或错误信息。
        """
        try:
            # 加载文档
            self.progress_updated.emit(10)

            if not self.processor.load_document(self.file_path):
                self.error_occurred.emit("无法加载文档")
                return

            # 获取所有文本
            self.progress_updated.emit(30)
            texts = self.processor.get_all_text()

            if not texts:
                self.error_occurred.emit("文档中没有找到文本内容")
                return

            # 清理文本
            self.progress_updated.emit(50)
            results = self.cleaner.clean_multiple_texts(texts)

            # 获取统计信息
            self.progress_updated.emit(80)
            statistics = self.cleaner.get_processing_statistics(results)

            self.progress_updated.emit(100)
            self.processing_completed.emit(results, statistics)

        except Exception as e:
            self.error_occurred.emit(f"处理过程中发生错误: {str(e)}")


class MainWindow(QMainWindow):
    """
    主窗口类

    该类实现Word文档中英文空格清理工具的图形用户界面，
    提供文档加载、处理、预览和保存等功能。

    Attributes:
        processor: DocumentProcessor实例，用于处理Word文档
        cleaner: SpaceCleaner实例，用于清理文本空格
        current_file_path: 当前加载的文档路径
        processing_results: 文档处理结果列表
    """

    def __init__(self):
        """
        初始化主窗口

        创建必要的组件实例并初始化用户界面。
        """
        super().__init__()
        self.processor = DocumentProcessor()
        self.cleaner = SpaceCleaner()
        self.current_file_path = None
        self.processing_results = []

        self.init_ui()
    
    def init_ui(self):
        """
        初始化用户界面

        设置窗口基本属性，创建并布局所有UI组件，包括工具栏、
        主要内容区域和状态栏。
        """
        self.setWindowTitle('Word文档中英文空格清理工具')
        self.setGeometry(100, 100, 1200, 800)

        # 设置应用图标
        # self.setWindowIcon(QIcon('icon.png'))

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)

        # 创建工具栏
        self.create_toolbar(main_layout)

        # 创建主要内容区域
        self.create_main_content(main_layout)

        # 创建状态栏
        self.create_status_bar()

        self.show()
    
    def create_toolbar(self, parent_layout):
        """
        创建工具栏

        创建包含打开文件、处理文档和保存结果按钮的工具栏，
        并设置相应的点击事件处理器。

        Args:
            parent_layout: 父布局，用于添加工具栏布局
        """
        toolbar_layout = QHBoxLayout()

        # 打开文件按钮
        self.open_btn = QPushButton('打开Word文档')
        self.open_btn.clicked.connect(self.open_file)
        toolbar_layout.addWidget(self.open_btn)

        # 处理按钮
        self.process_btn = QPushButton('处理文档')
        self.process_btn.clicked.connect(self.process_document)
        self.process_btn.setEnabled(False)
        toolbar_layout.addWidget(self.process_btn)

        # 保存按钮
        self.save_btn = QPushButton('保存处理结果')
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setEnabled(False)
        toolbar_layout.addWidget(self.save_btn)

        toolbar_layout.addStretch()

        parent_layout.addLayout(toolbar_layout)
    
    def create_main_content(self, parent_layout):
        """
        创建主要内容区域

        创建并布局主要内容区域，包括原始文本展示区、处理后文本展示区、
        统计信息显示、进度条和详细信息表格。

        Args:
            parent_layout: 父布局，用于添加主内容组件
        """
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：原始文本
        left_group = QGroupBox("原始文本")
        left_layout = QVBoxLayout()
        
        self.original_text_edit = QTextEdit()
        self.original_text_edit.setReadOnly(True)
        self.original_text_edit.setFont(QFont("Consolas", 10))
        left_layout.addWidget(self.original_text_edit)
        
        left_group.setLayout(left_layout)
        splitter.addWidget(left_group)
        
        # 右侧：处理后的文本
        right_group = QGroupBox("处理后的文本")
        right_layout = QVBoxLayout()
        
        self.processed_text_edit = QTextEdit()
        self.processed_text_edit.setReadOnly(True)
        self.processed_text_edit.setFont(QFont("Consolas", 10))
        right_layout.addWidget(self.processed_text_edit)
        
        right_group.setLayout(right_layout)
        splitter.addWidget(right_group)
        
        # 设置分割器比例
        splitter.setSizes([600, 600])
        
        parent_layout.addWidget(splitter)
        
        # 底部：统计信息和进度条
        bottom_layout = QVBoxLayout()
        
        # 统计标签
        self.stats_label = QLabel("统计信息: 未加载文档")
        bottom_layout.addWidget(self.stats_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        bottom_layout.addWidget(self.progress_bar)
        
        # 详细信息表格
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(4)
        self.details_table.setHorizontalHeaderLabels(['原始文本', '处理后文本', '移除空格数', '变更详情'])
        self.details_table.setVisible(False)
        bottom_layout.addWidget(self.details_table)
        
        parent_layout.addLayout(bottom_layout)
    
    def create_status_bar(self):
        """
        创建状态栏

        初始化窗口底部的状态栏，用于显示应用程序的当前状态信息。
        """
        self.statusBar().showMessage('就绪')
    
    def open_file(self):
        """
        打开Word文档

        打开文件选择对话框让用户选择Word文档，选定后加载文档
        并显示预览内容。
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择Word文档",
            "",
            "Word文档 (*.docx);;所有文件 (*)"
        )

        if file_path:
            self.current_file_path = file_path
            self.load_document_preview(file_path)
    
    def load_document_preview(self, file_path):
        """
        加载文档并显示预览

        加载Word文档，提取其中的文本内容并在界面上显示预览。
        同时更新文档统计信息并启用处理按钮。

        Args:
            file_path: Word文档的完整路径
        """
        try:
            # 加载文档
            if not self.processor.load_document(file_path):
                QMessageBox.critical(self, "错误", "无法加载文档")
                return
            
            # 获取文档信息
            doc_info = self.processor.get_document_info()
            
            # 获取所有文本
            texts = self.processor.get_all_text()
            
            # 显示原始文本
            self.original_text_edit.clear()
            for i, text in enumerate(texts):
                self.original_text_edit.append(f"=== 文本段 {i+1} ===")
                self.original_text_edit.append(text)
                self.original_text_edit.append("")
            
            # 更新统计信息
            self.stats_label.setText(
                f"文档信息: 段落数={doc_info.get('paragraph_count', 0)}, "
                f"表格数={doc_info.get('table_count', 0)}, "
                f"文本项数={doc_info.get('total_text_items', 0)}"
            )
            
            # 启用处理按钮
            self.process_btn.setEnabled(True)
            
            self.statusBar().showMessage(f"已加载: {os.path.basename(file_path)}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载文档时发生错误: {str(e)}")
    
    def process_document(self):
        """
        处理文档

        启动后台处理线程来清理当前加载文档中的中英文边界空格。
        处理过程中显示进度条并禁用相关按钮。
        """
        if not self.current_file_path:
            return

        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # 禁用按钮
        self.process_btn.setEnabled(False)
        self.open_btn.setEnabled(False)

        # 创建处理线程
        self.processing_thread = ProcessingThread(
            self.processor, self.cleaner, self.current_file_path
        )

        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.processing_completed.connect(self.processing_finished)
        self.processing_thread.error_occurred.connect(self.processing_error)

        self.processing_thread.start()
    
    def update_progress(self, value):
        """
        更新进度条

        接收后台线程发送的进度更新信号，并更新进度条显示。

        Args:
            value: 进度百分比（0-100）
        """
        self.progress_bar.setValue(value)
    
    def processing_finished(self, results, statistics):
        """
        处理完成

        处理后台线程处理完成后的回调，显示处理后的文本、
        统计信息和详细变更表格。

        Args:
            results: 处理结果列表
            statistics: 统计信息字典
        """
        self.processing_results = results
        
        # 显示处理后的文本
        self.processed_text_edit.clear()
        for i, result in enumerate(results):
            self.processed_text_edit.append(f"=== 处理后的文本段 {i+1} ===")
            self.processed_text_edit.append(result['cleaned_text'])
            self.processed_text_edit.append("")
        
        # 显示统计信息
        stats_text = (
            f"处理统计: 总文本数={statistics['total_texts']}, "
            f"有变更文本数={statistics['texts_with_changes']}, "
            f"总移除空格数={statistics['total_spaces_removed']}, "
            f"变更率={statistics['change_rate']:.1f}%"
        )
        self.stats_label.setText(stats_text)
        
        # 显示详细信息
        self.show_details_table(results)
        
        # 隐藏进度条，启用按钮
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.open_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        
        self.statusBar().showMessage("处理完成")
        
        QMessageBox.information(self, "完成", "文档处理完成！")
    
    def processing_error(self, error_message):
        """
        处理错误

        处理后台线程发生错误时的回调，隐藏进度条、
        恢复按钮状态并显示错误消息。

        Args:
            error_message: 错误消息字符串
        """
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.open_btn.setEnabled(True)
        
        QMessageBox.critical(self, "错误", error_message)
    
    def show_details_table(self, results):
        """
        显示详细信息表格

        在表格中显示每个文本段的处理详情，包括原始文本、
        处理后文本、移除的空格数和变更详情。

        Args:
            results: 处理结果列表
        """
        self.details_table.setVisible(True)
        self.details_table.setRowCount(len(results))
        
        for i, result in enumerate(results):
            # 原始文本（截断显示）
            original_text = result['original_text'][:100] + "..." if len(result['original_text']) > 100 else result['original_text']
            self.details_table.setItem(i, 0, QTableWidgetItem(original_text))
            
            # 处理后文本（截断显示）
            cleaned_text = result['cleaned_text'][:100] + "..." if len(result['cleaned_text']) > 100 else result['cleaned_text']
            self.details_table.setItem(i, 1, QTableWidgetItem(cleaned_text))
            
            # 移除空格数
            self.details_table.setItem(i, 2, QTableWidgetItem(str(result['spaces_removed'])))
            
            # 变更详情
            changes_detail = "; ".join([change['description'] for change in result['changes']])
            self.details_table.setItem(i, 3, QTableWidgetItem(changes_detail))
        
        self.details_table.resizeColumnsToContents()
    
    def save_results(self):
        """
        保存处理结果到processed_documents文件夹

        弹出文件保存对话框，默认保存到processed_documents目录，
        文件名为原文件名加_cleaned后缀。保存时保持原文档的所有格式。
        """
        if not self.processing_results or not self.current_file_path:
            return
        
        # 生成默认文件名和保存路径
        base_name = os.path.basename(self.current_file_path)
        name_parts = os.path.splitext(base_name)
        default_name = f"{name_parts[0]}_cleaned{name_parts[1]}"
        
        # 构建processed_documents文件夹的完整路径
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        processed_dir = os.path.join(project_dir, "processed_documents")
        
        # 如果文件夹不存在则创建
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)
        
        # 构建默认保存路径
        default_path = os.path.join(processed_dir, default_name)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存处理后的文档",
            default_path,
            "Word文档 (*.docx);;所有文件 (*)"
        )
        
        if file_path:
            try:
                # 获取清理后的文本
                cleaned_texts = [result['cleaned_text'] for result in self.processing_results]
                
                # 保存文档（保持所有格式不变）
                if self.processor.save_as_new_document(file_path, cleaned_texts):
                    # 显示相对路径，更友好
                    rel_path = os.path.relpath(file_path, project_dir)
                    QMessageBox.information(self, "成功", f"文档已保存到:\n{rel_path}")
                    self.statusBar().showMessage(f"已保存: {os.path.basename(file_path)}")
                else:
                    QMessageBox.critical(self, "错误", "保存文档失败")
                    
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文档时发生错误: {str(e)}")
    



def main():
    """
    主函数

    创建QApplication应用程序实例，设置应用样式，
    初始化并显示主窗口，然后进入事件循环。
    """
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    main_window = MainWindow()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()