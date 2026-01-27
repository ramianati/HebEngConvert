# HebEngConvert

HebEngConvert is a modern, lightweight cross-platform utility (Windows & macOS) designed to instantly convert text between Hebrew and English keyboard layouts. Whether you've accidentally typed a sentence in the wrong language or need to quickly fix clipboard content, this tool provides a seamless one-click solution.

> [!NOTE]
> This application was created entirely using **AI** (Antigravity by Google DeepMind), demonstrating advanced agentic coding and UI design capabilities.

## Features

- **Tray-Based Utility**: Runs quietly in your system tray with a custom clipboard icon.
- **Global Hotkey**: Instantly open and refresh the converter window with a customizable shortcut (default: `CTRL+ALT+D` on Windows, `CMD+SHIFT+D` on macOS).
- **One-Click Conversion**: 
    - Top section: English text to Hebrew layout.
    - Bottom section: Hebrew text to English layout.
- **Micro-Refresh**: Quickly update the window content with your current clipboard.
- **Sleek, Modern UI**: Built with `customtkinter`, featuring a high-contrast dark theme and vibrant blue/purple gradients.
- **Single Instance Support**: Ensures only one copy of the app runs at a time (configurable via settings).

## Screenshot

![HebEngConvert Interface](screenshot.png)

## How to Use

1. **Launch**: 
   - **Windows**: Run `HebEngConvert.exe`. You'll see a notification in the Windows Action Center and a purple clipboard icon in your tray.
   - **macOS**: Open `HebEngConvert.app` from Applications. You'll see a notification and a clipboard icon in your menu bar.
2. **Convert**: Simply copy any text to your clipboard and hit your global hotkey (Default: `CTRL+ALT+D` on Windows, `CMD+SHIFT+D` on macOS).
3. **Copy Back**: Click the large purple clipboard icon next to the converted text to copy it back to your clipboard instantly.
4. **Refresh**: Use the circular arrow icon in the bottom control row to pull the latest clipboard content manually.

## Settings & Configuration

Click the **Gear Icon** in the application window to open the settings dialog:

- **Hotkey Customization**:
    1. Click the "Capture" button.
    2. Press your desired key combination (e.g., `Ctrl+Shift+H`).
    3. The application will record and format it automatically.
    4. Click "Save Settings" to apply instantly.
- **Instance Port**:
    - **Single Instance Check**: If enabled, the app uses a local communication port (default: `54321`) to ensure only one window is open. If you run the app a second time, it will simply refocus the existing one.
    - **Port Number**: You can change this port if it conflicts with other software on your machine.
- **Persistence**: All settings are automatically saved:
    - **Windows**: `~/.hebengconvert.json`
    - **macOS**: `~/Library/Application Support/HebEngConvert/settings.json`

## Privacy & Security

**100% Local & Private**
- ✅ **No telemetry or analytics** - Zero network calls, no data collection
- ✅ **Fully offline** - No internet connection required
- ✅ **Open source** - All code is transparent and reviewable on GitHub

**What the app accesses:**
- 📋 **Clipboard** - Reads clipboard content when you open the window or press refresh
- ⌨️ **Keyboard** - Listens for your custom global hotkey (default: Ctrl+Alt+D)
- 💾 **Local storage** - Saves settings locally (Windows: `~/.hebengconvert.json`, macOS: `~/Library/Application Support/HebEngConvert/settings.json`)
- 🖥️ **System tray** - Displays a tray icon for quick access

**No access to:**
- ❌ Network/Internet
- ❌ File system (beyond its own config file)
- ❌ Other applications
- ❌ System processes

## Requirements

- **OS**: Windows 10/11 or macOS 10.14+
- **Python**: 3.8 or higher (for running from source)
- **Standalone**: No installation required for pre-built executables.

## Running from Source

Want to run the application without building an executable? Follow these steps:

### Windows

1. **Download the source code**
   ```powershell
   git clone <repository-url>
   cd HebEngConvert
   ```
   Or download and extract the ZIP from GitHub.

2. **Create a virtual environment** (recommended)
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```powershell
   python main.py
   ```

The application will start, and you'll see the system tray icon appear.

### macOS

1. **Download the source code**
   ```bash
   git clone <repository-url>
   cd HebEngConvert
   ```
   Or download and extract the ZIP from GitHub.

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

   > [!IMPORTANT]
   > On first launch, macOS may prompt you to grant Accessibility permissions:
   > 1. Go to **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
   > 2. Click the lock icon to make changes
   > 3. Add Terminal (or your Python executable) to the list
   > 4. Restart the application

The application will start, and you'll see the menu bar icon appear.

### Troubleshooting

**"Command not found: python"** (macOS)
- Use `python3` instead of `python`

**Missing dependencies error**
- Make sure you activated the virtual environment
- Re-run `pip install -r requirements.txt`

**Hotkey not working**
- **Windows**: Run as administrator if needed
- **macOS**: Grant Accessibility permissions (see above)

**Application won't start**
- Check if another instance is running
- Disable "Single Instance Check" by editing the config file manually

## Building from Source

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python build_windows.py
```

### macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x build_mac.sh
./build_mac.sh
```

## Platform-Specific Notes

### macOS
- Default hotkey uses `CMD` instead of `CTRL` (e.g., `CMD+SHIFT+D`)
- Settings are stored in `~/Library/Application Support/HebEngConvert/`
- The app uses pynput for global hotkey detection
- On first launch, you may need to grant Accessibility permissions in System Preferences

### Windows
- Default hotkey uses `CTRL` (e.g., `CTRL+ALT+D`)
- Settings are stored in your home directory as `.hebengconvert.json`
- Single instance check uses local socket communication

## Disclaimer

This software is provided "as is", without warranty of any kind, express or implied. By using this application, you agree that the author and AI creators are not responsible for any issues, data loss, or system conflicts that may arise. Always ensure the Hotkey and Instance Port do not conflict with other critical software on your machine.

---
*Created by Antigravity AI.*
