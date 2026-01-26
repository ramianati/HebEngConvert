import pystray
from PIL import Image
import pyperclip
import threading
from gui import ClipboardWindow
import os
import sys
import time

from pynput import keyboard

import json
from pynput import keyboard

# Global app instance for single-instance control
app = None
icon = None
hotkey_listener = None
config_path = os.path.join(os.path.expanduser("~"), ".hebengconvert.json")

def load_config():
    default_config = {"hotkey": "<ctrl>+<alt>+d", "port": 54321}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return {**default_config, **json.load(f)}
        except:
            pass
    return default_config

def save_config(config):
    try:
        with open(config_path, "w") as f:
            json.dump(config, f)
    except:
        pass

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def on_tray_clicked(icon, item):
    if str(item) == "Open":
        show_clipboard()
    elif str(item) == "Exit":
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

def exit_app():
    global icon, app, hotkey_listener
    if hotkey_listener:
        hotkey_listener.stop()
    if icon:
        icon.stop()
    if app:
        app.quit()
    sys.exit(0)

def setup_tray(hotkey_str):
    global icon
    icon_path = get_resource_path("assets/clipboard.png")
    image = Image.open(icon_path)
    
    menu = pystray.Menu(
        pystray.MenuItem("Open", on_tray_clicked, default=True),
        pystray.MenuItem("Exit", on_tray_clicked)
    )
    
    icon = pystray.Icon("HebEngConvert", image, "HebEngConvert", menu)
    
    threading.Thread(target=icon.run, daemon=True).start()
    
    # Startup notification with Clean Hotkey (No <>)
    display_hk = hotkey_str.replace("<", "").replace(">", "").upper()
    time.sleep(1.5)
    icon.notify(f"Press {display_hk} to open.", "HebEngConvert is Ready")

def update_hotkey_listener(new_hotkey):
    global hotkey_listener
    if hotkey_listener:
        hotkey_listener.stop()
    
    try:
        hk = new_hotkey.lower().strip()
        for key in ['ctrl', 'alt', 'shift', 'win', 'cmd']:
            if key in hk and f'<{key}>' not in hk:
                hk = hk.replace(key, f'<{key}>')
        hk = hk.replace(" ", "").replace(",", "+")
        
        hotkey_listener = keyboard.GlobalHotKeys({hk: show_clipboard})
        hotkey_listener.start()
    except Exception as e:
        print(f"Hotkey Error: {e}")

def handle_settings_save(new_hotkey, new_port):
    # Update config
    config = load_config()
    config["hotkey"] = new_hotkey
    config["port"] = new_port
    save_config(config)
    
    # Update hotkey listener on the fly
    update_hotkey_listener(new_hotkey)
    
    # Note: Port changes require restart to take effect on the socket
    # But we update the internal state for consistency
    if app:
        app.current_hotkey = new_hotkey
        app.current_port = new_port

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

# Single Instance Globals
server_socket = None

def check_single_instance(port):
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Using SO_REUSEADDR isn't standard on Windows, just bind
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
        except:
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
        except:
            break

if __name__ == "__main__":
    config = load_config()
    current_hotkey = config.get("hotkey", "<ctrl>+<alt>+d")
    current_port = config.get("port", 54321)
    
    if not check_single_instance(current_port):
        sys.exit(0)
        
    # 1. Initialize GUI
    app = ClipboardWindow(
        on_refresh_callback=refresh_callback,
        current_hotkey=current_hotkey,
        current_port=current_port,
        on_settings_save=handle_settings_save
    )
    
    # 2. Start hotkey listener
    update_hotkey_listener(current_hotkey)
    
    # 3. Start tray icon
    setup_tray(current_hotkey)
    
    # 4. Main thread runs the GUI
    app.mainloop()
