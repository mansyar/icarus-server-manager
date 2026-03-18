import os
import customtkinter as ctk

class BackupsView(ctk.CTkFrame):
    """View for managing server backups."""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.backup_now_button = ctk.CTkButton(
            self, text="Backup Now", command=self.app.manual_backup
        )
        self.backup_now_button.grid(row=0, column=0, padx=20, pady=20)
        self.app.backup_now_button = self.backup_now_button

        self.backups_list_frame = ctk.CTkScrollableFrame(self, label_text="Available Backups")
        self.backups_list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.app.backups_list_frame = self.backups_list_frame

        # Initial refresh
        self.app.refresh_backups_list()
