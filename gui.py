import customtkinter as ctk
import pyperclip

class ClipboardWindow(ctk.CTk):
    def __init__(self, on_refresh_callback=None):
        super().__init__()

        self.title("Clipboard Content")
        self.geometry("500x400")
        self.on_refresh_callback = on_refresh_callback
        
        # Configure grid for responsiveness
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Use a TextBox for selectable text
        self.textbox = ctk.CTkTextbox(self.main_frame, wrap="word", font=("Inter", 14))
        self.textbox.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="nsew")
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self.button_frame, 
            text="Refresh", 
            command=self.refresh_content,
            font=("Inter", 13, "bold"),
            height=35
        )
        self.refresh_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        # Convert to Hebrew button
        from converter import convert_eng_to_heb, convert_heb_to_eng
        self.convert_heb_button = ctk.CTkButton(
            self.button_frame,
            text="To Heb",
            command=lambda: self.update_content(convert_eng_to_heb(self.textbox.get("0.0", "end-1c"))),
            fg_color="#1f538d",
            hover_color="#14375e",
            font=("Inter", 13, "bold"),
            height=35
        )
        self.convert_heb_button.grid(row=0, column=1, padx=5, sticky="ew")

        # Convert to English button
        self.convert_eng_button = ctk.CTkButton(
            self.button_frame,
            text="To Eng",
            command=lambda: self.update_content(convert_heb_to_eng(self.textbox.get("0.0", "end-1c"))),
            fg_color="#1f538d",
            hover_color="#14375e",
            font=("Inter", 13, "bold"),
            height=35
        )
        self.convert_eng_button.grid(row=0, column=2, padx=(5, 0), sticky="ew")
        
        # Close handling (hide instead of destroy)
        self.protocol("WM_DELETE_WINDOW", self.hide)
        
        # Initial state: hidden
        self.withdraw()

    def update_content(self, text):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)
        
        # Simple heuristic for RTL alignment
        has_hebrew = any('\u0590' <= c <= '\u05FF' for c in text)
        if has_hebrew:
            self.textbox.configure(font=("Inter", 16)) # Larger font for Hebrew
        else:
            self.textbox.configure(font=("Inter", 14))

        self.textbox.configure(state="disabled")
        
    def refresh_content(self):
        if self.on_refresh_callback:
            self.on_refresh_callback()
        else:
            # Fallback if no callback provided
            try:
                content = pyperclip.paste()
                if not content:
                    content = "[Clipboard is empty or contains non-text data]"
            except Exception as e:
                content = f"Error reading clipboard: {e}"
            self.update_content(content)

    def show(self, text=None):
        if text is not None:
            self.update_content(text)
        self.deiconify()
        self.lift()
        self.focus_force()
        # Bring to front hack for Windows
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

    def hide(self):
        self.withdraw()

if __name__ == "__main__":
    # Test
    app = ClipboardWindow()
    app.show("Sample clipboard text")
    app.mainloop()
