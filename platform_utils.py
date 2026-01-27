"""
Platform-specific utilities for cross-platform support (Windows/macOS).
"""
import sys
import os
import platform


def get_platform():
    """Returns 'windows' or 'darwin' (macOS)."""
    return platform.system().lower()


def is_windows():
    """Check if running on Windows."""
    return get_platform() == 'windows'


def is_mac():
    """Check if running on macOS."""
    return get_platform() == 'darwin'


def get_default_hotkey():
    """Returns platform-appropriate default hotkey."""
    if is_mac():
        return "<cmd>+<shift>+d"
    else:
        return "<ctrl>+<alt>+d"


def get_config_path():
    """Returns platform-appropriate configuration file path."""
    if is_mac():
        # macOS: ~/Library/Application Support/HebEngConvert/settings.json
        config_dir = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "HebEngConvert"
        )
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "settings.json")
    else:
        # Windows/Linux: ~/.hebengconvert.json
        return os.path.join(os.path.expanduser("~"), ".hebengconvert.json")


def normalize_modifier_key(key):
    """
    Normalize modifier key names across platforms.
    Maps platform-specific names to canonical forms.
    """
    key_lower = key.lower()
    
    # macOS uses 'cmd', Windows uses 'ctrl' for primary modifier
    if key_lower in ['cmd', 'command']:
        return 'cmd'
    elif key_lower in ['ctrl', 'control']:
        return 'ctrl'
    elif key_lower in ['alt', 'option']:
        return 'alt'
    elif key_lower == 'shift':
        return 'shift'
    
    return key_lower


def format_hotkey_display(hotkey_str):
    """
    Format hotkey string for display using platform-appropriate symbols.
    On macOS: shows ⌘, ⇧, ⌥
    On Windows: shows Ctrl, Shift, Alt
    """
    clean = hotkey_str.replace("<", "").replace(">", "").upper()
    
    if is_mac():
        # Use macOS symbols
        clean = clean.replace("CMD", "⌘")
        clean = clean.replace("SHIFT", "⇧")
        clean = clean.replace("ALT", "⌥")
        clean = clean.replace("OPTION", "⌥")
        clean = clean.replace("CTRL", "⌃")
    
    return clean


def get_modifier_keys():
    """Returns list of valid modifier keys for current platform."""
    if is_mac():
        return ['cmd', 'ctrl', 'alt', 'shift', 'option']
    else:
        return ['ctrl', 'alt', 'shift', 'win']
