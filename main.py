import pystray
from PIL import Image
import pyperclip
import threading
from gui import ClipboardWindow
import os
import sys
import time

from pynput import keyboard

# Global app instance for single-instance control
app = None
icon = None

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
        
        # Use after() to ensure thread safety if called from background threads
        app.after(0, lambda: app.show(content))

def exit_app():
    global icon, app
    if icon:
        icon.stop()
    if app:
        app.quit()
    sys.exit(0)

def setup_tray():
    global icon
    icon_path = get_resource_path("assets/clipboard.png")
    image = Image.open(icon_path)
    
    menu = pystray.Menu(
        pystray.MenuItem("Open", on_tray_clicked, default=True),
        pystray.MenuItem("Exit", on_tray_clicked)
    )
    
    icon = pystray.Icon("HebEngConvert", image, "HebEngConvert", menu)
    icon.run()

def setup_hotkey():
    """ Setup global hotkey Ctrl+Alt+D """
    # Hotkey definition: <ctrl>+<alt>+d
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+d': show_clipboard
    }) as h:
        h.join()

def refresh_callback():
    """ Called from the GUI refresh button """
    try:
        content = pyperclip.paste()
        if not content:
            content = "[No text found]"
    except Exception as e:
        content = f"Error: {e}"
    
    if app:
        app.update_content(content)

if __name__ == "__main__":
    # 1. Initialize GUI
    app = ClipboardWindow(on_refresh_callback=refresh_callback)
    
    # 2. Start hotkey listener in background
    threading.Thread(target=setup_hotkey, daemon=True).start()
    
    # 3. Start tray icon in background
    threading.Thread(target=setup_tray, daemon=True).start()
    
    # 4. Main thread runs the GUI
    app.mainloop()
