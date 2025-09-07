"""
Target input component
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLineEdit, QLabel, QPushButton, QFileDialog,
    QTextEdit, QTabWidget, QCheckBox
)
from PySide6.QtCore import Qt


class TargetInput(QGroupBox):
    """
    Component for inputting target information
    """
    
    def __init__(self):
        super().__init__("Target Input")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different input methods
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # URL tab
        self.url_tab = self.create_url_tab()
        self.tab_widget.addTab(self.url_tab, "URL")
        
        # Request file tab
        self.request_tab = self.create_request_tab()
        self.tab_widget.addTab(self.request_tab, "Request File")
        
        # Custom headers tab
        self.headers_tab = self.create_headers_tab()
        self.tab_widget.addTab(self.headers_tab, "Headers")
        
    def create_url_tab(self):
        """Create the URL input tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Target URL:"))
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("http://example.com/page.php?id=1")
        url_layout.addWidget(self.url_input)
        
        layout.addLayout(url_layout)
        
        # Additional URL options
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("POST data (optional)")
        layout.addWidget(QLabel("POST Data:"))
        layout.addWidget(self.data_input)
        
        self.cookie_input = QLineEdit()
        self.cookie_input.setPlaceholderText("Cookie string (optional)")
        layout.addWidget(QLabel("Cookies:"))
        layout.addWidget(self.cookie_input)
        
        layout.addStretch()
        return widget
        
    def create_request_tab(self):
        """Create the request file input tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Request File:"))
        
        self.request_file_input = QLineEdit()
        self.request_file_input.setPlaceholderText("Select a request file (.txt)")
        file_layout.addWidget(self.request_file_input)
        
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_request_file)
        file_layout.addWidget(self.browse_button)
        
        layout.addLayout(file_layout)
        
        # Request file preview
        layout.addWidget(QLabel("Preview:"))
        self.request_preview = QTextEdit()
        self.request_preview.setMaximumHeight(150)
        self.request_preview.setReadOnly(True)
        layout.addWidget(self.request_preview)
        
        layout.addStretch()
        return widget
        
    def create_headers_tab(self):
        """Create the custom headers tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Headers input
        layout.addWidget(QLabel("Custom Headers (one per line):"))
        self.headers_input = QTextEdit()
        self.headers_input.setMaximumHeight(100)
        self.headers_input.setPlaceholderText("User-Agent: Mozilla/5.0...\nX-Forwarded-For: 127.0.0.1")
        layout.addWidget(self.headers_input)
        
        # Additional options
        self.random_user_agent = QCheckBox("Random User-Agent")
        layout.addWidget(self.random_user_agent)
        
        layout.addStretch()
        return widget
        
    def browse_request_file(self):
        """Browse for request file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Request File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            self.request_file_input.setText(file_path)
            self.preview_request_file(file_path)
            
    def preview_request_file(self, file_path):
        """Preview the contents of a request file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.request_preview.setPlainText(content[:500])  # Show first 500 chars
        except Exception as e:
            self.request_preview.setPlainText(f"Error reading file: {str(e)}")
            
    def get_target_info(self):
        """
        Get target information from the input fields
        
        Returns:
            dict: Target information
        """
        target_info = {}
        
        # Get current tab
        current_tab = self.tab_widget.currentIndex()
        
        if current_tab == 0:  # URL tab
            url = self.url_input.text().strip()
            if url:
                target_info['url'] = url
                
            data = self.data_input.text().strip()
            if data:
                target_info['data'] = data
                
            cookies = self.cookie_input.text().strip()
            if cookies:
                target_info['cookies'] = cookies
                
        elif current_tab == 1:  # Request file tab
            request_file = self.request_file_input.text().strip()
            if request_file:
                target_info['request_file'] = request_file
                
        # Headers (always available)
        headers_text = self.headers_input.toPlainText().strip()
        if headers_text:
            target_info['headers'] = headers_text
            
        # Random user agent
        if self.random_user_agent.isChecked():
            target_info['random_user_agent'] = True
            
        return target_info
