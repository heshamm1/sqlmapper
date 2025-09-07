"""
Options panel component
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QSpinBox, QComboBox, QLineEdit, QCheckBox,
    QTabWidget, QLabel, QSlider
)
from PySide6.QtCore import Qt, Signal


class OptionsPanel(QGroupBox):
    """
    Panel for configuring sqlmap options
    """
    
    profile_selected = Signal(dict)
    
    def __init__(self):
        super().__init__("Scan Options")
        self.init_ui()
        self.setup_default_profiles()
        
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different option categories
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # General tab
        self.general_tab = self.create_general_tab()
        self.tab_widget.addTab(self.general_tab, "General")
        
        # Injection tab
        self.injection_tab = self.create_injection_tab()
        self.tab_widget.addTab(self.injection_tab, "Injection")
        
        # Detection tab
        self.detection_tab = self.create_detection_tab()
        self.tab_widget.addTab(self.detection_tab, "Detection")
        
        # Optimization tab
        self.optimization_tab = self.create_optimization_tab()
        self.tab_widget.addTab(self.optimization_tab, "Optimization")
        
        # Advanced tab
        self.advanced_tab = self.create_advanced_tab()
        self.tab_widget.addTab(self.advanced_tab, "Advanced")
        
    def create_general_tab(self):
        """Create the general options tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Risk level
        risk_layout = QHBoxLayout()
        risk_layout.addWidget(QLabel("Risk Level:"))
        self.risk_level = QSpinBox()
        self.risk_level.setRange(1, 3)
        self.risk_level.setValue(1)
        self.risk_level.setToolTip("Risk level (1-3): Higher values test more dangerous payloads")
        risk_layout.addWidget(self.risk_level)
        risk_layout.addStretch()
        layout.addLayout(risk_layout)
        
        # Level
        level_layout = QHBoxLayout()
        level_layout.addWidget(QLabel("Level:"))
        self.level = QSpinBox()
        self.level.setRange(1, 5)
        self.level.setValue(1)
        self.level.setToolTip("Level (1-5): Higher values perform more extensive tests")
        level_layout.addWidget(self.level)
        level_layout.addStretch()
        layout.addLayout(level_layout)
        
        # Threads
        threads_layout = QHBoxLayout()
        threads_layout.addWidget(QLabel("Threads:"))
        self.threads = QSpinBox()
        self.threads.setRange(1, 10)
        self.threads.setValue(1)
        self.threads.setToolTip("Number of concurrent HTTP requests")
        threads_layout.addWidget(self.threads)
        threads_layout.addStretch()
        layout.addLayout(threads_layout)
        
        # Timeout
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Timeout:"))
        self.timeout = QSpinBox()
        self.timeout.setRange(1, 300)
        self.timeout.setValue(30)
        self.timeout.setSuffix(" seconds")
        self.timeout.setToolTip("HTTP request timeout")
        timeout_layout.addWidget(self.timeout)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)
        
        # Retries
        retries_layout = QHBoxLayout()
        retries_layout.addWidget(QLabel("Retries:"))
        self.retries = QSpinBox()
        self.retries.setRange(0, 10)
        self.retries.setValue(3)
        self.retries.setToolTip("Number of retries for failed requests")
        retries_layout.addWidget(self.retries)
        retries_layout.addStretch()
        layout.addLayout(retries_layout)
        
        layout.addStretch()
        return widget
        
    def create_injection_tab(self):
        """Create the injection options tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Techniques
        techniques_group = QGroupBox("Injection Techniques")
        techniques_layout = QVBoxLayout(techniques_group)
        
        self.technique_b = QCheckBox("Boolean-based blind")
        self.technique_b.setChecked(True)
        techniques_layout.addWidget(self.technique_b)
        
        self.technique_e = QCheckBox("Error-based")
        self.technique_e.setChecked(True)
        techniques_layout.addWidget(self.technique_e)
        
        self.technique_u = QCheckBox("Union query-based")
        self.technique_u.setChecked(True)
        techniques_layout.addWidget(self.technique_u)
        
        self.technique_s = QCheckBox("Stacked queries")
        techniques_layout.addWidget(self.technique_s)
        
        self.technique_t = QCheckBox("Time-based blind")
        self.technique_t.setChecked(True)
        techniques_layout.addWidget(self.technique_t)
        
        self.technique_q = QCheckBox("Inline queries")
        techniques_layout.addWidget(self.technique_q)
        
        layout.addWidget(techniques_group)
        
        # DBMS
        dbms_layout = QHBoxLayout()
        dbms_layout.addWidget(QLabel("DBMS:"))
        self.dbms = QComboBox()
        self.dbms.addItems(["Auto-detect", "MySQL", "PostgreSQL", "Oracle", "Microsoft SQL Server", "SQLite", "Firebird", "Sybase", "SAP MaxDB", "DB2", "Informix", "HSQLDB", "H2", "MonetDB", "Derby", "Vertica", "Mckoi", "Presto", "Altibase", "MimerSQL", "CockroachDB"])
        dbms_layout.addWidget(self.dbms)
        dbms_layout.addStretch()
        layout.addLayout(dbms_layout)
        
        layout.addStretch()
        return widget
        
    def create_detection_tab(self):
        """Create the detection options tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Detection options
        self.banner = QCheckBox("Retrieve DBMS banner")
        layout.addWidget(self.banner)
        
        self.current_user = QCheckBox("Retrieve current user")
        layout.addWidget(self.current_user)
        
        self.current_db = QCheckBox("Retrieve current database")
        layout.addWidget(self.current_db)
        
        self.hostname = QCheckBox("Retrieve hostname")
        layout.addWidget(self.hostname)
        
        self.is_dba = QCheckBox("Check if current user is DBA")
        layout.addWidget(self.is_dba)
        
        self.users = QCheckBox("Enumerate DBMS users")
        layout.addWidget(self.users)
        
        self.passwords = QCheckBox("Enumerate DBMS users password hashes")
        layout.addWidget(self.passwords)
        
        self.privileges = QCheckBox("Enumerate DBMS users privileges")
        layout.addWidget(self.privileges)
        
        self.roles = QCheckBox("Enumerate DBMS users roles")
        layout.addWidget(self.roles)
        
        self.dbs = QCheckBox("Enumerate databases")
        layout.addWidget(self.dbs)
        
        self.tables = QCheckBox("Enumerate tables")
        layout.addWidget(self.tables)
        
        self.columns = QCheckBox("Enumerate columns")
        layout.addWidget(self.columns)
        
        self.schema = QCheckBox("Enumerate DBMS schema")
        layout.addWidget(self.schema)
        
        layout.addStretch()
        return widget
        
    def create_optimization_tab(self):
        """Create the optimization options tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Proxy
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(QLabel("Proxy:"))
        self.proxy = QLineEdit()
        self.proxy.setPlaceholderText("http://127.0.0.1:8080")
        proxy_layout.addWidget(self.proxy)
        layout.addLayout(proxy_layout)
        
        # Tor
        self.tor = QCheckBox("Use Tor")
        layout.addWidget(self.tor)
        
        # Tor port
        tor_port_layout = QHBoxLayout()
        tor_port_layout.addWidget(QLabel("Tor Port:"))
        self.tor_port = QSpinBox()
        self.tor_port.setRange(1, 65535)
        self.tor_port.setValue(9050)
        tor_port_layout.addWidget(self.tor_port)
        tor_port_layout.addStretch()
        layout.addLayout(tor_port_layout)
        
        # Delay
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Delay:"))
        self.delay = QSpinBox()
        self.delay.setRange(0, 60)
        self.delay.setValue(0)
        self.delay.setSuffix(" seconds")
        delay_layout.addWidget(self.delay)
        delay_layout.addStretch()
        layout.addLayout(delay_layout)
        
        # Skip URL encoding
        self.skip_url_encode = QCheckBox("Skip URL encoding")
        layout.addWidget(self.skip_url_encode)
        
        # Skip static
        self.skip_static = QCheckBox("Skip static content")
        layout.addWidget(self.skip_static)
        
        layout.addStretch()
        return widget
        
    def create_advanced_tab(self):
        """Create the advanced options tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tamper scripts
        tamper_layout = QHBoxLayout()
        tamper_layout.addWidget(QLabel("Tamper Scripts:"))
        self.tamper = QLineEdit()
        self.tamper.setPlaceholderText("space2comment,charencode")
        tamper_layout.addWidget(self.tamper)
        layout.addLayout(tamper_layout)
        
        # OS
        os_layout = QHBoxLayout()
        os_layout.addWidget(QLabel("OS:"))
        self.os = QComboBox()
        self.os.addItems(["Auto-detect", "Windows", "Linux"])
        os_layout.addWidget(self.os)
        os_layout.addStretch()
        layout.addLayout(os_layout)
        
        # Batch mode
        self.batch = QCheckBox("Batch mode (non-interactive)")
        self.batch.setChecked(True)
        layout.addWidget(self.batch)
        
        # No check
        self.no_check = QCheckBox("Skip connection check")
        layout.addWidget(self.no_check)
        
        # Fresh queries
        self.fresh_queries = QCheckBox("Ignore stored results")
        layout.addWidget(self.fresh_queries)
        
        # Custom arguments
        layout.addWidget(QLabel("Custom Arguments:"))
        self.custom_args = QLineEdit()
        self.custom_args.setPlaceholderText("e.g., --os-shell --file-read=/etc/passwd --file-write=/tmp/test.txt")
        self.custom_args.setToolTip("Enter additional sqlmap command-line arguments separated by spaces. Examples:\n--os-shell (get OS shell)\n--file-read=/etc/passwd (read file)\n--file-write=/tmp/test.txt (write file)\n--sql-query='SELECT * FROM users' (custom SQL)")
        layout.addWidget(self.custom_args)
        
        layout.addStretch()
        return widget
        
    def setup_default_profiles(self):
        """Setup default scan profiles"""
        self.profiles = {
            "Quick Scan": {
                "risk_level": 1,
                "level": 1,
                "threads": 1,
                "timeout": 30,
                "techniques": ["B", "E", "U", "T"],
                "detection": ["banner", "current_user", "current_db"]
            },
            "Full Scan": {
                "risk_level": 3,
                "level": 5,
                "threads": 3,
                "timeout": 60,
                "techniques": ["B", "E", "U", "S", "T", "Q"],
                "detection": ["banner", "current_user", "current_db", "hostname", "is_dba", "users", "passwords", "privileges", "roles", "dbs", "tables", "columns", "schema"]
            },
            "Custom": {}
        }
        
    def load_profile(self, profile_name):
        """Load a scan profile"""
        if profile_name in self.profiles:
            profile = self.profiles[profile_name]
            
            # Apply profile settings
            if "risk_level" in profile:
                self.risk_level.setValue(profile["risk_level"])
            if "level" in profile:
                self.level.setValue(profile["level"])
            if "threads" in profile:
                self.threads.setValue(profile["threads"])
            if "timeout" in profile:
                self.timeout.setValue(profile["timeout"])
                
            # Apply techniques
            if "techniques" in profile:
                self.technique_b.setChecked("B" in profile["techniques"])
                self.technique_e.setChecked("E" in profile["techniques"])
                self.technique_u.setChecked("U" in profile["techniques"])
                self.technique_s.setChecked("S" in profile["techniques"])
                self.technique_t.setChecked("T" in profile["techniques"])
                self.technique_q.setChecked("Q" in profile["techniques"])
                
            # Apply detection options
            if "detection" in profile:
                detection_opts = profile["detection"]
                self.banner.setChecked("banner" in detection_opts)
                self.current_user.setChecked("current_user" in detection_opts)
                self.current_db.setChecked("current_db" in detection_opts)
                self.hostname.setChecked("hostname" in detection_opts)
                self.is_dba.setChecked("is_dba" in detection_opts)
                self.users.setChecked("users" in detection_opts)
                self.passwords.setChecked("passwords" in detection_opts)
                self.privileges.setChecked("privileges" in detection_opts)
                self.roles.setChecked("roles" in detection_opts)
                self.dbs.setChecked("dbs" in detection_opts)
                self.tables.setChecked("tables" in detection_opts)
                self.columns.setChecked("columns" in detection_opts)
                self.schema.setChecked("schema" in detection_opts)
                
    def get_options(self):
        """
        Get all selected options
        
        Returns:
            dict: Options dictionary
        """
        options = {}
        
        # General options
        options['risk_level'] = self.risk_level.value()
        options['level'] = self.level.value()
        options['threads'] = self.threads.value()
        options['timeout'] = self.timeout.value()
        options['retries'] = self.retries.value()
        
        # Injection techniques
        techniques = []
        if self.technique_b.isChecked():
            techniques.append('B')
        if self.technique_e.isChecked():
            techniques.append('E')
        if self.technique_u.isChecked():
            techniques.append('U')
        if self.technique_s.isChecked():
            techniques.append('S')
        if self.technique_t.isChecked():
            techniques.append('T')
        if self.technique_q.isChecked():
            techniques.append('Q')
        options['techniques'] = techniques
        
        # DBMS
        dbms = self.dbms.currentText()
        if dbms != "Auto-detect":
            options['dbms'] = dbms.lower()
            
        # Detection options
        detection = []
        if self.banner.isChecked():
            detection.append('banner')
        if self.current_user.isChecked():
            detection.append('current_user')
        if self.current_db.isChecked():
            detection.append('current_db')
        if self.hostname.isChecked():
            detection.append('hostname')
        if self.is_dba.isChecked():
            detection.append('is_dba')
        if self.users.isChecked():
            detection.append('users')
        if self.passwords.isChecked():
            detection.append('passwords')
        if self.privileges.isChecked():
            detection.append('privileges')
        if self.roles.isChecked():
            detection.append('roles')
        if self.dbs.isChecked():
            detection.append('dbs')
        if self.tables.isChecked():
            detection.append('tables')
        if self.columns.isChecked():
            detection.append('columns')
        if self.schema.isChecked():
            detection.append('schema')
        options['detection'] = detection
        
        # Optimization options
        proxy = self.proxy.text().strip()
        if proxy:
            options['proxy'] = proxy
            
        if self.tor.isChecked():
            options['tor'] = True
            options['tor_port'] = self.tor_port.value()
            
        options['delay'] = self.delay.value()
        options['skip_url_encode'] = self.skip_url_encode.isChecked()
        options['skip_static'] = self.skip_static.isChecked()
        
        # Advanced options
        tamper = self.tamper.text().strip()
        if tamper:
            options['tamper'] = tamper
            
        os = self.os.currentText()
        if os != "Auto-detect":
            options['os'] = os.lower()
            
        options['batch'] = self.batch.isChecked()
        options['no_check'] = self.no_check.isChecked()
        options['fresh_queries'] = self.fresh_queries.isChecked()
        
        # Custom arguments
        custom_args = self.custom_args.text().strip()
        if custom_args:
            options['custom_args'] = custom_args
        
        return options
