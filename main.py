import pystray
from PIL import Image
import pyperclip
import threading
from gui import ClipboardWindow
import os
import sys

from pynput import keyboard

import json
from platform_utils import (
    get_default_hotkey,
    get_config_path,
    get_modifier_keys,
    format_hotkey_display,
    is_mac,
    is_windows
)

# Global app instance for single-instance control
app = None
icon = None
hotkey_listener = None
config_path = get_config_path()

def load_config():
    default_config = {"hotkey": get_default_hotkey(), "port": 54321, "use_port": True}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return {**default_config, **json.load(f)}
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            pass
    return default_config

def save_config(config):
    try:
        with open(config_path, "w") as f:
            json.dump(config, f)
    except (PermissionError, OSError):
        pass

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def on_tray_clicked(icon, item):
    text = str(item)
    if text.startswith("Open"):
        show_clipboard()
    elif text == "Help":
        show_help()
    elif text == "Exit":
        exit_app()

def show_clipboard():
    if app:
        try:
            content = pyperclip.paste()
            if not content:
                content = "[No text found]"
        except Exception as e:
            content = f"Error: {e}"
        app.after(0, lambda: app.show(content))

def show_help():
    if app:
        app.after(0, app.open_help)
        app.after(10, app.show) # Focus the window so help dialog is visible

def exit_app():
    global icon, app, hotkey_listener
    if hotkey_listener:
        hotkey_listener.stop()
    if icon:
        icon.stop()
    if app:
        app.quit()
    sys.exit(0)

def _safe_notify(clean_hk):
    """Send a tray notification if supported by the platform."""
    try:
        if icon:
            icon.notify(f"Press {clean_hk} to open.", "HebEngConvert is Ready")
    except Exception:
        pass  # Notifications may not be available on all macOS configurations

def setup_tray(hotkey_str):
    global icon
    icon_path = get_resource_path("assets/clipboard.png")
    image = Image.open(icon_path)
    
    clean_hk = format_hotkey_display(hotkey_str)
    
    # Create the menu
    menu = pystray.Menu(
        pystray.MenuItem(f"Open ({clean_hk})", on_tray_clicked, default=True),
        pystray.MenuItem("Help", on_tray_clicked),
        pystray.MenuItem("Exit", on_tray_clicked)
    )
    
    icon = pystray.Icon("HebEngConvert", image, "HebEngConvert", menu)
    
    # run_detached() integrates with the OS event loop without requiring the
    # main thread — critical on macOS where Cocoa/AppKit must own the main thread.
    # On Windows it falls back to a regular background thread automatically.
    icon.run_detached()
    
    # Schedule the startup notification via the Tkinter event loop so it fires
    # after the GUI is ready, avoiding a race with the tray initialization.
    if app:
        app.after(1500, lambda: _safe_notify(clean_hk))

def update_hotkey_listener(new_hotkey):
    global hotkey_listener
    if hotkey_listener:
        hotkey_listener.stop()
    
    try:
        if is_mac():
            # Use macOS-specific hotkey listener
            from hotkey_listener_mac import HotkeyListenerMac
            
            # Parse hotkey string into tuple format
            # e.g., "<cmd>+<shift>+d" -> ('<cmd>', '<shift>', 'd')
            hk = new_hotkey.lower().strip()
            modifier_keys = get_modifier_keys()
            for key in modifier_keys:
                if key in hk and f'<{key}>' not in hk:
                    hk = hk.replace(key, f'<{key}>')
            hk = hk.replace(" ", "").replace(",", "+")
            
            # Split into tuple
            hotkey_parts = tuple(hk.split('+'))
            hotkey_listener = HotkeyListenerMac(hotkey_parts, show_clipboard)
            hotkey_listener.start()
        else:
            # Use pynput GlobalHotKeys for Windows/Linux
            hk = new_hotkey.lower().strip()
            modifier_keys = get_modifier_keys()
            for key in modifier_keys:
                if key in hk and f'<{key}>' not in hk:
                    hk = hk.replace(key, f'<{key}>')
            hk = hk.replace(" ", "").replace(",", "+")
            
            hotkey_listener = keyboard.GlobalHotKeys({hk: show_clipboard})
            hotkey_listener.start()
    except Exception as e:
        print(f"Hotkey Error: {e}")

def handle_settings_save(new_hotkey, new_port, use_port):
    global icon
    config = load_config()
    config["hotkey"] = new_hotkey
    config["port"] = new_port
    config["use_port"] = use_port
    save_config(config)
    
    update_hotkey_listener(new_hotkey)
    
    # Update Tray Menu Text
    if icon:
        clean_hk = format_hotkey_display(new_hotkey)
        new_menu = pystray.Menu(
            pystray.MenuItem(f"Open ({clean_hk})", on_tray_clicked, default=True),
            pystray.MenuItem("Help", on_tray_clicked),
            pystray.MenuItem("Exit", on_tray_clicked)
        )
        icon.menu = new_menu

    if app:
        app.current_hotkey = new_hotkey
        app.current_port = new_port
        app.use_port = use_port

def refresh_callback():
    try:
        content = pyperclip.paste()
        if not content:
            content = "[No text found]"
    except Exception as e:
        content = f"Error: {e}"
    if app:
        app.update_content(content)

import socket
import threading

server_socket = None

def check_single_instance(port, use_port):
    if not use_port:
        return True
        
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen(5)
        threading.Thread(target=listen_for_show_signals, args=(server_socket,), daemon=True).start()
        return True
    except socket.error:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', port))
            client.sendall(b"show")
            client.close()
        except (socket.error, ConnectionRefusedError):
            pass
        return False

def listen_for_show_signals(sock):
    while True:
        try:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            if data == b"show":
                show_clipboard()
            conn.close()
        except (socket.error, OSError):
            break

if __name__ == "__main__":
    config = load_config()
    current_hotkey = config.get("hotkey", "<ctrl>+<alt>+d")
    current_port = config.get("port", 54321)
    use_port = config.get("use_port", True)
    
    if not check_single_instance(current_port, use_port):
        sys.exit(0)
        
    app = ClipboardWindow(
        on_refresh_callback=refresh_callback,
        current_hotkey=current_hotkey,
        current_port=current_port,
        use_port=use_port,
        on_settings_save=handle_settings_save
    )
    
    # 2. Start hotkey listener
    update_hotkey_listener(current_hotkey)
    
    # 3. Start tray icon
    setup_tray(current_hotkey)
    
    # 4. Main thread runs the GUI
    app.mainloop()
