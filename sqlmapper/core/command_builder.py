"""
Command builder for constructing sqlmap command line arguments
"""

import shlex
from typing import Dict, List, Any


class CommandBuilder:
    """
    Builds sqlmap command line arguments from user input
    """
    
    def __init__(self):
        """Initialize the command builder"""
        self.sqlmap_path = self.find_sqlmap()
        
    def find_sqlmap(self) -> str:
        """
        Find sqlmap executable path
        
        Returns:
            str: Path to sqlmap executable
        """
        import shutil
        import sys
        import os
        
        # Check if we're running from PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # Running from executable - sqlmap should be in parent directory
            # The executable is in H:\sqlmap\sqlmapper\dist\SQLmapper.exe
            # So sqlmap.py should be in H:\sqlmap\sqlmap.py
            current_dir = os.path.dirname(sys.executable)
            # Go up to sqlmap directory
            sqlmap_dir = os.path.dirname(os.path.dirname(current_dir))
            sqlmap_path = os.path.join(sqlmap_dir, 'sqlmap.py')
            if os.path.exists(sqlmap_path):
                return sqlmap_path
        
        # Try to find sqlmap in PATH
        sqlmap_path = shutil.which('sqlmap')
        if sqlmap_path:
            return sqlmap_path
            
        # Try common locations
        common_paths = [
            'sqlmap.py',
            './sqlmap.py',
            '../sqlmap.py',
            'sqlmap/sqlmap.py'
        ]
        
        for path in common_paths:
            if self._is_executable(path):
                return path
                
        # Default fallback
        return 'sqlmap'
        
    def _is_executable(self, path: str) -> bool:
        """
        Check if a path is executable
        
        Args:
            path (str): Path to check
            
        Returns:
            bool: True if executable
        """
        import os
        if os.path.isfile(path):
            # For Python files, just check if file exists
            if path.endswith('.py'):
                return True
            # For other files, check if executable
            return os.access(path, os.X_OK)
        return False
        
    def build_command(self, target: Dict[str, Any], options: Dict[str, Any]) -> List[str]:
        """
        Build sqlmap command from target and options
        
        Args:
            target (dict): Target information
            options (dict): Scan options
            
        Returns:
            list: Command arguments
        """
        import sys
        
        # Check if sqlmap_path is a Python script
        if self.sqlmap_path.endswith('.py'):
            # When running from PyInstaller bundle, use the bundled Python
            if getattr(sys, 'frozen', False):
                # Use the same Python executable that's running this app
                cmd = [sys.executable, self.sqlmap_path]
            else:
                cmd = ['python', self.sqlmap_path]
        else:
            cmd = [self.sqlmap_path]
        
        # Add target
        cmd.extend(self._build_target_args(target))
        
        # Add options
        cmd.extend(self._build_option_args(options))
        
        return cmd
        
    def _build_target_args(self, target: Dict[str, Any]) -> List[str]:
        """
        Build target-related arguments
        
        Args:
            target (dict): Target information
            
        Returns:
            list: Target arguments
        """
        args = []
        
        # URL target
        if 'url' in target:
            args.extend(['-u', target['url']])
            
        # Request file
        if 'request_file' in target:
            args.extend(['-r', target['request_file']])
            
        # POST data
        if 'data' in target:
            args.extend(['--data', target['data']])
            
        # Cookies
        if 'cookies' in target:
            args.extend(['--cookie', target['cookies']])
            
        # Headers
        if 'headers' in target:
            args.extend(['--headers', target['headers']])
            
        # Random user agent
        if target.get('random_user_agent'):
            args.append('--random-agent')
            
        return args
        
    def _build_option_args(self, options: Dict[str, Any]) -> List[str]:
        """
        Build option-related arguments
        
        Args:
            options (dict): Scan options
            
        Returns:
            list: Option arguments
        """
        args = []
        
        # Risk level
        if 'risk_level' in options:
            args.extend(['--risk', str(options['risk_level'])])
            
        # Level
        if 'level' in options:
            args.extend(['--level', str(options['level'])])
            
        # Threads
        if 'threads' in options:
            args.extend(['--threads', str(options['threads'])])
            
        # Timeout
        if 'timeout' in options:
            args.extend(['--timeout', str(options['timeout'])])
            
        # Retries
        if 'retries' in options:
            args.extend(['--retries', str(options['retries'])])
            
        # Techniques
        if 'techniques' in options and options['techniques']:
            techniques = ''.join(options['techniques'])
            args.extend(['--technique', techniques])
            
        # DBMS
        if 'dbms' in options:
            args.extend(['--dbms', options['dbms']])
            
        # Detection options
        if 'detection' in options:
            detection_map = {
                'banner': '--banner',
                'current_user': '--current-user',
                'current_db': '--current-db',
                'hostname': '--hostname',
                'is_dba': '--is-dba',
                'users': '--users',
                'passwords': '--passwords',
                'privileges': '--privileges',
                'roles': '--roles',
                'dbs': '--dbs',
                'tables': '--tables',
                'columns': '--columns',
                'schema': '--schema'
            }
            
            for detection in options['detection']:
                if detection in detection_map:
                    args.append(detection_map[detection])
                
        # Proxy
        if 'proxy' in options:
            args.extend(['--proxy', options['proxy']])
            
        # Tor
        if options.get('tor'):
            args.append('--tor')
            if 'tor_port' in options:
                args.extend(['--tor-port', str(options['tor_port'])])
                
        # Delay
        if 'delay' in options and options['delay'] > 0:
            args.extend(['--delay', str(options['delay'])])
            
        # Skip options
        if options.get('skip_url_encode'):
            args.append('--skip-url-encode')
            
        if options.get('skip_static'):
            args.append('--skip-static')
            
        # Tamper scripts
        if 'tamper' in options:
            args.extend(['--tamper', options['tamper']])
            
        # OS
        if 'os' in options:
            args.extend(['--os', options['os']])
            
        # Batch mode
        if options.get('batch'):
            args.append('--batch')
            
        # Skip WAF detection (valid sqlmap option)
        if options.get('skip_waf'):
            args.append('--skip-waf')
            
        # Fresh queries
        if options.get('fresh_queries'):
            args.append('--fresh-queries')
            
        # Always add batch mode for non-interactive operation
        if not any('--batch' in arg for arg in args):
            args.append('--batch')
            
        # Custom arguments
        if 'custom_args' in options:
            custom_args = options['custom_args'].strip()
            if custom_args:
                # Split by spaces but preserve quoted arguments
                import shlex
                try:
                    custom_args_list = shlex.split(custom_args)
                    args.extend(custom_args_list)
                except ValueError:
                    # If shlex fails, fall back to simple split
                    args.extend(custom_args.split())
            
        return args
        
    def get_command_string(self, target: Dict[str, Any], options: Dict[str, Any]) -> str:
        """
        Get command as a string for display
        
        Args:
            target (dict): Target information
            options (dict): Scan options
            
        Returns:
            str: Command string
        """
        cmd = self.build_command(target, options)
        return ' '.join(shlex.quote(arg) for arg in cmd)
        
    def validate_target(self, target: Dict[str, Any]) -> List[str]:
        """
        Validate target information
        
        Args:
            target (dict): Target information
            
        Returns:
            list: List of validation errors
        """
        errors = []
        
        # Check if at least one target is specified
        if not target.get('url') and not target.get('request_file'):
            errors.append("Either URL or request file must be specified")
            
        # Validate URL format
        if 'url' in target:
            url = target['url']
            if not url.startswith(('http://', 'https://')):
                errors.append("URL must start with http:// or https://")
                
        # Validate request file
        if 'request_file' in target:
            import os
            if not os.path.isfile(target['request_file']):
                errors.append("Request file does not exist")
                
        return errors
        
    def validate_options(self, options: Dict[str, Any]) -> List[str]:
        """
        Validate options
        
        Args:
            options (dict): Scan options
            
        Returns:
            list: List of validation errors
        """
        errors = []
        
        # Validate risk level
        if 'risk_level' in options:
            risk = options['risk_level']
            if not isinstance(risk, int) or risk < 1 or risk > 3:
                errors.append("Risk level must be between 1 and 3")
                
        # Validate level
        if 'level' in options:
            level = options['level']
            if not isinstance(level, int) or level < 1 or level > 5:
                errors.append("Level must be between 1 and 5")
                
        # Validate threads
        if 'threads' in options:
            threads = options['threads']
            if not isinstance(threads, int) or threads < 1 or threads > 10:
                errors.append("Threads must be between 1 and 10")
                
        # Validate timeout
        if 'timeout' in options:
            timeout = options['timeout']
            if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
                errors.append("Timeout must be between 1 and 300 seconds")
                
        # Validate techniques
        if 'techniques' in options:
            techniques = options['techniques']
            valid_techniques = ['B', 'E', 'U', 'S', 'T', 'Q']
            for technique in techniques:
                if technique not in valid_techniques:
                    errors.append(f"Invalid technique: {technique}")
                    
        return errors
