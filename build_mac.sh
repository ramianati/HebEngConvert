#!/bin/bash

# macOS build script for HebEngConvert
# Creates a standalone .app bundle using PyInstaller

echo "Building HebEngConvert for macOS..."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script must be run on macOS"
    exit 1
fi

# Check if virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Warning: No virtual environment detected. Consider activating venv first."
fi

# Install dependencies if needed
echo "Installing dependencies..."
pip install -q pyinstaller pystray pillow pyperclip customtkinter pynput

# Create .app bundle
echo "Creating .app bundle..."
pyinstaller --clean \
    --windowed \
    --name "HebEngConvert" \
    --icon="assets/clipboard.png" \
    --add-data "assets:assets" \
    --hidden-import="PIL._tkinter_finder" \
    --hidden-import="customtkinter" \
    --hidden-import="pynput.keyboard" \
    --hidden-import="pynput.mouse" \
    --osx-bundle-identifier="com.hebengconvert.app" \
    main.py

# Check if build succeeded
if [ -d "dist/HebEngConvert.app" ]; then
    echo "✓ Build successful!"
    echo "Application bundle: dist/HebEngConvert.app"
    echo ""
    echo "To install:"
    echo "  cp -r dist/HebEngConvert.app /Applications/"
    echo ""
    echo "To run:"
    echo "  open dist/HebEngConvert.app"
    echo ""
    echo "NOTE: On first launch, macOS may require Accessibility permission"
    echo "for the global hotkey to work. Go to:"
    echo "  System Settings → Privacy & Security → Accessibility"
    echo "  and enable HebEngConvert."
else
    echo "✗ Build failed!"
    exit 1
fi

# Optional: Code sign (requires Developer ID)
# echo "Signing application..."
# codesign --force --deep --sign "Developer ID Application: Your Name" dist/HebEngConvert.app

echo "Done!"
