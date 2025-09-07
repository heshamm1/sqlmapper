"""
Logging configuration for SQLmapper
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
):
    """
    Setup logging configuration
    
    Args:
        level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str): Log file path (optional)
        console_output (bool): Enable console output
    """
    # Create logger
    logger = logging.getLogger('sqlmapper')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    # Prevent duplicate logs
    logger.propagate = False
    
    return logger


def get_logger(name: str = 'sqlmapper') -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


class LogHandler(logging.Handler):
    """
    Custom log handler for GUI output
    """
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        
    def emit(self, record):
        """Emit log record"""
        try:
            msg = self.format(record)
            self.callback(msg)
        except Exception:
            self.handleError(record)


def setup_gui_logging(callback):
    """
    Setup logging for GUI output
    
    Args:
        callback: Callback function for log messages
    """
    logger = get_logger()
    
    # Add GUI handler
    gui_handler = LogHandler(callback)
    gui_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    gui_handler.setFormatter(formatter)
    
    logger.addHandler(gui_handler)
    
    return gui_handler
