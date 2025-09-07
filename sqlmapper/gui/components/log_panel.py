"""
Console log panel component
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox, 
    QPushButton, QHBoxLayout, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QTextCursor


class LogPanel(QGroupBox):
    """
    Panel for displaying console output from sqlmap
    """
    
    def __init__(self):
        super().__init__("Console Output")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_output)
        
        self.auto_scroll_checkbox = QCheckBox("Auto-scroll")
        self.auto_scroll_checkbox.setChecked(True)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.auto_scroll_checkbox)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Text output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        
        # Set minimum height to make console bigger
        self.output_text.setMinimumHeight(300)
        
        # Set dark theme colors
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                font-size: 10pt;
                line-height: 1.2;
            }
        """)
        
        layout.addWidget(self.output_text)
        
    def append_output(self, text):
        """
        Append text to the output area
        
        Args:
            text (str): Text to append
        """
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format the text with timestamp
        formatted_text = f"[{timestamp}] {text}"
        
        # Append to text area
        self.output_text.append(formatted_text)
        
        # Auto-scroll if enabled
        if self.auto_scroll_checkbox.isChecked():
            cursor = self.output_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.output_text.setTextCursor(cursor)
            
    def clear_output(self):
        """Clear the output area"""
        self.output_text.clear()
        
    def get_output(self):
        """
        Get the current output text
        
        Returns:
            str: Current output text
        """
        return self.output_text.toPlainText()
