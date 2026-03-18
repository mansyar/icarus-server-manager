import customtkinter as ctk

class SaveSyncView(ctk.CTkFrame):
    """View for manual save synchronization."""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.sync_frame = ctk.CTkFrame(self)
        self.sync_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.sync_frame.grid_columnconfigure(1, weight=1)

        # SteamID Selection
        ctk.CTkLabel(self.sync_frame, text="Local SteamID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.steam_id_dropdown = ctk.CTkOptionMenu(
            self.sync_frame, 
            values=["None Found"], 
            command=self.app.on_steam_id_selected
        )
        self.steam_id_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.app.steam_id_dropdown = self.steam_id_dropdown

        # Sync Button
        self.manual_sync_btn = ctk.CTkButton(
            self.sync_frame, text="Sync Now", command=self.app.perform_manual_sync
        )
        self.manual_sync_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=20)
        self.app.manual_sync_btn = self.manual_sync_btn

        # Last Sync Info
        self.last_sync_label = ctk.CTkLabel(
            self.sync_frame, 
            text=f"Last Sync: {self.app.server_manager.state.get('last_sync_timestamp', 'Never')}"
        )
        self.last_sync_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.app.last_sync_label = self.last_sync_label

        self.app.refresh_steam_ids()
