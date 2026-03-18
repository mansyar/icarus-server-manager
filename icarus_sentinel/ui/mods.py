import customtkinter as ctk

class ModsView(ctk.CTkFrame):
    """View for managing server mods."""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        # Header with Install Button
        self.mods_header = ctk.CTkFrame(self, fg_color="transparent")
        self.mods_header.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        self.install_mod_btn = ctk.CTkButton(
            self.mods_header, text="Install Mod (.pak or .zip)", command=self.app.install_mod_ui
        )
        self.install_mod_btn.pack(side="left", padx=10)
        self.app.install_mod_btn = self.install_mod_btn

        self.select_all_var = ctk.BooleanVar(value=False)
        self.app.select_all_var = self.select_all_var
        self.select_all_cb = ctk.CTkCheckBox(
            self.mods_header, text="Select All", variable=self.select_all_var, command=self.app.toggle_select_all_mods
        )
        self.select_all_cb.pack(side="left", padx=20)
        self.app.select_all_cb = self.select_all_cb

        self.refresh_mods_btn = ctk.CTkButton(
            self.mods_header, text="Refresh", width=80, command=self.app.refresh_mod_list
        )
        self.refresh_mods_btn.pack(side="right", padx=10)
        self.app.refresh_mods_btn = self.refresh_mods_btn

        # Mod List (Scrollable Checklist)
        self.mod_list = ctk.CTkScrollableFrame(self, label_text="Installed Mods")
        self.mod_list.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.app.mod_list = self.mod_list
        
        # Action Buttons for selected mods
        self.mod_actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mod_actions_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.remove_mod_btn = ctk.CTkButton(
            self.mod_actions_frame, text="Remove Selected Mods", fg_color="red", hover_color="darkred",
            command=self.app.remove_mod_ui
        )
        self.remove_mod_btn.pack(side="left", padx=10)
        self.app.remove_mod_btn = self.remove_mod_btn

        # Sync Warning
        self.sync_warning_label = ctk.CTkLabel(
            self, 
            text="WARNING: Clients MUST have the exact same .pak files to join without crashing.",
            text_color="orange",
            font=("Arial", 12, "bold")
        )
        self.sync_warning_label.grid(row=3, column=0, padx=20, pady=10)
        self.app.sync_warning_label = self.sync_warning_label

        self.app.refresh_mod_list()
