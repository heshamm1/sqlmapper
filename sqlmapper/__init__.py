"""
SQLmapper - Desktop GUI for sqlmap

A professional desktop GUI application for sqlmap, similar to how Zenmap is a GUI for nmap.
Provides a clean, beginner-friendly interface to run and manage sqlmap scans.

Author: SQLmapper Team
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "SQLmapper Team"
__email__ = "contact@sqlmapper.dev"
__license__ = "MIT"

# Import main components for easy access
from .gui.main_window import MainWindow
from .core.command_builder import CommandBuilder
from .core.subprocess_runner import SubprocessRunner
from .utils.config import Config
from .utils.logger import setup_logging, get_logger

__all__ = [
    "MainWindow",
    "CommandBuilder", 
    "SubprocessRunner",
    "Config",
    "setup_logging",
    "get_logger",
]
