import os
import customtkinter as ctk
from icarus_sentinel import style_config, constants

class DashboardView(ctk.CTkScrollableFrame):
    """View for server dashboard and process management."""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.init_widgets()

    def init_widgets(self):
        # Path Selection Frame
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(self.path_frame, text="Install Path:")
        self.path_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        # We keep the entry in app for now as it's heavily accessed by core logic
        # but we link it to the UI
        self.path_entry = ctk.CTkEntry(self.path_frame)
        self.path_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.path_entry.insert(0, self.app.path_entry.get() if hasattr(self.app, "path_entry") else os.path.join(os.getcwd(), constants.DEFAULT_INSTALL_DIR))
        
        # Link back to app
        self.app.path_entry = self.path_entry
        self.app.update_ini_manager()

        self.browse_button = ctk.CTkButton(
            self.path_frame, text="Browse", width=80, command=self.app.browse_path
        )
        self.browse_button.grid(row=0, column=2, padx=(5, 10), pady=10)
        self.app.browse_button = self.browse_button

        # Actions
        self.install_button = ctk.CTkButton(
            self, text="Install/Update Server", command=self.app.start_install
        )
        self.install_button.grid(row=1, column=0, padx=10, pady=5)
        self.app.install_button = self.install_button

        # Metrics Frame (Center)
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.metrics_frame.grid_columnconfigure(0, weight=1)

        # CPU Metrics
        self.cpu_usage_label = ctk.CTkLabel(self.metrics_frame, text="CPU USAGE: 0.0%", font=(style_config.FONT_MAIN[0], 14, "bold"))
        self.cpu_usage_label.grid(row=0, column=0, sticky="w", padx=20)
        self.app.cpu_usage_label = self.cpu_usage_label

        self.cpu_progress_bar = ctk.CTkProgressBar(self.metrics_frame, height=15, progress_color=style_config.ACCENT_COLOR)
        self.cpu_progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 15))
        self.cpu_progress_bar.set(0)
        self.app.cpu_progress_bar = self.cpu_progress_bar

        # RAM Metrics
        self.ram_usage_label = ctk.CTkLabel(self.metrics_frame, text="RAM USAGE: 0.00GB / 0.00GB", font=(style_config.FONT_MAIN[0], 14, "bold"))
        self.ram_usage_label.grid(row=2, column=0, sticky="w", padx=20)
        self.app.ram_usage_label = self.ram_usage_label

        self.ram_progress_bar = ctk.CTkProgressBar(self.metrics_frame, height=15, progress_color=style_config.ACCENT_COLOR)
        self.ram_progress_bar.grid(row=3, column=0, sticky="ew", padx=20, pady=(5, 15))
        self.ram_progress_bar.set(0)
        self.app.ram_progress_bar = self.ram_progress_bar

        # Server Control Frame (Massive Button)
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.grid(row=3, column=0, padx=10, pady=20, sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight=1)

        self.orbital_launch_btn = ctk.CTkButton(
            self.control_frame, 
            text="INITIATE ORBITAL LAUNCH", 
            font=(style_config.FONT_MAIN[0], 24, "bold"),
            height=100,
            fg_color=style_config.ACCENT_COLOR,
            hover_color="#e67e00", # Darker orange
            command=self.app.toggle_server
        )
        self.orbital_launch_btn.grid(row=0, column=0, sticky="ew", padx=100)
        self.app.orbital_launch_btn = self.orbital_launch_btn
        
        # Smart Restart Settings
        self.smart_restart_frame = ctk.CTkFrame(self, corner_radius=style_config.CORNER_RADIUS)
        self.smart_restart_frame.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.smart_restart_var = ctk.BooleanVar(value=self.app.server_manager.smart_restart_enabled)
        self.app.smart_restart_var = self.smart_restart_var

        self.smart_restart_switch = ctk.CTkSwitch(
            self.smart_restart_frame, text="Enable Smart Idle Restart", 
            variable=self.smart_restart_var, command=self.app.save_settings
        )
        self.smart_restart_switch.grid(row=0, column=0, padx=10, pady=10)

        self.restart_time_label = ctk.CTkLabel(self.smart_restart_frame, text="Maintenance Time (HH:MM):")
        self.restart_time_label.grid(row=0, column=1, padx=(10, 5), pady=10)

        self.restart_time_entry = ctk.CTkEntry(self.smart_restart_frame, width=60)
        self.restart_time_entry.grid(row=0, column=2, padx=5, pady=10)
        self.restart_time_entry.insert(0, self.app.server_manager.smart_restart_time)
        self.app.restart_time_entry = self.restart_time_entry

        # Backup Settings
        self.backup_settings_frame = ctk.CTkFrame(self)
        self.backup_settings_frame.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        self.backup_interval_label = ctk.CTkLabel(self.backup_settings_frame, text="Backup Interval (min):")
        self.backup_interval_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.backup_interval_entry = ctk.CTkEntry(self.backup_settings_frame, width=60)
        self.backup_interval_entry.grid(row=0, column=1, padx=5, pady=10)
        self.backup_interval_entry.insert(0, str(int(self.app.backup_manager.interval_minutes)))
        self.app.backup_interval_entry = self.backup_interval_entry

        self.backup_retention_label = ctk.CTkLabel(self.backup_settings_frame, text="Max Backups:")
        self.backup_retention_label.grid(row=0, column=2, padx=(10, 5), pady=10)

        self.backup_retention_entry = ctk.CTkEntry(self.backup_settings_frame, width=60)
        self.backup_retention_entry.grid(row=0, column=3, padx=5, pady=10)
        self.backup_retention_entry.insert(0, str(self.app.backup_manager.retention_limit))
        self.app.backup_retention_entry = self.backup_retention_entry

        # RAM Threshold Frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

        self.threshold_label = ctk.CTkLabel(self.settings_frame, text="RAM Threshold (GB):")
        self.threshold_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.threshold_entry = ctk.CTkEntry(self.settings_frame, width=60)
        self.threshold_entry.grid(row=0, column=1, padx=5, pady=10)
        self.threshold_entry.insert(0, str(self.app.server_manager.ram_threshold_gb))
        self.app.threshold_entry = self.threshold_entry

        self.save_settings_button = ctk.CTkButton(
            self.settings_frame, text="Save Settings", width=100, command=self.app.save_settings
        )
        self.save_settings_button.grid(row=0, column=2, padx=(5, 10), pady=10)
        self.app.save_settings_button = self.save_settings_button
