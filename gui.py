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

class ClipboardWindow(ctk.CTk):
    def __init__(self, on_refresh_callback=None):
        super().__init__()

        self.title("HebEngConvert")
        self.geometry("300x170")
        self.on_refresh_callback = on_refresh_callback
        
        # Load copy icon
        icon_path = get_resource_path("assets/copy.png")
        self.copy_image = ctk.CTkImage(
            light_image=Image.open(icon_path),
            dark_image=Image.open(icon_path),
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
        self.heb_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 2))
        self.heb_frame.grid_rowconfigure(0, weight=1)
        self.heb_frame.grid_columnconfigure(0, weight=1)

        self.heb_textbox = ctk.CTkTextbox(self.heb_frame, wrap="word", font=("Inter", 15), height=45)
        self.heb_textbox.grid(row=0, column=0, sticky="nsew")
        
        self.heb_copy_btn = ctk.CTkButton(
            self.heb_frame, text="", image=self.copy_image, width=32, height=32,
            fg_color="transparent", hover_color=("#ebebeb", "#2b2b2b"),
            command=lambda: self.copy_to_clip(self.heb_textbox.get("0.0", "end-1c"))
        )
        self.heb_copy_btn.grid(row=0, column=1, padx=(4, 0), sticky="ns")

        # --- English View Section ---
        self.eng_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.eng_frame.grid(row=1, column=0, sticky="nsew", pady=(2, 0))
        self.eng_frame.grid_rowconfigure(0, weight=1)
        self.eng_frame.grid_columnconfigure(0, weight=1)

        self.eng_textbox = ctk.CTkTextbox(self.eng_frame, wrap="word", font=("Inter", 13), height=45)
        self.eng_textbox.grid(row=0, column=0, sticky="nsew")
        
        self.eng_copy_btn = ctk.CTkButton(
            self.eng_frame, text="", image=self.copy_image, width=32, height=32,
            fg_color="transparent", hover_color=("#ebebeb", "#2b2b2b"),
            command=lambda: self.copy_to_clip(self.eng_textbox.get("0.0", "end-1c"))
        )
        self.eng_copy_btn.grid(row=0, column=1, padx=(4, 0), sticky="ns")

        # --- Bottom Control Section ---
        icon_refresh_path = get_resource_path("assets/refresh.png")
        self.refresh_image = ctk.CTkImage(
            light_image=Image.open(icon_refresh_path),
            dark_image=Image.open(icon_refresh_path),
            size=(24, 24)
        )
        
        self.refresh_button = ctk.CTkButton(
            self.main_frame, text="", image=self.refresh_image, 
            command=self.refresh_content, width=32, height=32,
            fg_color="transparent", hover_color=("#ebebeb", "#2b2b2b")
        )
        self.refresh_button.grid(row=2, column=0, pady=(2, 0))
        
        # Close handling (hide instead of destroy)
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.withdraw()

    def copy_to_clip(self, text):
        pyperclip.copy(text)

    def update_content(self, text):
        # Convert text
        heb_text = convert_eng_to_heb(text)
        eng_text = convert_heb_to_eng(text)

        # Update Hebrew textbox
        self.heb_textbox.configure(state="normal")
        self.heb_textbox.delete("0.0", "end")
        self.heb_textbox.insert("0.0", heb_text)
        self.heb_textbox.configure(state="disabled")

        # Update English textbox
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
