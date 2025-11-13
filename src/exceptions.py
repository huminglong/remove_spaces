"""
自定义异常类层次结构

定义了文档处理过程中可能出现的各种异常类型,
便于精确的错误处理和问题追踪。
"""


class DocumentProcessorError(Exception):
    """
    文档处理器基础异常
    
    所有文档处理相关异常的基类,用于捕获所有文档处理错误。
    """
    pass


class DocumentLoadError(DocumentProcessorError):
    """
    文档加载失败异常
    
    当无法加载文档时抛出,可能的原因包括:
    - 文件不存在
    - 文件格式不正确
    - 文件已损坏
    - 权限不足
    
    Examples:
        >>> try:
        ...     processor.load_document("non_existent.docx")
        ... except DocumentLoadError as e:
        ...     print(f"无法加载文档: {e}")
    """
    pass


class DocumentStructureError(DocumentProcessorError):
    """
    文档结构错误异常
    
    当文档结构无法正确解析时抛出,可能的原因包括:
    - 文档结构损坏
    - 不支持的文档格式
    - 缺少必要的元素
    """
    pass


class TextUpdateError(DocumentProcessorError):
    """
    文本更新失败异常
    
    当更新文档文本时失败时抛出,可能的原因包括:
    - 段落索引超出范围
    - 格式信息丢失
    - 运行时错误
    """
    pass


class DocumentSaveError(DocumentProcessorError):
    """
    文档保存失败异常
    
    当保存文档时失败时抛出,可能的原因包括:
    - 目标路径不存在
    - 磁盘空间不足
    - 权限不足
    - 文件被占用
    """
    pass


class TextCleanerError(Exception):
    """
    文本清理异常基类
    
    所有文本清理相关异常的基类。
    """
    pass


class InvalidTextError(TextCleanerError):
    """
    无效文本异常
    
    当输入文本无效时抛出,例如:
    - 文本为None
    - 文本类型不正确
    """
    pass
