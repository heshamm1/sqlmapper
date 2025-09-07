"""
Results panel component
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QTextEdit, QLabel, QTreeWidget, QTreeWidgetItem,
    QTabWidget, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ResultsPanel(QGroupBox):
    """
    Panel for displaying scan results
    """
    
    def __init__(self):
        super().__init__("Scan Results")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different result views
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Summary tab
        self.summary_tab = self.create_summary_tab()
        self.tab_widget.addTab(self.summary_tab, "Summary")
        
        # Vulnerabilities tab
        self.vulnerabilities_tab = self.create_vulnerabilities_tab()
        self.tab_widget.addTab(self.vulnerabilities_tab, "Vulnerabilities")
        
        # Database info tab
        self.database_tab = self.create_database_tab()
        self.tab_widget.addTab(self.database_tab, "Database")
        
        # Raw output tab
        self.raw_tab = self.create_raw_tab()
        self.tab_widget.addTab(self.raw_tab, "Raw Output")
        
    def create_summary_tab(self):
        """Create the summary tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Summary text
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(200)
        layout.addWidget(self.summary_text)
        
        # Status labels
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Not scanned")
        self.status_label.setStyleSheet("QLabel { font-weight: bold; color: #666; }")
        status_layout.addWidget(self.status_label)
        
        self.target_label = QLabel("Target: None")
        status_layout.addWidget(self.target_label)
        
        self.dbms_label = QLabel("DBMS: Unknown")
        status_layout.addWidget(self.dbms_label)
        
        self.vulnerable_label = QLabel("Vulnerable: No")
        self.vulnerable_label.setStyleSheet("QLabel { color: #f44336; }")
        status_layout.addWidget(self.vulnerable_label)
        
        layout.addLayout(status_layout)
        layout.addStretch()
        
        return widget
        
    def create_vulnerabilities_tab(self):
        """Create the vulnerabilities tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Vulnerabilities table
        self.vulnerabilities_table = QTableWidget()
        self.vulnerabilities_table.setColumnCount(4)
        self.vulnerabilities_table.setHorizontalHeaderLabels(["Parameter", "Type", "Title", "Payload"])
        
        # Set table properties
        self.vulnerabilities_table.setAlternatingRowColors(True)
        self.vulnerabilities_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.vulnerabilities_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.vulnerabilities_table)
        
        return widget
        
    def create_database_tab(self):
        """Create the database information tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Database info tree
        self.database_tree = QTreeWidget()
        self.database_tree.setHeaderLabel("Database Information")
        layout.addWidget(self.database_tree)
        
        return widget
        
    def create_raw_tab(self):
        """Create the raw output tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Raw output text
        self.raw_output = QTextEdit()
        self.raw_output.setReadOnly(True)
        self.raw_output.setFont(QFont("Consolas", 9))
        
        # Set dark theme colors
        self.raw_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
            }
        """)
        
        layout.addWidget(self.raw_output)
        
        return widget
        
    def update_results(self, result):
        """
        Update the results panel with scan results
        
        Args:
            result (dict): Scan result data
        """
        # Update summary
        self.update_summary(result)
        
        # Update vulnerabilities
        self.update_vulnerabilities(result)
        
        # Update database info
        self.update_database_info(result)
        
        # Update raw output
        self.update_raw_output(result)
        
    def update_summary(self, result):
        """Update the summary tab"""
        # Update status labels
        status = result.get('status', 'Unknown')
        self.status_label.setText(f"Status: {status}")
        
        target = result.get('target', 'Unknown')
        self.target_label.setText(f"Target: {target}")
        
        dbms = result.get('dbms', 'Unknown')
        self.dbms_label.setText(f"DBMS: {dbms}")
        
        vulnerable = result.get('vulnerable', False)
        if vulnerable:
            self.vulnerable_label.setText("Vulnerable: Yes")
            self.vulnerable_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; }")
        else:
            self.vulnerable_label.setText("Vulnerable: No")
            self.vulnerable_label.setStyleSheet("QLabel { color: #f44336; }")
            
        # Update summary text
        summary_text = result.get('summary', 'No summary available')
        self.summary_text.setPlainText(summary_text)
        
    def update_vulnerabilities(self, result):
        """Update the vulnerabilities tab"""
        vulnerabilities = result.get('vulnerabilities', [])
        
        # Clear existing data
        self.vulnerabilities_table.setRowCount(len(vulnerabilities))
        
        # Populate table
        for row, vuln in enumerate(vulnerabilities):
            self.vulnerabilities_table.setItem(row, 0, QTableWidgetItem(vuln.get('parameter', '')))
            self.vulnerabilities_table.setItem(row, 1, QTableWidgetItem(vuln.get('type', '')))
            self.vulnerabilities_table.setItem(row, 2, QTableWidgetItem(vuln.get('title', '')))
            self.vulnerabilities_table.setItem(row, 3, QTableWidgetItem(vuln.get('payload', '')))
            
        # Resize columns
        self.vulnerabilities_table.resizeColumnsToContents()
        
    def update_database_info(self, result):
        """Update the database information tab"""
        # Clear existing data
        self.database_tree.clear()
        
        # Add database information
        db_info = result.get('database_info', {})
        
        if db_info:
            # DBMS info
            dbms_item = QTreeWidgetItem(self.database_tree, ["DBMS Information"])
            
            for key, value in db_info.items():
                if key == 'databases' and isinstance(value, dict):
                    # Database structure
                    db_item = QTreeWidgetItem(dbms_item, ["Databases"])
                    for db_name, db_data in value.items():
                        db_name_item = QTreeWidgetItem(db_item, [db_name])
                        if isinstance(db_data, dict) and 'tables' in db_data:
                            tables_item = QTreeWidgetItem(db_name_item, ["Tables"])
                            for table_name in db_data['tables']:
                                QTreeWidgetItem(tables_item, [table_name])
                elif isinstance(value, dict):
                    # Nested information
                    nested_item = QTreeWidgetItem(dbms_item, [key])
                    for nested_key, nested_value in value.items():
                        QTreeWidgetItem(nested_item, [nested_key, str(nested_value)])
                else:
                    # Simple key-value pair
                    QTreeWidgetItem(dbms_item, [key, str(value)])
                    
            # Expand the tree
            self.database_tree.expandAll()
        else:
            # Show message if no database info
            no_info_item = QTreeWidgetItem(self.database_tree, ["No database information available"])
            no_info_item.setDisabled(True)
            
    def update_raw_output(self, result):
        """Update the raw output tab"""
        raw_output = result.get('raw_output', '')
        self.raw_output.setPlainText(raw_output)
        
    def clear_results(self):
        """Clear all results"""
        self.status_label.setText("Status: Not scanned")
        self.target_label.setText("Target: None")
        self.dbms_label.setText("DBMS: Unknown")
        self.vulnerable_label.setText("Vulnerable: No")
        self.vulnerable_label.setStyleSheet("QLabel { color: #f44336; }")
        
        self.summary_text.clear()
        self.vulnerabilities_table.setRowCount(0)
        self.database_tree.clear()
        self.raw_output.clear()
