#!/usr/bin/env python3
"""
SQLmapper - Desktop GUI for sqlmap
Main application launcher
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PySide6
        print("✓ PySide6 is available")
    except ImportError:
        print("✗ PySide6 is not installed. Please run: pip install PySide6")
        return False
        
    try:
        import requests
        print("✓ requests is available")
    except ImportError:
        print("✗ requests is not installed. Please run: pip install requests")
        return False
        
    return True

def check_sqlmap():
    """Check if sqlmap is available"""
    import shutil
    
    sqlmap_path = shutil.which('sqlmap')
    if sqlmap_path:
        print(f"✓ sqlmap found at: {sqlmap_path}")
        return True
    else:
        print("⚠ sqlmap not found in PATH")
        
        # Check for sqlmap.py in various locations
        possible_paths = [
            'sqlmap.py',  # Current directory
            'sqlmap/sqlmap.py',  # Local sqlmap directory (created by setup.py)
            '../sqlmap.py',  # Parent directory
        ]
        
        # If running from executable, check relative to executable location
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            # Go up to sqlmap directory (executable is in sqlmapper/dist/)
            sqlmap_dir = os.path.dirname(os.path.dirname(exe_dir))
            possible_paths.extend([
                os.path.join(sqlmap_dir, 'sqlmap.py'),
                os.path.join(sqlmap_dir, 'sqlmap', 'sqlmap.py'),
                os.path.join(exe_dir, 'sqlmap.py'),
                os.path.join(exe_dir, '..', 'sqlmap.py'),
                os.path.join(exe_dir, '..', 'sqlmap', 'sqlmap.py'),
            ])
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✓ sqlmap.py found at: {path}")
                return True
        
        print("✗ sqlmap not found. Please install sqlmap or place sqlmap.py in the project directory")
        return False

def main():
    """Main application entry point"""
    print("SQLmapper - Desktop GUI for sqlmap")
    print("=" * 50)
    
    # Check if we're running in windowed mode (PyInstaller)
    is_windowed = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        if is_windowed:
            # In windowed mode, we can't use input(), so just exit
            print("Exiting due to missing dependencies...")
            sys.exit(1)
        else:
            input("Press Enter to exit...")
            sys.exit(1)
        
    # Check sqlmap
    if not check_sqlmap():
        print("\nWarning: sqlmap not found. The application may not work properly.")
        if is_windowed:
            # In windowed mode, continue anyway since we can't ask user
            print("Continuing anyway in windowed mode...")
        else:
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    print("\nStarting SQLmapper...")
    
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        from PySide6.QtCore import Qt
        from sqlmapper.gui.main_window import MainWindow
        from sqlmapper.utils.logger import setup_logging
        
        # Setup logging
        setup_logging()
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("SQLmapper")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("SQLmapper")
        
        # Set application style
        app.setStyle('Fusion')
        
        # Show sqlmap warning in windowed mode if needed
        if is_windowed and not check_sqlmap():
            QMessageBox.warning(
                None,
                "SQLmap Warning",
                "SQLmap not found. The application may not work properly.\n\n"
                "Please ensure sqlmap.py is in the parent directory (H:\\sqlmap\\sqlmap.py).\n\n"
                "The executable should be in H:\\sqlmap\\sqlmapper\\dist\\"
            )
        
        # Set application icon
        try:
            from PySide6.QtGui import QIcon, QPixmap
            from PySide6.QtCore import Qt
            
            # Try logo.ico first, then logo.png
            logo_paths = [project_root / "logo.ico", project_root / "logo.png"]
            icon_loaded = False
            
            for logo_path in logo_paths:
                if logo_path.exists():
                    if logo_path.suffix.lower() == '.ico':
                        # Load ICO file directly
                        icon = QIcon(str(logo_path))
                        app.setWindowIcon(icon)
                        print("✓ Application icon loaded successfully")
                        icon_loaded = True
                        break
                    else:
                        # Load PNG image
                        pixmap = QPixmap(str(logo_path))
                        if not pixmap.isNull():
                            # Scale to appropriate size if needed
                            if pixmap.width() > 64 or pixmap.height() > 64:
                                pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            
                            icon = QIcon(pixmap)
                            app.setWindowIcon(icon)
                            print("✓ Application icon loaded successfully")
                            icon_loaded = True
                            break
            
            if not icon_loaded:
                print("⚠ No logo file found (logo.ico or logo.png)")
        except Exception as e:
            print(f"Could not set application icon: {e}")
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        print("✓ SQLmapper GUI started successfully!")
        print("✓ Custom arguments feature available in Advanced tab")
        
        # Start event loop
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please ensure all dependencies are installed correctly.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error starting application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
