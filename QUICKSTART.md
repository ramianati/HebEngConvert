# Quick Start Guide - Running from Source

This guide will help you run HebEngConvert directly from source code without building an executable.

## Prerequisites

- **Windows**: Python 3.8+ installed
- **macOS**: Python 3.8+ (use `python3` command)
- **Git** (optional, for cloning)

## Setup Steps

### 1. Get the Source Code

**Option A: Using Git**
```bash
git clone <repository-url>
cd HebEngConvert
```

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to a folder
3. Open terminal/PowerShell in that folder

### 2. Create Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pystray` - System tray icon
- `Pillow` - Image handling
- `pyperclip` - Clipboard access
- `customtkinter` - Modern UI
- `pynput` - Global hotkeys

### 4. Run the Application

**Windows:**
```powershell
python main.py
```

**macOS:**
```bash
python main.py
```

## First Launch

### Windows
- System tray icon will appear
- Default hotkey: `Ctrl+Alt+D`
- Press the hotkey to open the window

### macOS
- Menu bar icon will appear
- Default hotkey: `Cmd+Shift+D`
- **IMPORTANT**: Grant Accessibility permissions when prompted:
  1. Open **System Preferences**
  2. Go to **Security & Privacy** → **Privacy** → **Accessibility**
  3. Click lock to make changes
  4. Add Terminal (or Python) to the list
  5. Restart the app

## Usage

1. **Copy text** to clipboard
2. **Press hotkey** (Ctrl+Alt+D or Cmd+Shift+D)
3. **View conversions** in both directions
4. **Click copy button** next to desired conversion
5. **Close window** - app stays in tray/menu bar

## Stopping the Application

- Right-click tray/menu bar icon → Exit
- Or close the main window and select Exit

## Common Issues

### "python not found" (macOS)
Use `python3` instead of `python`

### Dependencies not installing
- Activate virtual environment first
- Use `pip3` instead of `pip` on macOS

### Hotkey not working
- **Windows**: Try running as administrator
- **macOS**: Grant Accessibility permissions (see above)

### Application crashes on startup
- Check Python version (must be 3.8+)
- Verify all dependencies installed: `pip list`
- Check for conflicting port (default: 54321)

## Customization

Open settings via the gear icon in the app:
- Change hotkey combination
- Modify single-instance port
- Enable/disable port checking

Settings are saved automatically.

## Development Mode

To run with debug output:
```bash
python main.py --debug  # (if implemented)
```

Or check console output for any errors.

## Next Steps

- See [README.md](README.md) for full documentation
- Build standalone executable: See "Building from Source" in README
- Report issues on GitHub
