import customtkinter as ctk
import pyperclip
import os
import sys
from PIL import Image
from converter import convert_eng_to_heb, convert_heb_to_eng

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, current_hotkey, current_port, use_port, on_save_callback):
        super().__init__(parent)
        self.title("HebEngConvert")
        self.geometry("380x280")
        self.on_save_callback = on_save_callback
        self.is_capturing = False
        self.captured_keys = set()
        
        # Center the dialog
        self.after(10, self._center_window)
        
        # UI Elements
        title_font = ("Inter", 16, "bold")
        label_font = ("Inter", 12, "bold")
        info_font = ("Inter", 11)
        
        # App Info
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(padx=20, pady=(15, 5), fill="x")
        
        ctk.CTkLabel(self.info_frame, text="HebEngConvert", font=title_font).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self.info_frame, text=f"v1.0.2", font=info_font).grid(row=0, column=1, sticky="w", padx=10)
        
        folder_text = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
        folder_label = ctk.CTkLabel(self, text=folder_text, font=("Inter", 9), wraplength=340, justify="left")
        folder_label.pack(padx=20, pady=(0, 10), anchor="w")

        # Hotkey Change Area
        self.hotkey_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.hotkey_frame.pack(padx=20, pady=5, fill="x")
        
        ctk.CTkLabel(self.hotkey_frame, text="Hotkey:", font=label_font).grid(row=0, column=0, sticky="w")
        self.hotkey_entry = ctk.CTkEntry(self.hotkey_frame, width=140)
        clean_hotkey = current_hotkey.replace("<", "").replace(">", "")
        self.hotkey_entry.insert(0, clean_hotkey)
        self.hotkey_entry.grid(row=0, column=1, padx=10, sticky="w")
        
        self.capture_btn = ctk.CTkButton(self.hotkey_frame, text="Capture", width=70, command=self._toggle_capture)
        self.capture_btn.grid(row=0, column=2, padx=5)

        # Port Change Area
        self.port_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.port_frame.pack(padx=20, pady=5, fill="x")
        
        self.port_check = ctk.CTkCheckBox(self.port_frame, text="Enable single instance port:", font=label_font, width=20)
        if use_port:
            self.port_check.select()
        self.port_check.grid(row=0, column=0, sticky="w")
        
        self.port_entry = ctk.CTkEntry(self.port_frame, width=80)
        self.port_entry.insert(0, str(current_port))
        self.port_entry.grid(row=0, column=1, padx=10, sticky="w")

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", font=("Inter", 10, "italic"), text_color="gray")
        self.status_label.pack(pady=(0, 5))
        
        # Save Button
        self.save_btn = ctk.CTkButton(self, text="Save Settings", command=self._save)
        self.save_btn.pack(pady=(5, 15))
        
        self.attributes('-topmost', True)
        self.grab_set()

    def _toggle_capture(self):
        from pynput import keyboard
        if not self.is_capturing:
            self.is_capturing = True
            self.captured_keys = set()
            self.capture_btn.configure(text="Recording", fg_color="#d32f2f")
            self.status_label.configure(text="Press your keys...")
            self.hotkey_entry.delete(0, "end")
            self.listener = keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release)
            self.listener.start()
        else:
            self._stop_capture()

    def _on_key_press(self, key):
        from pynput import keyboard
        if not self.is_capturing: return
        
        k_str = ""
        if hasattr(key, 'vk') and 65 <= key.vk <= 90:
            k_str = chr(key.vk).lower()
        elif hasattr(key, 'char') and key.char:
            k_str = key.char.lower()
        elif hasattr(key, 'name'):
            name = key.name.split('_')[0].lower()
            if name in ['ctrl', 'alt', 'shift', 'win', 'cmd']:
                k_str = name 
        else:
            k_str = str(key).replace("Key.", "").split('_l')[0].split('_r')[0]
        
        if k_str:
            self.captured_keys.add(k_str)
            mods_list = [k for k in self.captured_keys if k in ['ctrl', 'alt', 'shift', 'win', 'cmd']]
            others = sorted([k for k in self.captured_keys if k not in mods_list])
            current_str = "+".join(sorted(mods_list) + others)
            self.hotkey_entry.delete(0, "end")
            self.hotkey_entry.insert(0, current_str)

    def _on_key_release(self, key):
        if not self.is_capturing: return
        has_non_mod = any(k not in ['ctrl', 'alt', 'shift', 'win', 'cmd'] for k in self.captured_keys)
        if has_non_mod:
            self.after(600, self._stop_capture)

    def _stop_capture(self):
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.is_capturing = False
        self.capture_btn.configure(text="Capture", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.status_label.configure(text="Capture finished.")

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _save(self):
        new_hotkey_raw = self.hotkey_entry.get().strip().lower()
        new_port = self.port_entry.get().strip()
        use_port = bool(self.port_check.get())
        
        if new_hotkey_raw and new_port:
            try:
                port_int = int(new_port)
                save_hk = new_hotkey_raw
                for key in ['ctrl', 'alt', 'shift', 'win', 'cmd']:
                    if key in save_hk and f'<{key}>' not in save_hk:
                        save_hk = save_hk.replace(key, f'<{key}>')
                
                self.on_save_callback(save_hk, port_int, use_port)
                self.destroy()
            except ValueError:
                self.status_label.configure(text="Error: Port must be a number", text_color="red")

class ClipboardWindow(ctk.CTk):
    def __init__(self, on_refresh_callback=None, current_hotkey="ctrl+alt+d", current_port=54321, use_port=True, on_settings_save=None):
        super().__init__()

        self.title("HebEngConvert")
        self.geometry("300x220")
        self.on_refresh_callback = on_refresh_callback
        self.current_hotkey = current_hotkey
        self.current_port = current_port
        self.use_port = use_port
        self.on_settings_save = on_settings_save
        
        # Load images
        icon_path = get_resource_path("assets/copy.png")
        self.copy_image = ctk.CTkImage(
            light_image=Image.open(icon_path),
            dark_image=Image.open(icon_path),
            size=(48, 48)
        )
        
        icon_refresh_path = get_resource_path("assets/refresh.png")
        self.refresh_image = ctk.CTkImage(
            light_image=Image.open(icon_refresh_path),
            dark_image=Image.open(icon_refresh_path),
            size=(24, 24)
        )
        
        icon_settings_path = get_resource_path("assets/settings.png")
        self.settings_image = ctk.CTkImage(
            light_image=Image.open(icon_settings_path),
            dark_image=Image.open(icon_settings_path),
            size=(24, 24)
        )
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        self.main_frame.grid_rowconfigure((0, 1), weight=1) 
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- Hebrew View Section ---
        self.heb_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.heb_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        self.heb_frame.grid_rowconfigure(0, weight=1)
        self.heb_frame.grid_columnconfigure(0, weight=1)

        self.heb_textbox = ctk.CTkTextbox(self.heb_frame, wrap="word", font=("Inter", 15), height=60)
        self.heb_textbox.grid(row=0, column=0, sticky="nsew")
        
        self.heb_copy_btn = ctk.CTkButton(
            self.heb_frame, text="", image=self.copy_image, width=56, height=56,
            fg_color=("#f0f0f0", "#333333"), hover_color=("#e5e5e5", "#404040"),
            corner_radius=8,
            command=lambda: self.copy_to_clip(self.heb_textbox.get("0.0", "end-1c"))
        )
        self.heb_copy_btn.grid(row=0, column=1, padx=(6, 0), sticky="ns")

        # --- English View Section ---
        self.eng_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.eng_frame.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        self.eng_frame.grid_rowconfigure(0, weight=1)
        self.eng_frame.grid_columnconfigure(0, weight=1)

        self.eng_textbox = ctk.CTkTextbox(self.eng_frame, wrap="word", font=("Inter", 13), height=60)
        self.eng_textbox.grid(row=0, column=0, sticky="nsew")
        
        self.eng_copy_btn = ctk.CTkButton(
            self.eng_frame, text="", image=self.copy_image, width=56, height=56,
            fg_color=("#f0f0f0", "#333333"), hover_color=("#e5e5e5", "#404040"),
            corner_radius=8,
            command=lambda: self.copy_to_clip(self.eng_textbox.get("0.0", "end-1c"))
        )
        self.eng_copy_btn.grid(row=0, column=1, padx=(6, 0), sticky="ns")

        # --- Bottom Control Section ---
        self.control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.control_frame.grid(row=2, column=0, pady=(6, 0), sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1), weight=1)

        self.refresh_button = ctk.CTkButton(
            self.control_frame, text="", image=self.refresh_image, 
            command=self.refresh_content, width=40, height=40,
            fg_color=("#f0f0f0", "#333333"), hover_color=("#e5e5e5", "#404040"),
            corner_radius=8
        )
        self.refresh_button.grid(row=0, column=0, sticky="e", padx=4)
        
        self.settings_button = ctk.CTkButton(
            self.control_frame, text="", image=self.settings_image, 
            command=self.open_settings, width=40, height=40,
            fg_color=("#f0f0f0", "#333333"), hover_color=("#e5e5e5", "#404040"),
            corner_radius=8
        )
        self.settings_button.grid(row=0, column=1, sticky="w", padx=4)
        
        # Close handling
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.withdraw()

    def open_settings(self):
        SettingsDialog(self, self.current_hotkey, self.current_port, self.use_port, self._on_settings_applied)

    def _on_settings_applied(self, new_hotkey, new_port):
        self.current_hotkey = new_hotkey
        self.current_port = new_port
        if self.on_settings_save:
            self.on_settings_save(new_hotkey, new_port)

    def copy_to_clip(self, text):
        pyperclip.copy(text)

    def update_content(self, text):
        heb_text = convert_eng_to_heb(text)
        eng_text = convert_heb_to_eng(text)

        self.heb_textbox.configure(state="normal")
        self.heb_textbox.delete("0.0", "end")
        self.heb_textbox.insert("0.0", heb_text)
        self.heb_textbox.configure(state="disabled")

        self.eng_textbox.configure(state="normal")
        self.eng_textbox.delete("0.0", "end")
        self.eng_textbox.insert("0.0", eng_text)
        self.eng_textbox.configure(state="disabled")
        
    def refresh_content(self):
        if self.on_refresh_callback:
            self.on_refresh_callback()
        else:
            try:
                content = pyperclip.paste()
                if not content:
                    content = "[No text found]"
            except Exception as e:
                content = f"Error: {e}"
            self.update_content(content)

    def show(self, text=None):
        if text is not None:
            self.update_content(text)
        self.deiconify()
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

    def hide(self):
        self.withdraw()

if __name__ == "__main__":
    app = ClipboardWindow()
    app.show("Sample text qwrty אקערטי")
    app.mainloop()
