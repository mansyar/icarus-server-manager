import customtkinter as ctk
from typing import Callable
from icarus_sentinel import style_config

class RamOptimizationDialog(ctk.CTkToplevel):
    """Dialog shown when system RAM is low before server launch."""

    def __init__(self, parent, available_pct: float, on_confirm: Callable):
        super().__init__(parent)
        self.title("System Resource Warning")
        self.geometry("400x300")
        self.on_confirm = on_confirm
        
        self.label = ctk.CTkLabel(
            self, 
            text=(
                f"CRITICAL: Low System RAM detected!\n"
                f"Only {available_pct}% available."
            ),
            text_color="red",
            font=(style_config.FONT_MAIN[0], 16, "bold")
        )
        self.label.pack(padx=20, pady=20)

        self.info_text = ctk.CTkTextbox(self, width=350, height=100, fg_color=style_config.CONSOLE_BG, text_color=style_config.CONSOLE_TEXT)
        self.info_text.pack(padx=20, pady=10)
        self.info_text.insert(
            "0.0", 
            "Recommendations:\n"
            "- Close memory-heavy applications (Chrome, etc.)\n"
            "- Consider restarting your computer.\n"
            "- Launching now may cause server instability or crashes."
        )
        self.info_text.configure(state="disabled")

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(padx=20, pady=20, fill="x")

        self.launch_anyway_btn = ctk.CTkButton(
            self.btn_frame, text="Launch Anyway", fg_color=style_config.ACCENT_COLOR, command=self.confirm
        )
        self.launch_anyway_btn.pack(side="left", padx=10, expand=True)

        self.cancel_btn = ctk.CTkButton(
            self.btn_frame, text="Cancel", fg_color="gray", command=self.destroy
        )
        self.cancel_btn.pack(side="right", padx=10, expand=True)

        # Make modal
        self.grab_set()

    def confirm(self):
        self.on_confirm()
        self.destroy()
