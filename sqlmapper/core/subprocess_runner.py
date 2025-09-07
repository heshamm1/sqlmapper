"""
Subprocess runner for executing sqlmap commands
"""

import subprocess
import threading
import queue
import time
import os
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QThread, Signal, QObject


class SubprocessRunner(QThread):
    """
    Runs sqlmap as a subprocess and streams output
    """
    
    output_received = Signal(str)
    scan_completed = Signal(dict)
    scan_failed = Signal(str)
    
    def __init__(self, command: List[str]):
        super().__init__()
        self.command = command
        self.process = None
        self.running = False
        self.output_queue = queue.Queue()
        self.output_lines = []  # Store all output for parsing
        
    def run(self):
        """Run the subprocess"""
        try:
            self.running = True
            
            # Set up environment for subprocess
            env = None
            import sys
            if getattr(sys, 'frozen', False):
                # When running from PyInstaller bundle, preserve the environment
                env = dict(os.environ)
                # Add the bundle path to PYTHONPATH if needed
                if hasattr(sys, '_MEIPASS'):
                    pythonpath = env.get('PYTHONPATH', '')
                    if pythonpath:
                        env['PYTHONPATH'] = f"{sys._MEIPASS};{pythonpath}"
                    else:
                        env['PYTHONPATH'] = sys._MEIPASS
            
            # Start subprocess
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                env=env
            )
            
            # Stream output
            while self.running and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    line_stripped = line.rstrip()
                    self.output_lines.append(line_stripped)
                    self.output_received.emit(line_stripped)
                    
            # Get remaining output
            if self.process.poll() is None:
                remaining_output = self.process.stdout.read()
                if remaining_output:
                    remaining_lines = remaining_output.split('\n')
                    for line in remaining_lines:
                        if line.strip():
                            self.output_lines.append(line.strip())
                            self.output_received.emit(line.strip())
                    
            # Wait for process to complete
            return_code = self.process.wait()
            
            if return_code == 0:
                # Parse results (simplified)
                result = self._parse_results()
                self.scan_completed.emit(result)
            else:
                self.scan_failed.emit(f"Process exited with code {return_code}")
                
        except Exception as e:
            self.scan_failed.emit(str(e))
        finally:
            self.running = False
            
    def stop(self):
        """Stop the subprocess"""
        self.running = False
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    self.process.kill()
                    self.process.wait(timeout=2)
                except:
                    pass
            except Exception as e:
                print(f"Error stopping process: {e}")
                
    def _parse_results(self) -> Dict[str, Any]:
        """
        Parse sqlmap output to extract results
        
        Returns:
            dict: Parsed results
        """
        result = {
            'status': 'completed',
            'target': 'Unknown',
            'dbms': 'Unknown',
            'vulnerable': False,
            'vulnerabilities': [],
            'database_info': {},
            'summary': 'Scan completed successfully',
            'raw_output': '\n'.join(self.output_lines),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Parse the output lines
        self._parse_sqlmap_output(self.output_lines, result)
        
        return result
    
    def _parse_sqlmap_output(self, lines: List[str], result: Dict[str, Any]):
        """
        Parse sqlmap output lines to extract information
        
        Args:
            lines: List of output lines
            result: Result dictionary to update
        """
        current_section = None
        vulnerabilities = []
        database_info = {}
        target_url = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Extract target URL from various patterns
            if '[*] testing connection to the target URL' in line:
                # Extract URL from line like: [*] testing connection to the target URL: 'http://example.com'
                if "'" in line:
                    start = line.find("'") + 1
                    end = line.rfind("'")
                    if start > 0 and end > start:
                        target_url = line[start:end]
                        result['target'] = target_url
                        
            elif '[*] starting at' in line and '[*] ending at' in line:
                # Extract URL from timing line
                if target_url:
                    result['target'] = target_url
                    
            elif '[INFO] testing URL' in line:
                # Extract URL from testing line
                if "'" in line:
                    start = line.find("'") + 1
                    end = line.rfind("'")
                    if start > 0 and end > start:
                        result['target'] = line[start:end]
                        
            elif '[INFO] testing connection to the target URL' in line:
                # Alternative pattern
                if "'" in line:
                    start = line.find("'") + 1
                    end = line.rfind("'")
                    if start > 0 and end > start:
                        result['target'] = line[start:end]
            
            # Extract DBMS information
            elif '[INFO] the back-end DBMS is' in line:
                # Extract DBMS from line like: [INFO] the back-end DBMS is MySQL
                dbms = line.split('is ')[-1].strip()
                result['dbms'] = dbms
                database_info['dbms'] = dbms
                
            elif '[INFO] banner:' in line:
                # Extract banner information
                banner = line.split('banner: ')[-1].strip()
                database_info['banner'] = banner
                
            # Check for vulnerabilities - multiple patterns
            elif '[CRITICAL] sqlmap identified the following injection point(s):' in line:
                result['vulnerable'] = True
                current_section = 'vulnerability'
                
            elif '[CRITICAL] all tested parameters appear to be not injectable' in line:
                result['vulnerable'] = False
                current_section = 'not_vulnerable'
                
            elif '[INFO] sqlmap identified the following injection point(s):' in line:
                result['vulnerable'] = True
                current_section = 'vulnerability'
                
            elif '[PAYLOAD]' in line and current_section == 'vulnerability':
                # Extract payload information
                if 'Parameter:' in line:
                    param = line.split('Parameter: ')[-1].split()[0]
                    vuln = {
                        'parameter': param,
                        'type': 'Unknown',
                        'title': 'SQL Injection',
                        'payload': line
                    }
                    vulnerabilities.append(vuln)
                    
            elif '[INFO] testing for SQL injection on' in line:
                # Extract parameter being tested
                if 'Parameter:' in line:
                    param = line.split('Parameter: ')[-1].split()[0]
                    # Check if this parameter was found vulnerable
                    result['vulnerable'] = True
                    
            elif '[INFO] testing' in line and 'injection' in line.lower():
                # General injection testing
                if 'Parameter:' in line:
                    param = line.split('Parameter: ')[-1].split()[0]
                    # This indicates testing is happening, vulnerability will be determined later
                    
            # Extract database information
            elif '[INFO] fetching database names' in line:
                current_section = 'databases'
                
            elif '[INFO] fetching tables for database:' in line:
                db_name = line.split('database: ')[-1].strip("'\"")
                if 'databases' not in database_info:
                    database_info['databases'] = {}
                if db_name not in database_info['databases']:
                    database_info['databases'][db_name] = {'tables': []}
                    
            elif '[INFO] fetching columns for table' in line:
                # Extract table name
                if 'table ' in line and 'database' in line:
                    table_info = line.split('table ')[-1]
                    if ' in database' in table_info:
                        table_name = table_info.split(' in database')[0].strip("'\"")
                        db_name = table_info.split('database ')[-1].strip("'\"")
                        if 'databases' not in database_info:
                            database_info['databases'] = {}
                        if db_name not in database_info['databases']:
                            database_info['databases'][db_name] = {'tables': []}
                        if table_name not in database_info['databases'][db_name]['tables']:
                            database_info['databases'][db_name]['tables'].append(table_name)
                            
            # Extract current user
            elif '[INFO] fetching current user' in line:
                current_section = 'user_info'
                
            elif '[INFO] retrieved:' in line and current_section == 'user_info':
                user_info = line.split('retrieved: ')[-1].strip()
                database_info['current_user'] = user_info
                
            # Extract version information
            elif '[INFO] fetching database server version' in line:
                current_section = 'version_info'
                
            elif '[INFO] retrieved:' in line and current_section == 'version_info':
                version_info = line.split('retrieved: ')[-1].strip()
                database_info['version'] = version_info
                
            # Check for successful data extraction
            elif '[INFO] retrieved:' in line:
                # This indicates successful data extraction
                if not result['vulnerable']:
                    result['vulnerable'] = True
                    
            # Extract summary information
            elif '[INFO] sqlmap identified the following injection point(s):' in line:
                result['vulnerable'] = True
                result['summary'] = 'SQL injection vulnerability found'
                
            elif '[INFO] no injection point(s) found' in line:
                result['vulnerable'] = False
                result['summary'] = 'No SQL injection vulnerabilities found'
                
            elif '[CRITICAL] all tested parameters appear to be not injectable' in line:
                result['vulnerable'] = False
                result['summary'] = 'No SQL injection vulnerabilities found'
                
            elif '[INFO] sqlmap got a connection to the target URL' in line:
                result['summary'] = 'Successfully connected to target'
                
            # Additional vulnerability indicators
            elif '[INFO] confirming that the parameter' in line and 'is injectable' in line:
                result['vulnerable'] = True
                
            elif '[INFO] parameter' in line and 'is vulnerable' in line:
                result['vulnerable'] = True
                
            elif '[INFO] found a total of' in line and 'injection point(s)' in line:
                result['vulnerable'] = True
                
        # Update result with parsed information
        result['vulnerabilities'] = vulnerabilities
        result['database_info'] = database_info
        
        # Fallback: Extract target from command if not found in output
        if result['target'] == 'Unknown' and self.command:
            for arg in self.command:
                if arg.startswith('http://') or arg.startswith('https://'):
                    result['target'] = arg
                    break
                elif arg == '-u' and len(self.command) > self.command.index(arg) + 1:
                    result['target'] = self.command[self.command.index(arg) + 1]
                    break
        
        # Update summary if we found vulnerabilities
        if result['vulnerable']:
            vuln_count = len(vulnerabilities)
            if vuln_count > 0:
                result['summary'] = f'Found {vuln_count} SQL injection vulnerability(ies)'
            else:
                result['summary'] = 'SQL injection vulnerability detected'
        else:
            result['summary'] = 'No SQL injection vulnerabilities found'


class RestApiClient(QObject):
    """
    Client for sqlmap REST API
    """
    
    task_created = Signal(str)
    task_started = Signal(str)
    task_completed = Signal(str, dict)
    task_failed = Signal(str, str)
    output_received = Signal(str, str)
    
    def __init__(self, api_url: str = "http://127.0.0.1:8775"):
        super().__init__()
        self.api_url = api_url
        self.session = None
        self.tasks = {}
        
    def start_api_server(self) -> bool:
        """
        Start sqlmap API server
        
        Returns:
            bool: True if started successfully
        """
        try:
            # Start sqlmap API server
            self.api_process = subprocess.Popen(
                ['sqlmapapi.py', '-s'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Test connection
            return self.test_connection()
            
        except Exception as e:
            print(f"Failed to start API server: {e}")
            return False
            
    def test_connection(self) -> bool:
        """
        Test connection to API server
        
        Returns:
            bool: True if connected
        """
        try:
            import requests
            response = requests.get(f"{self.api_url}/")
            return response.status_code == 200
        except:
            return False
            
    def create_task(self, target: Dict[str, Any], options: Dict[str, Any]) -> Optional[str]:
        """
        Create a new scan task
        
        Args:
            target (dict): Target information
            options (dict): Scan options
            
        Returns:
            str: Task ID if successful
        """
        try:
            import requests
            
            # Build command
            from sqlmapper.core.command_builder import CommandBuilder
            builder = CommandBuilder()
            command = builder.build_command(target, options)
            
            # Create task
            response = requests.post(f"{self.api_url}/task/new")
            if response.status_code == 200:
                task_id = response.json()['taskid']
                self.tasks[task_id] = {
                    'target': target,
                    'options': options,
                    'command': command,
                    'status': 'created'
                }
                self.task_created.emit(task_id)
                return task_id
                
        except Exception as e:
            print(f"Failed to create task: {e}")
            
        return None
        
    def start_task(self, task_id: str) -> bool:
        """
        Start a scan task
        
        Args:
            task_id (str): Task ID
            
        Returns:
            bool: True if started successfully
        """
        try:
            import requests
            
            if task_id not in self.tasks:
                return False
                
            # Start task
            response = requests.post(f"{self.api_url}/scan/{task_id}/start")
            if response.status_code == 200:
                self.tasks[task_id]['status'] = 'running'
                self.task_started.emit(task_id)
                return True
                
        except Exception as e:
            print(f"Failed to start task: {e}")
            
        return False
        
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task status
        
        Args:
            task_id (str): Task ID
            
        Returns:
            dict: Task status
        """
        try:
            import requests
            
            response = requests.get(f"{self.api_url}/scan/{task_id}/status")
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            print(f"Failed to get task status: {e}")
            
        return None
        
    def get_task_log(self, task_id: str) -> Optional[str]:
        """
        Get task log
        
        Args:
            task_id (str): Task ID
            
        Returns:
            str: Task log
        """
        try:
            import requests
            
            response = requests.get(f"{self.api_url}/scan/{task_id}/log")
            if response.status_code == 200:
                return response.text
                
        except Exception as e:
            print(f"Failed to get task log: {e}")
            
        return None
        
    def get_task_data(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task data
        
        Args:
            task_id (str): Task ID
            
        Returns:
            dict: Task data
        """
        try:
            import requests
            
            response = requests.get(f"{self.api_url}/scan/{task_id}/data")
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            print(f"Failed to get task data: {e}")
            
        return None
        
    def stop_task(self, task_id: str) -> bool:
        """
        Stop a scan task
        
        Args:
            task_id (str): Task ID
            
        Returns:
            bool: True if stopped successfully
        """
        try:
            import requests
            
            response = requests.post(f"{self.api_url}/scan/{task_id}/stop")
            if response.status_code == 200:
                if task_id in self.tasks:
                    self.tasks[task_id]['status'] = 'stopped'
                return True
                
        except Exception as e:
            print(f"Failed to stop task: {e}")
            
        return False
        
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a scan task
        
        Args:
            task_id (str): Task ID
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            import requests
            
            response = requests.delete(f"{self.api_url}/task/{task_id}/delete")
            if response.status_code == 200:
                if task_id in self.tasks:
                    del self.tasks[task_id]
                return True
                
        except Exception as e:
            print(f"Failed to delete task: {e}")
            
        return False
        
    def stop_api_server(self):
        """Stop the API server"""
        if hasattr(self, 'api_process'):
            self.api_process.terminate()
            try:
                self.api_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.api_process.kill()
