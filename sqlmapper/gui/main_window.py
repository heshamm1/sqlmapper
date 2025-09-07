"""
Main window for SQLmapper application
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QTabWidget, QPushButton, QLabel, 
    QTextEdit, QGroupBox, QLineEdit, QComboBox,
    QStatusBar, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QIcon

from sqlmapper.gui.components.log_panel import LogPanel
from sqlmapper.gui.components.target_input import TargetInput
from sqlmapper.gui.components.options_panel import OptionsPanel
from sqlmapper.gui.components.results_panel import ResultsPanel
from sqlmapper.gui.components.profiles_panel import ProfilesPanel
from sqlmapper.core.command_builder import CommandBuilder
from sqlmapper.core.subprocess_runner import SubprocessRunner
from sqlmapper.utils.config import Config


class MainWindow(QMainWindow):
    """
    Main application window
    """
    
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.command_builder = CommandBuilder()
        self.subprocess_runner = None
        
        self.init_ui()
        self.setup_connections()
        self.load_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("SQLmapper - Desktop GUI for sqlmap")
        self.setMinimumSize(1200, 800)
        
        # Set application icon
        self.set_application_icon()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left sidebar (Profiles and History)
        left_sidebar = self.create_left_sidebar()
        splitter.addWidget(left_sidebar)
        
        # Center area (Target input, Options, Console)
        center_area = self.create_center_area()
        splitter.addWidget(center_area)
        
        # Right sidebar (Results)
        right_sidebar = self.create_right_sidebar()
        splitter.addWidget(right_sidebar)
        
        # Set splitter proportions (left, center, right) - give more space to center for console
        splitter.setSizes([250, 800, 350])
        
        # Create status bar
        self.create_status_bar()
        
        # Legal disclaimer
        self.show_legal_disclaimer()
        
    def set_application_icon(self):
        """Set the application icon"""
        try:
            from PySide6.QtGui import QIcon, QPixmap
            from PySide6.QtCore import Qt
            from pathlib import Path
            
            # Try to load PNG icon
            logo_path = Path(__file__).parent.parent / "logo.png"
            if logo_path.exists():
                # Load PNG image directly
                pixmap = QPixmap(str(logo_path))
                
                # Scale to appropriate size if needed
                if pixmap.width() > 64 or pixmap.height() > 64:
                    pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                # Set icon
                icon = QIcon(pixmap)
                self.setWindowIcon(icon)
                print("✓ Window icon loaded successfully")
            else:
                print(f"Logo file not found: {logo_path}")
                
        except Exception as e:
            # If icon loading fails, continue without icon
            print(f"Could not load application icon: {e}")
        
    def create_left_sidebar(self):
        """Create the left sidebar with profiles and history"""
        sidebar = QWidget()
        layout = QVBoxLayout(sidebar)
        
        # Profiles panel
        self.profiles_panel = ProfilesPanel()
        layout.addWidget(self.profiles_panel)
        
        # History panel (placeholder)
        history_group = QGroupBox("Scan History")
        history_layout = QVBoxLayout(history_group)
        
        self.history_list = QTextEdit()
        self.history_list.setMaximumHeight(200)
        self.history_list.setReadOnly(True)
        history_layout.addWidget(self.history_list)
        
        layout.addWidget(history_group)
        layout.addStretch()
        
        return sidebar
        
    def create_center_area(self):
        """Create the center area with target input, options, and console"""
        center = QWidget()
        layout = QVBoxLayout(center)
        
        # Target input
        self.target_input = TargetInput()
        layout.addWidget(self.target_input)
        
        # Options tabs
        self.options_panel = OptionsPanel()
        layout.addWidget(self.options_panel)
        
        # Console log panel
        self.log_panel = LogPanel()
        layout.addWidget(self.log_panel)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Scan")
        self.start_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        
        self.stop_button = QPushButton("Stop Scan")
        self.stop_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; }")
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        return center
        
    def create_right_sidebar(self):
        """Create the right sidebar with results"""
        sidebar = QWidget()
        layout = QVBoxLayout(sidebar)
        
        self.results_panel = ResultsPanel()
        layout.addWidget(self.results_panel)
        
        return sidebar
        
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)
        
        # Profile selection
        self.profiles_panel.profile_selected.connect(self.on_profile_selected)
        
    def load_settings(self):
        """Load application settings"""
        # Load window geometry
        geometry = self.config.get('window_geometry')
        if geometry:
            # Convert base64 string back to QByteArray if needed
            if isinstance(geometry, str):
                from PySide6.QtCore import QByteArray
                geometry = QByteArray.fromBase64(geometry.encode('utf-8'))
            self.restoreGeometry(geometry)
            
    def save_settings(self):
        """Save application settings"""
        self.config.set('window_geometry', self.saveGeometry())
        
    def show_legal_disclaimer(self):
        """Show legal disclaimer dialog"""
        disclaimer = QMessageBox()
        disclaimer.setWindowTitle("Legal Disclaimer")
        disclaimer.setText(
            "SQLmapper is a tool for authorized security testing only.\n\n"
            "By using this software, you agree to:\n"
            "• Only test systems you own or have explicit permission to test\n"
            "• Comply with all applicable laws and regulations\n"
            "• Use the tool responsibly and ethically\n\n"
            "The developers are not responsible for any misuse of this tool."
        )
        disclaimer.setIcon(QMessageBox.Warning)
        disclaimer.exec()
        
    def on_profile_selected(self, profile):
        """Handle profile selection"""
        # Update options panel with profile settings
        self.options_panel.load_profile(profile)
        
    def start_scan(self):
        """Start a new scan"""
        try:
            # Get target information
            target = self.target_input.get_target_info()
            if not target.get('url') and not target.get('request_file'):
                QMessageBox.warning(self, "Error", "Please specify a target URL or request file.")
                return
                
            # Get options
            options = self.options_panel.get_options()
            
            # Build command
            command = self.command_builder.build_command(target, options)
            
            # Start subprocess runner
            self.subprocess_runner = SubprocessRunner(command)
            self.subprocess_runner.output_received.connect(self.log_panel.append_output)
            self.subprocess_runner.scan_completed.connect(self.on_scan_completed)
            self.subprocess_runner.scan_failed.connect(self.on_scan_failed)
            
            # Update UI
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.status_label.setText("Scanning...")
            
            # Start scan
            self.subprocess_runner.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start scan: {str(e)}")
            
    def stop_scan(self):
        """Stop the current scan"""
        try:
            if self.subprocess_runner and self.subprocess_runner.isRunning():
                self.subprocess_runner.stop()
                self.log_panel.append_output("Scan stopped by user")
                
                # Update UI immediately
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.progress_bar.setVisible(False)
                self.status_label.setText("Scan stopped")
            else:
                self.log_panel.append_output("No active scan to stop")
        except Exception as e:
            self.log_panel.append_output(f"Error stopping scan: {str(e)}")
            # Still update UI even if there's an error
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.progress_bar.setVisible(False)
            self.status_label.setText("Error stopping scan")
            
    def on_scan_completed(self, result):
        """Handle scan completion"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Scan completed")
        
        # Update results panel
        self.results_panel.update_results(result)
        
        # Add to history
        self.add_to_history(result)
        
    def on_scan_failed(self, error):
        """Handle scan failure"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Scan failed")
        
        QMessageBox.critical(self, "Scan Failed", f"Scan failed with error: {str(error)}")
        
    def add_to_history(self, result):
        """Add scan result to history"""
        timestamp = result.get('timestamp', 'Unknown')
        target = result.get('target', 'Unknown')
        status = result.get('status', 'Unknown')
        
        history_entry = f"[{timestamp}] {target} - {status}\n"
        self.history_list.append(history_entry)
        
    def closeEvent(self, event):
        """Handle application close event"""
        self.save_settings()
        
        # Stop any running scans
        if self.subprocess_runner:
            self.subprocess_runner.stop()
            
        event.accept()
