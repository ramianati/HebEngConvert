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
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self.main_frame, 
            text="Refresh Clipboard", 
            command=self.refresh_content,
            font=("Inter", 13, "bold"),
            height=35
        )
        self.refresh_button.grid(row=1, column=0, sticky="ew")
        
        # Close handling (hide instead of destroy)
        self.protocol("WM_DELETE_WINDOW", self.hide)
        
        # Initial state: hidden
        self.withdraw()

    def update_content(self, text):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)
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
