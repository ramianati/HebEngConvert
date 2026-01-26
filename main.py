import pystray
from PIL import Image
import pyperclip
import threading
from gui import ClipboardWindow
import os
import sys
import time

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
                content = "[Clipboard is empty or contains non-text data]"
        except Exception as e:
            content = f"Error reading clipboard: {e}"
        
        # Use after() to ensure thread safety if called from pystray thread
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
    
    icon = pystray.Icon("HebEngConvert", image, "Clipboard Monitor", menu)
    icon.run()

def refresh_callback():
    """ Called from the GUI refresh button """
    try:
        content = pyperclip.paste()
        if not content:
            content = "[Clipboard is empty or contains non-text data]"
    except Exception as e:
        content = f"Error reading clipboard: {e}"
    
    if app:
        app.update_content(content)

if __name__ == "__main__":
    # 1. Initialize GUI in a way that it starts hidden
    app = ClipboardWindow(on_refresh_callback=refresh_callback)
    
    # 2. Start tray icon in a background thread
    tray_thread = threading.Thread(target=setup_tray, daemon=True)
    tray_thread.start()
    
    # 3. Main thread runs the GUI event loop
    app.mainloop()
