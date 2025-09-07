# SQLmapper

<div align="center">

```
 _____  _____  __     _____  _____  _____  _____  _____  _____  _____ 
|   __||     ||  |   |     ||  _  ||  _  ||  _  ||  _  ||   __|| __  |
|__   ||  |  ||  |__ | | | ||     ||   __||   __||   __||   __||    -|
|_____||__  _||_____||_|_|_||__|__||__|   |__|   |__|   |_____||__|__|
          |__|          GUI Version of SQLMap
```

**SQLmapper** is a professional desktop GUI application for sqlmap, similar to how Zenmap is a GUI for nmap. It provides a clean, beginner-friendly interface to run and manage sqlmap scans.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/sqlmapper/sqlmapper)
[![Downloads](https://img.shields.io/badge/downloads-1000%2B-brightgreen.svg)](https://github.com/sqlmapper/sqlmapper/releases)

[Installation](#-installation) • [Usage](#-usage) • [Features](#-features) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

## ⚠️ Legal Disclaimer

**SQLmapper is a tool for authorized security testing only.**

By using this software, you agree to:
- Only test systems you own or have explicit permission to test
- Comply with all applicable laws and regulations
- Use the tool responsibly and ethically

The developers are not responsible for any misuse of this tool.

## 🚀 Installation

### Quick Start (Recommended)

```bash
# Clone the repository
git clone https://github.com/sqlmapper/sqlmapper.git
cd sqlmapper

# Run the automated installer
python setup.py
```

The installer will automatically:
- ✅ Detect your operating system (Windows, Linux, macOS)
- ✅ Check for Python 3.8+ compatibility
- ✅ Install SQLMap if not found
- ✅ Install all Python dependencies
- ✅ Create launcher scripts
- ✅ Configure the application

### Manual Installation

If you prefer manual installation:

#### Prerequisites

1. **Python 3.8+** installed on your system
2. **SQLMap** installed and accessible

#### Install SQLMap

**Option 1: Package Manager (Recommended)**
```bash
# Ubuntu/Debian
sudo apt install sqlmap

# macOS (with Homebrew)
brew install sqlmap

# Windows (with Chocolatey)
choco install sqlmap
```

**Option 2: Manual Installation**
```bash
# Clone SQLMap repository
git clone https://github.com/sqlmapproject/sqlmap.git
```

#### Install SQLmapper

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sqlmapper/sqlmapper.git
   cd sqlmapper
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## 🎯 Features

### Core Features
- 🎯 **Target Input**: Support for URLs, request files, headers, and cookies
- 📋 **Scan Profiles**: Pre-configured profiles (Quick Scan, Full Scan, Custom)
- ⚙️ **Options Panel**: Comprehensive configuration for risk/level, proxy, auth, timeout, etc.
- 📊 **Real-time Console**: Live output streaming from sqlmap
- 🛑 **Stop Control**: Graceful scan termination
- 📈 **Results Panel**: Display detected DBMS, injectable parameters, and findings
- 📚 **Scan History**: Track previous scans with timestamps and profiles
- 💾 **Configuration**: Persistent settings and profile management

### Advanced Features
- 🔄 **Cross-Platform**: Works on Windows, Linux, and macOS
- 🎨 **Modern UI**: Clean, intuitive interface with dark theme console
- 🔧 **Auto-Installation**: Automatically installs SQLMap if not found
- 📦 **Easy Setup**: One-command installation and configuration
- 🛡️ **Security**: Input validation and safe command construction
- ⚡ **Performance**: Optimized for speed and reliability

## 📸 Screenshots

<div align="center">

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Scan Options
![Scan Options](screenshots/scan-options.png)

### Results Display
![Results Display](screenshots/results-display.png)

</div>

## 🚀 Usage

### Basic Usage

1. **Launch SQLmapper**:
   ```bash
   python app.py
   ```

2. **Configure Target**:
   - Enter target URL in the URL tab
   - Or load a request file in the Request File tab
   - Add custom headers if needed

3. **Select Profile**:
   - Choose from Quick Scan, Full Scan, or Custom
   - Adjust options in the Options panel if needed

4. **Start Scan**:
   - Click "Start Scan" button
   - Monitor progress in the Console Output panel
   - View results in the Results panel

### Advanced Configuration

#### Scan Profiles

- **Quick Scan**: Fast, low-risk scan for basic detection
- **Full Scan**: Comprehensive scan with all techniques and detection options
- **Custom**: User-defined profile with specific settings

#### Options Categories

- **General**: Risk level, threads, timeout, retries
- **Injection**: Techniques, DBMS type
- **Detection**: What information to retrieve
- **Optimization**: Proxy, Tor, delays
- **Advanced**: Tamper scripts, OS detection, batch mode

## 🏗️ Architecture

### Design Patterns

- **MVC/MVP**: Separation of concerns between GUI, business logic, and data
- **Command Pattern**: CommandBuilder for constructing sqlmap arguments
- **Observer Pattern**: Signal/slot for GUI updates
- **Factory Pattern**: Profile creation and management

### Key Components

1. **CommandBuilder**: Safely constructs sqlmap command line arguments
2. **SubprocessRunner**: Executes sqlmap and streams output
3. **Config**: Handles user preferences and saved profiles
4. **GUI Components**: Modular UI components for different functionalities

## 📁 Project Structure

```
sqlmapper/
├── app.py                 # Main application launcher
├── setup.py              # Installation and setup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── sqlmapper/            # Main package
│   ├── gui/             # GUI components
│   │   ├── main_window.py
│   │   └── components/  # UI components
│   ├── core/            # Core functionality
│   │   ├── command_builder.py
│   │   └── subprocess_runner.py
│   └── utils/           # Utilities
│       ├── config.py
│       └── logger.py
└── logo.png, logo.ico   # Application assets
```

## 🔧 Configuration

SQLmapper stores configuration in `~/.sqlmapper/config.json`:

- **Window geometry**: Window size and position
- **Scan profiles**: Custom scan configurations
- **Recent targets**: Recently scanned URLs/files
- **Scan history**: Previous scan results
- **Settings**: Application preferences

## 🛠️ Development

### Setting up Development Environment

1. **Clone repository**:
   ```bash
   git clone https://github.com/sqlmapper/sqlmapper.git
   cd sqlmapper
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run in development mode**:
   ```bash
   python app.py
   ```

### Building Executables

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed app.py

# Or with custom icon
pyinstaller --onefile --windowed --icon=logo.ico app.py
```

## 🐛 Troubleshooting

### Common Issues

1. **SQLMap not found**:
   - Run `python setup.py` to automatically install SQLMap
   - Or ensure SQLMap is installed and in PATH

2. **Import errors**:
   - Check Python version (3.8+ required)
   - Install dependencies: `pip install -r requirements.txt`

3. **GUI not displaying**:
   - Ensure PySide6 is installed
   - Check display settings on Linux

4. **Permission errors**:
   - Run with appropriate permissions
   - Check file/directory permissions

### Logs

Application logs are stored in:
- **Windows**: `%APPDATA%/sqlmapper/logs/`
- **Linux/macOS**: `~/.sqlmapper/logs/`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [sqlmap](https://github.com/sqlmapproject/sqlmap) - The underlying SQL injection tool
- [PySide6](https://pypi.org/project/PySide6/) - Qt for Python
- [Zenmap](https://nmap.org/zenmap/) - Inspiration for the GUI approach

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/sqlmapper/sqlmapper?style=social)
![GitHub forks](https://img.shields.io/github/forks/sqlmapper/sqlmapper?style=social)
![GitHub issues](https://img.shields.io/github/issues/sqlmapper/sqlmapper)
![GitHub pull requests](https://img.shields.io/github/issues-pr/sqlmapper/sqlmapper)

## 📈 Roadmap

### Version 1.1
- [ ] REST API integration
- [ ] Result export functionality
- [ ] Advanced result parsing
- [ ] Theme support

### Version 1.2
- [ ] Plugin system
- [ ] Custom tamper scripts
- [ ] Batch scanning
- [ ] Report generation

### Version 2.0
- [ ] Multi-platform packaging
- [ ] Advanced visualization
- [ ] Integration with other security tools
- [ ] Cloud deployment support

---

<div align="center">

**Made with ❤️ for the security community**

[Report Bug](https://github.com/sqlmapper/sqlmapper/issues) • [Request Feature](https://github.com/sqlmapper/sqlmapper/issues) • [View Documentation](https://github.com/sqlmapper/sqlmapper/wiki)

</div>