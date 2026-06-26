# Elegant Barbershop - Monthly Reports Generator

A desktop application for generating monthly reports (Attendance, Revenue, and Salaries) for barbershop management.

## Windows 7 Compatibility

This application has been specifically designed to work with **Windows 7** and **Python 3.8.10**.

### Requirements

- **Python 3.8.10** (Required for Windows 7 compatibility)
- **tkinter** (Built-in with Python, no separate installation needed)
- **openpyxl** (For Excel file generation)
- **PyYAML** (For configuration management)

### Installation

1. **Install Python 3.8.10** on your Windows 7 machine:
   - Download from: https://www.python.org/downloads/release/python-3810/
   - Make sure to check "Add Python to PATH" during installation

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Building Executable for Windows 7

To create a standalone executable that can run on Windows 7 without Python installed:

```bash
pip install pyinstaller==5.13.2
pyinstaller main.spec
```

The executable will be created in the `dist/main/` directory.

### Features

- **Generate Attendance Reports**: Track employee and stylist attendance
- **Generate Revenue Reports**: Monitor daily revenue and payment methods
- **Generate Salary Reports**: Calculate salaries based on attendance and revenue
- **Settings Management**: Configure employees, stylists, and output directory
- **Month Folder Organization**: All reports for a month are organized in dedicated folders

### GUI Framework

The application uses **tkinter**, Python's standard GUI library, which:
- Comes built-in with Python (no extra installation)
- Fully supports Windows 7
- Compatible with Python 3.8.10
- Provides a native Windows look and feel

### Migration from PySide6

This application was migrated from PySide6 to tkinter for Windows 7 compatibility:
- PySide6 requires Windows 10+ and Python 3.9+
- tkinter works perfectly with Windows 7 and Python 3.8.10
- All functionality has been preserved in the migration

### Configuration

The application stores configuration in `configs/config.yaml`:
- Employee information (name, working hours, daily rate)
- Stylist information (name, daily target, daily rate, working hours)
- Output directory for generated reports
- Payment methods

### Support

For issues or questions, please refer to the project documentation or contact the development team.
