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
    default_config = {"hotkey": "<ctrl>+<alt>+d"}
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
    
    # Run in thread so notification doesn't block
    threading.Thread(target=icon.run, daemon=True).start()
    
    # Startup notification with Hotkey
    time.sleep(1.5) # Wait for icon to initialize
    icon.notify(f"Press {hotkey_str} to open.", "HebEngConvert is Ready")

def update_hotkey_listener(new_hotkey):
    global hotkey_listener
    if hotkey_listener:
        hotkey_listener.stop()
    
    try:
        # Standardize format for GlobalHotKeys
        hk = new_hotkey.lower().strip()
        # Ensure pynput notation: ctrl -> <ctrl>
        for key in ['ctrl', 'alt', 'shift', 'win', 'cmd']:
            if key in hk and f'<{key}>' not in hk:
                hk = hk.replace(key, f'<{key}>')
        # Replace spaces or commas with +
        hk = hk.replace(" ", "").replace(",", "+")
        
        hotkey_listener = keyboard.GlobalHotKeys({hk: show_clipboard})
        hotkey_listener.start()
        
        # PERSIST: Update config file immediately
        config = load_config()
        config["hotkey"] = new_hotkey
        save_config(config)
    except Exception as e:
        print(f"Hotkey Error: {e}")

def refresh_callback():
    try:
        content = pyperclip.paste()
        if not content:
            content = "[No text found]"
    except Exception as e:
        content = f"Error: {e}"
    if app:
        app.update_content(content)

if __name__ == "__main__":
    config = load_config()
    current_hotkey = config.get("hotkey", "<ctrl>+<alt>+d")
    
    # 1. Initialize GUI
    app = ClipboardWindow(
        on_refresh_callback=refresh_callback,
        current_hotkey=current_hotkey,
        on_hotkey_save=update_hotkey_listener
    )
    
    # 2. Start hotkey listener
    update_hotkey_listener(current_hotkey)
    
    # 3. Start tray icon with active hotkey info
    setup_tray(current_hotkey)
    
    # 4. Main thread runs the GUI
    app.mainloop()
