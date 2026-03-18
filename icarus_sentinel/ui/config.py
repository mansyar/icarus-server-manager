import customtkinter as ctk
from icarus_sentinel import constants

class ConfigView(ctk.CTkScrollableFrame):
    """View for server configuration (Basic and Advanced)."""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.init_widgets()

    def init_widgets(self):
        self.config_subtabview = ctk.CTkTabview(self, command=self.app.on_config_tab_change)
        self.config_subtabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.app.config_subtabview = self.config_subtabview

        self.basic_config_tab = self.config_subtabview.add("Basic")
        self.advanced_config_tab = self.config_subtabview.add("Advanced")
        
        self.basic_config_tab.grid_columnconfigure(1, weight=1)
        self.advanced_config_tab.grid_columnconfigure(0, weight=1)
        self.advanced_config_tab.grid_rowconfigure(0, weight=1)

        # Basic Config Fields
        self.config_scroll = ctk.CTkScrollableFrame(self.basic_config_tab)
        self.config_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        self.config_scroll.grid_columnconfigure(1, weight=1)

        # Server Name
        ctk.CTkLabel(self.config_scroll, text="Server Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.server_name_entry = ctk.CTkEntry(self.config_scroll)
        self.server_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.app.server_name_entry = self.server_name_entry

        # Server Password
        ctk.CTkLabel(self.config_scroll, text="Server Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.server_password_entry = ctk.CTkEntry(self.config_scroll, show="*")
        self.server_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.app.server_password_entry = self.server_password_entry

        # Admin Password
        ctk.CTkLabel(self.config_scroll, text="Admin Password/ID:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.admin_password_entry = ctk.CTkEntry(self.config_scroll, show="*")
        self.admin_password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.app.admin_password_entry = self.admin_password_entry

        # Port
        ctk.CTkLabel(self.config_scroll, text="Server Port:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.server_port_entry = ctk.CTkEntry(self.config_scroll)
        self.server_port_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.app.server_port_entry = self.server_port_entry

        # Query Port
        ctk.CTkLabel(self.config_scroll, text="Query Port:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.query_port_entry = ctk.CTkEntry(self.config_scroll)
        self.query_port_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        self.app.query_port_entry = self.query_port_entry

        # Update on Launch
        self.update_on_launch_var = ctk.BooleanVar(value=False)
        self.app.update_on_launch_var = self.update_on_launch_var
        self.update_on_launch_checkbox = ctk.CTkCheckBox(
            self.config_scroll, text="Update on Launch", variable=self.update_on_launch_var
        )
        self.update_on_launch_checkbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Disable Steam Auth (NoSteam)
        self.no_steam_var = ctk.BooleanVar(value=False)
        self.app.no_steam_var = self.no_steam_var
        self.no_steam_checkbox = ctk.CTkCheckBox(
            self.config_scroll, text="Disable Steam Auth (-NOSTEAM)", variable=self.no_steam_var
        )
        self.no_steam_checkbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Save Button
        self.save_config_button = ctk.CTkButton(
            self.config_scroll, text="Save Configuration", command=self.app.save_config
        )
        self.save_config_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20)
        
        # Advanced Config Fields
        self.raw_ini_textbox = ctk.CTkTextbox(self.advanced_config_tab, font=("Consolas", 12))
        self.raw_ini_textbox.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.app.raw_ini_textbox = self.raw_ini_textbox
        
        self.save_advanced_button = ctk.CTkButton(
            self.advanced_config_tab, text="Save Advanced Changes", command=self.app.save_advanced_config
        )
        self.save_advanced_button.grid(row=1, column=0, padx=10, pady=(5, 10))
        
        # Initial populate
        self.app.load_config_to_gui()
