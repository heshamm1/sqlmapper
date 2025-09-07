"""
Profiles panel component
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QListWidget, QListWidgetItem,
    QDialog, QLineEdit, QDialogButtonBox,
    QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon


class ProfilesPanel(QGroupBox):
    """
    Panel for managing scan profiles
    """
    
    profile_selected = Signal(str)
    
    def __init__(self):
        super().__init__("Scan Profiles")
        self.init_ui()
        self.load_default_profiles()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        
        # Profiles list
        self.profiles_list = QListWidget()
        self.profiles_list.itemClicked.connect(self.on_profile_selected)
        layout.addWidget(self.profiles_list)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.create_new_profile)
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_profile)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_profile)
        
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
        
    def load_default_profiles(self):
        """Load default scan profiles"""
        default_profiles = [
            "Quick Scan",
            "Full Scan",
            "Custom"
        ]
        
        for profile in default_profiles:
            item = QListWidgetItem(profile)
            self.profiles_list.addItem(item)
            
        # Select first profile by default
        if self.profiles_list.count() > 0:
            self.profiles_list.setCurrentRow(0)
            self.on_profile_selected(self.profiles_list.item(0))
            
    def on_profile_selected(self, item):
        """Handle profile selection"""
        if item:
            profile_name = item.text()
            self.profile_selected.emit(profile_name)
            
    def create_new_profile(self):
        """Create a new profile"""
        dialog = ProfileDialog(self)
        if dialog.exec() == QDialog.Accepted:
            profile_name = dialog.get_profile_name()
            if profile_name and profile_name not in self.get_profile_names():
                # Add to list
                item = QListWidgetItem(profile_name)
                self.profiles_list.addItem(item)
                self.profiles_list.setCurrentItem(item)
                self.on_profile_selected(item)
            else:
                QMessageBox.warning(self, "Error", "Profile name already exists or is invalid.")
                
    def edit_profile(self):
        """Edit the selected profile"""
        current_item = self.profiles_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a profile to edit.")
            return
            
        profile_name = current_item.text()
        
        # Check if it's a default profile
        if profile_name in ["Quick Scan", "Full Scan", "Custom"]:
            QMessageBox.information(self, "Info", "Default profiles cannot be edited.")
            return
            
        # For now, just show a message
        QMessageBox.information(self, "Info", f"Editing profile '{profile_name}' - Feature coming soon!")
        
    def delete_profile(self):
        """Delete the selected profile"""
        current_item = self.profiles_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a profile to delete.")
            return
            
        profile_name = current_item.text()
        
        # Check if it's a default profile
        if profile_name in ["Quick Scan", "Full Scan", "Custom"]:
            QMessageBox.information(self, "Info", "Default profiles cannot be deleted.")
            return
            
        # Confirm deletion
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete the profile '{profile_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.profiles_list.takeItem(self.profiles_list.row(current_item))
            
    def get_profile_names(self):
        """Get list of all profile names"""
        names = []
        for i in range(self.profiles_list.count()):
            names.append(self.profiles_list.item(i).text())
        return names


class ProfileDialog(QDialog):
    """
    Dialog for creating/editing profiles
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Profile")
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        
        # Profile name input
        layout.addWidget(QLabel("Profile Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter profile name...")
        layout.addWidget(self.name_input)
        
        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def get_profile_name(self):
        """Get the profile name"""
        return self.name_input.text().strip()
