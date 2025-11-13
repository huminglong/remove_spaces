"""
日志系统配置

提供统一的日志配置,支持控制台输出和文件记录。
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    配置并返回一个logger实例
    
    Args:
        name: logger名称,通常使用 __name__
        level: 日志级别,默认为INFO
        log_file: 日志文件路径,如果为None则不记录到文件
        console_output: 是否输出到控制台,默认为True
    
    Returns:
        配置好的logger实例
    
    Examples:
        >>> logger = setup_logger(__name__)
        >>> logger.info("这是一条信息日志")
        
        >>> logger = setup_logger(__name__, level=logging.DEBUG, log_file='app.log')
        >>> logger.debug("这是一条调试日志")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台输出handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 文件输出handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    获取已存在的logger或创建新的logger
    
    Args:
        name: logger名称
    
    Returns:
        logger实例
    
    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.info("使用现有logger")
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger
