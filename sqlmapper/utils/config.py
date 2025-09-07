"""
Configuration management for SQLmapper
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class Config:
    """
    Configuration manager for SQLmapper
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file (str): Path to configuration file
        """
        if config_file is None:
            # Use default config file in user's home directory
            home_dir = Path.home()
            config_dir = home_dir / '.sqlmapper'
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / 'config.json'
            
        self.config_file = Path(config_file)
        self.config_data = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Returns:
            dict: Configuration data
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    return self._restore_qt_objects(config_data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()
            
    def _restore_qt_objects(self, obj):
        """Restore Qt objects from JSON-serialized data"""
        if isinstance(obj, str) and len(obj) > 100:  # Likely a base64 encoded QByteArray
            try:
                from PySide6.QtCore import QByteArray
                return QByteArray.fromBase64(obj.encode('utf-8'))
            except:
                return obj
        elif isinstance(obj, dict):
            return {k: self._restore_qt_objects(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._restore_qt_objects(item) for item in obj]
        else:
            return obj
            
    def save_config(self):
        """Save configuration to file"""
        try:
            # Convert QByteArray to base64 string for JSON serialization
            config_to_save = self._convert_qt_objects(self.config_data)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config: {e}")
            
    def _convert_qt_objects(self, obj):
        """Convert Qt objects to JSON-serializable objects"""
        if hasattr(obj, 'toBase64'):  # QByteArray
            return obj.toBase64().data().decode('utf-8')
        elif isinstance(obj, dict):
            return {k: self._convert_qt_objects(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_qt_objects(item) for item in obj]
        else:
            return obj
            
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration
        
        Returns:
            dict: Default configuration
        """
        return {
            'window_geometry': None,
            'last_target': '',
            'last_profile': 'Quick Scan',
            'sqlmap_path': 'sqlmap',
            'api_url': 'http://127.0.0.1:8775',
            'default_options': {
                'risk_level': 1,
                'level': 1,
                'threads': 1,
                'timeout': 30,
                'retries': 3,
                'batch': True
            },
            'profiles': {
                'Quick Scan': {
                    'risk_level': 1,
                    'level': 1,
                    'threads': 1,
                    'timeout': 30,
                    'techniques': ['B', 'E', 'U', 'T'],
                    'detection': ['banner', 'current_user', 'current_db']
                },
                'Full Scan': {
                    'risk_level': 3,
                    'level': 5,
                    'threads': 3,
                    'timeout': 60,
                    'techniques': ['B', 'E', 'U', 'S', 'T', 'Q'],
                    'detection': ['banner', 'current_user', 'current_db', 'hostname', 'is_dba', 'users', 'passwords', 'privileges', 'roles', 'dbs', 'tables', 'columns', 'schema']
                }
            },
            'scan_history': [],
            'recent_targets': [],
            'settings': {
                'auto_save': True,
                'show_legal_disclaimer': True,
                'log_level': 'INFO',
                'max_history_items': 100
            }
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key (str): Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key (str): Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        # Set the value
        config[keys[-1]] = value
        
        # Auto-save if enabled
        if self.get('settings.auto_save', True):
            self.save_config()
            
    def has(self, key: str) -> bool:
        """
        Check if configuration key exists
        
        Args:
            key (str): Configuration key
            
        Returns:
            bool: True if key exists
        """
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return True
        except (KeyError, TypeError):
            return False
            
    def delete(self, key: str):
        """
        Delete configuration key
        
        Args:
            key (str): Configuration key
        """
        keys = key.split('.')
        config = self.config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                return
            config = config[k]
            
        # Delete the key
        if keys[-1] in config:
            del config[keys[-1]]
            self.save_config()
            
    def add_scan_history(self, scan_data: Dict[str, Any]):
        """
        Add scan to history
        
        Args:
            scan_data (dict): Scan data
        """
        history = self.get('scan_history', [])
        
        # Add timestamp if not present
        if 'timestamp' not in scan_data:
            from datetime import datetime
            scan_data['timestamp'] = datetime.now().isoformat()
            
        # Add to beginning of list
        history.insert(0, scan_data)
        
        # Limit history size
        max_items = self.get('settings.max_history_items', 100)
        if len(history) > max_items:
            history = history[:max_items]
            
        self.set('scan_history', history)
        
    def get_scan_history(self) -> List[Dict[str, Any]]:
        """
        Get scan history
        
        Returns:
            list: List of scan history items
        """
        return self.get('scan_history', [])
        
    def add_recent_target(self, target: str):
        """
        Add target to recent targets list
        
        Args:
            target (str): Target URL or file path
        """
        recent = self.get('recent_targets', [])
        
        # Remove if already exists
        if target in recent:
            recent.remove(target)
            
        # Add to beginning
        recent.insert(0, target)
        
        # Limit to 10 items
        if len(recent) > 10:
            recent = recent[:10]
            
        self.set('recent_targets', recent)
        
    def get_recent_targets(self) -> List[str]:
        """
        Get recent targets
        
        Returns:
            list: List of recent targets
        """
        return self.get('recent_targets', [])
        
    def save_profile(self, name: str, profile_data: Dict[str, Any]):
        """
        Save a custom profile
        
        Args:
            name (str): Profile name
            profile_data (dict): Profile data
        """
        profiles = self.get('profiles', {})
        profiles[name] = profile_data
        self.set('profiles', profiles)
        
    def get_profile(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a profile by name
        
        Args:
            name (str): Profile name
            
        Returns:
            dict: Profile data or None if not found
        """
        profiles = self.get('profiles', {})
        return profiles.get(name)
        
    def get_all_profiles(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all profiles
        
        Returns:
            dict: All profiles
        """
        return self.get('profiles', {})
        
    def delete_profile(self, name: str):
        """
        Delete a profile
        
        Args:
            name (str): Profile name
        """
        profiles = self.get('profiles', {})
        if name in profiles:
            del profiles[name]
            self.set('profiles', profiles)
            
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config_data = self.get_default_config()
        self.save_config()
        
    def export_config(self, file_path: str):
        """
        Export configuration to file
        
        Args:
            file_path (str): Export file path
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error exporting config: {e}")
            
    def import_config(self, file_path: str):
        """
        Import configuration from file
        
        Args:
            file_path (str): Import file path
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
                
            # Merge with existing config
            self.config_data.update(imported_data)
            self.save_config()
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error importing config: {e}")
            raise
