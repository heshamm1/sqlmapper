#!/usr/bin/env python3
"""
SQLmapper - Desktop GUI for sqlmap
Cross-Platform Installation and Setup Script

This script automatically detects the operating system and installs SQLMap
if it's not found in the environment variables or system PATH.
"""

import os
import sys
import platform
import subprocess
import shutil
import urllib.request
import zipfile
import tarfile
import json
from pathlib import Path
from typing import Optional, Tuple
from setuptools import setup, find_packages


class SQLmapperInstaller:
    """Cross-platform installer for SQLmapper and SQLMap"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.project_root = Path(__file__).parent.absolute()
        self.sqlmap_dir = self.project_root / "sqlmap"
        self.sqlmap_path = None
        
    def print_banner(self):
        """Print installation banner"""
        print("=" * 60)
        print("           SQLmapper Installation Script")
        print("=" * 60)
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Architecture: {self.arch}")
        print(f"Python: {self.python_version}")
        print("=" * 60)
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        if sys.version_info < (3, 8):
            print("❌ Error: Python 3.8 or higher is required")
            print(f"   Current version: {self.python_version}")
            return False
        print(f"✅ Python version {self.python_version} is compatible")
        return True
        
    def check_sqlmap_installed(self) -> bool:
        """Check if SQLMap is already installed"""
        print("\n🔍 Checking for SQLMap installation...")
        
        # Check if sqlmap is in PATH
        sqlmap_path = shutil.which('sqlmap')
        if sqlmap_path:
            print(f"✅ SQLMap found in PATH: {sqlmap_path}")
            self.sqlmap_path = sqlmap_path
            return True
            
        # Check if sqlmap.py exists in project directory
        sqlmap_py = self.sqlmap_dir / "sqlmap.py"
        if sqlmap_py.exists():
            print(f"✅ SQLMap found in project directory: {sqlmap_py}")
            self.sqlmap_path = str(sqlmap_py)
            return True
            
        # Check if sqlmap directory exists
        if self.sqlmap_dir.exists() and (self.sqlmap_dir / "sqlmap.py").exists():
            print(f"✅ SQLMap found in project directory: {self.sqlmap_dir}")
            self.sqlmap_path = str(self.sqlmap_dir / "sqlmap.py")
            return True
            
        print("❌ SQLMap not found")
        return False
        
    def install_sqlmap(self) -> bool:
        """Install SQLMap based on the operating system"""
        print("\n📦 Installing SQLMap...")
        
        try:
            if self.system == "windows":
                return self._install_sqlmap_windows()
            elif self.system == "linux":
                return self._install_sqlmap_linux()
            elif self.system == "darwin":  # macOS
                return self._install_sqlmap_macos()
            else:
                print(f"❌ Unsupported operating system: {self.system}")
                return False
        except Exception as e:
            print(f"❌ Error installing SQLMap: {e}")
            return False
            
    def _install_sqlmap_windows(self) -> bool:
        """Install SQLMap on Windows"""
        print("Installing SQLMap for Windows...")
        
        # Create sqlmap directory
        self.sqlmap_dir.mkdir(exist_ok=True)
        
        # Download SQLMap
        sqlmap_url = "https://github.com/sqlmapproject/sqlmap/archive/master.zip"
        zip_path = self.sqlmap_dir / "sqlmap-master.zip"
        
        try:
            print("Downloading SQLMap from GitHub...")
            urllib.request.urlretrieve(sqlmap_url, zip_path)
            
            # Extract zip file
            print("Extracting SQLMap...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.sqlmap_dir)
            
            # Move contents to sqlmap directory
            extracted_dir = self.sqlmap_dir / "sqlmap-master"
            if extracted_dir.exists():
                for item in extracted_dir.iterdir():
                    dest = self.sqlmap_dir / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest)
                shutil.rmtree(extracted_dir)
            
            # Clean up
            zip_path.unlink()
            
            # Set sqlmap path
            self.sqlmap_path = str(self.sqlmap_dir / "sqlmap.py")
            
            print("✅ SQLMap installed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error installing SQLMap: {e}")
            return False
            
    def _install_sqlmap_linux(self) -> bool:
        """Install SQLMap on Linux"""
        print("Installing SQLMap for Linux...")
        
        # Try to install via package manager first
        if self._try_package_manager_install():
            return True
            
        # Fallback to manual installation
        return self._install_sqlmap_manual()
        
    def _install_sqlmap_macos(self) -> bool:
        """Install SQLMap on macOS"""
        print("Installing SQLMap for macOS...")
        
        # Try to install via Homebrew first
        if self._try_homebrew_install():
            return True
            
        # Fallback to manual installation
        return self._install_sqlmap_manual()
        
    def _try_package_manager_install(self) -> bool:
        """Try to install SQLMap via package manager"""
        package_managers = [
            ("apt", "apt-get install -y sqlmap"),
            ("yum", "yum install -y sqlmap"),
            ("dnf", "dnf install -y sqlmap"),
            ("pacman", "pacman -S --noconfirm sqlmap"),
            ("zypper", "zypper install -y sqlmap"),
        ]
        
        for pm, cmd in package_managers:
            if shutil.which(pm):
                try:
                    print(f"Trying to install SQLMap via {pm}...")
                    result = subprocess.run(cmd.split(), capture_output=True, text=True)
                    if result.returncode == 0:
                        # Verify installation
                        sqlmap_path = shutil.which('sqlmap')
                        if sqlmap_path:
                            print(f"✅ SQLMap installed via {pm}: {sqlmap_path}")
                            self.sqlmap_path = sqlmap_path
                            return True
                except Exception as e:
                    print(f"Package manager {pm} failed: {e}")
                    continue
                    
        return False
        
    def _try_homebrew_install(self) -> bool:
        """Try to install SQLMap via Homebrew on macOS"""
        if not shutil.which('brew'):
            return False
            
        try:
            print("Trying to install SQLMap via Homebrew...")
            result = subprocess.run(['brew', 'install', 'sqlmap'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                sqlmap_path = shutil.which('sqlmap')
                if sqlmap_path:
                    print(f"✅ SQLMap installed via Homebrew: {sqlmap_path}")
                    self.sqlmap_path = sqlmap_path
                    return True
        except Exception as e:
            print(f"Homebrew installation failed: {e}")
            
        return False
        
    def _install_sqlmap_manual(self) -> bool:
        """Manually install SQLMap by cloning from GitHub"""
        print("Installing SQLMap manually from GitHub...")
        
        # Create sqlmap directory
        self.sqlmap_dir.mkdir(exist_ok=True)
        
        try:
            # Try to clone with git first
            if shutil.which('git'):
                print("Cloning SQLMap repository...")
                result = subprocess.run([
                    'git', 'clone', 
                    'https://github.com/sqlmapproject/sqlmap.git',
                    str(self.sqlmap_dir)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.sqlmap_path = str(self.sqlmap_dir / "sqlmap.py")
                    print("✅ SQLMap cloned successfully")
                    return True
                    
        except Exception as e:
            print(f"Git clone failed: {e}")
            
        # Fallback to downloading zip
        try:
            sqlmap_url = "https://github.com/sqlmapproject/sqlmap/archive/master.zip"
            zip_path = self.sqlmap_dir / "sqlmap-master.zip"
            
            print("Downloading SQLMap from GitHub...")
            urllib.request.urlretrieve(sqlmap_url, zip_path)
            
            # Extract zip file
            print("Extracting SQLMap...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.sqlmap_dir)
            
            # Move contents to sqlmap directory
            extracted_dir = self.sqlmap_dir / "sqlmap-master"
            if extracted_dir.exists():
                for item in extracted_dir.iterdir():
                    dest = self.sqlmap_dir / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest)
                shutil.rmtree(extracted_dir)
            
            # Clean up
            zip_path.unlink()
            
            self.sqlmap_path = str(self.sqlmap_dir / "sqlmap.py")
            print("✅ SQLMap installed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Manual installation failed: {e}")
            return False
            
    def install_python_dependencies(self) -> bool:
        """Install Python dependencies"""
        print("\n📦 Installing Python dependencies...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
            
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # Install requirements
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         check=True, capture_output=True)
            
            print("✅ Python dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing Python dependencies: {e}")
            return False
            
    def create_launcher_scripts(self) -> bool:
        """Create platform-specific launcher scripts"""
        print("\n🔧 Creating launcher scripts...")
        
        try:
            if self.system == "windows":
                self._create_windows_launcher()
            else:
                self._create_unix_launcher()
                
            print("✅ Launcher scripts created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating launcher scripts: {e}")
            return False
            
    def _create_windows_launcher(self):
        """Create Windows batch launcher"""
        launcher_content = f'''@echo off
cd /d "{self.project_root}"
python app.py %*
pause
'''
        
        launcher_path = self.project_root / "run_sqlmapper.bat"
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
            
        # Make it executable
        os.chmod(launcher_path, 0o755)
        
    def _create_unix_launcher(self):
        """Create Unix shell launcher"""
        launcher_content = f'''#!/bin/bash
cd "{self.project_root}"
python3 app.py "$@"
'''
        
        launcher_path = self.project_root / "run_sqlmapper.sh"
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
            
        # Make it executable
        os.chmod(launcher_path, 0o755)
        
    def update_config(self) -> bool:
        """Update configuration with SQLMap path"""
        print("\n⚙️ Updating configuration...")
        
        try:
            config_file = self.project_root / "config.json"
            config = {}
            
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            
            # Update SQLMap path
            config['sqlmap_path'] = self.sqlmap_path
            config['installation_complete'] = True
            config['install_date'] = str(Path().cwd())
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
                
            print("✅ Configuration updated")
            return True
            
        except Exception as e:
            print(f"❌ Error updating configuration: {e}")
            return False
            
    def verify_installation(self) -> bool:
        """Verify the installation"""
        print("\n🔍 Verifying installation...")
        
        # Check Python dependencies
        try:
            import PySide6
            import requests
            print("✅ Python dependencies verified")
        except ImportError as e:
            print(f"❌ Python dependency error: {e}")
            return False
            
        # Check SQLMap
        if not self.sqlmap_path or not Path(self.sqlmap_path).exists():
            print("❌ SQLMap not found")
            return False
            
        print(f"✅ SQLMap verified: {self.sqlmap_path}")
        
        # Test SQLMap
        try:
            result = subprocess.run([sys.executable, self.sqlmap_path, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ SQLMap is working correctly")
            else:
                print("⚠️ SQLMap version check failed, but file exists")
        except Exception as e:
            print(f"⚠️ Could not test SQLMap: {e}")
            
        return True
        
    def print_usage_instructions(self):
        """Print usage instructions"""
        print("\n" + "=" * 60)
        print("           Installation Complete!")
        print("=" * 60)
        print("\n🚀 To run SQLmapper:")
        
        if self.system == "windows":
            print("   Double-click: run_sqlmapper.bat")
            print("   Or run: python app.py")
        else:
            print("   Run: ./run_sqlmapper.sh")
            print("   Or run: python3 app.py")
            
        print(f"\n📁 SQLMap location: {self.sqlmap_path}")
        print(f"📁 Project directory: {self.project_root}")
        
        print("\n⚠️  Legal Disclaimer:")
        print("   This tool is for authorized security testing only.")
        print("   Use responsibly and in compliance with applicable laws.")
        
        print("\n📚 For more information:")
        print("   - README.md: Basic usage and features")
        print("   - GitHub: https://github.com/sqlmapper/sqlmapper")
        
    def run(self) -> bool:
        """Run the complete installation process"""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            return False
            
        # Check if SQLMap is already installed
        if self.check_sqlmap_installed():
            print("\n✅ SQLMap is already installed")
        else:
            # Install SQLMap
            if not self.install_sqlmap():
                print("\n❌ Failed to install SQLMap")
                return False
                
        # Install Python dependencies
        if not self.install_python_dependencies():
            print("\n❌ Failed to install Python dependencies")
            return False
            
        # Create launcher scripts
        if not self.create_launcher_scripts():
            print("\n❌ Failed to create launcher scripts")
            return False
            
        # Update configuration
        if not self.update_config():
            print("\n❌ Failed to update configuration")
            return False
            
        # Verify installation
        if not self.verify_installation():
            print("\n❌ Installation verification failed")
            return False
            
        # Print usage instructions
        self.print_usage_instructions()
        
        return True


def main():
    """Main installation function"""
    installer = SQLmapperInstaller()
    
    try:
        success = installer.run()
        if success:
            print("\n🎉 Installation completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Installation failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

# Setup configuration
setup(
    name="sqlmapper",
    version="1.0.0",
    author="SQLmapper Team",
    author_email="contact@sqlmapper.dev",
    description="A desktop GUI application for sqlmap, similar to Zenmap for nmap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sqlmapper/sqlmapper",
    project_urls={
        "Bug Reports": "https://github.com/sqlmapper/sqlmapper/issues",
        "Source": "https://github.com/sqlmapper/sqlmapper",
        "Documentation": "https://github.com/sqlmapper/sqlmapper/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Security :: Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sqlmapper=app:main",
        ],
        "gui_scripts": [
            "sqlmapper-gui=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "sqlmapper": [
            "*.png",
            "*.ico",
            "*.qss",
            "data/*",
            "templates/*",
        ],
    },
    keywords="sqlmap, gui, security, penetration-testing, sql-injection, cybersecurity",
    zip_safe=False,
)


if __name__ == "__main__":
    main()
