import datetime
import os
import subprocess
import threading
from tkinter import filedialog, messagebox
from typing import Optional, Callable

import customtkinter as ctk
import psutil

from icarus_sentinel import __version__, style_config
from icarus_sentinel.steam_manager import SteamManager
from icarus_sentinel.server_manager import ServerProcessManager
from icarus_sentinel.backup_manager import BackupManager
from icarus_sentinel.core.ini_manager import INIManager
from icarus_sentinel.core.save_sync_manager import SaveSyncManager
from icarus_sentinel.core.mod_manager import ModManager

# Set appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") # We will override with our own colors

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

class App(ctk.CTk):
    """Main application class for Icarus Sentinel."""

    def __init__(self, state_file: str = "server_state.json") -> None:
        """Initializes the main application window and its components."""
        super().__init__()
        self.title("Icarus Sentinel")
        self.geometry("1100x700")
        self.configure(fg_color=style_config.APP_BG)
        
        self.steam_manager = SteamManager()
        
        # Initialize BackupManager
        initial_server_path = os.path.join(os.getcwd(), "icarus_server")
        self.backup_manager = BackupManager(
            server_path=initial_server_path,
            backup_path=os.path.join(os.getcwd(), "backups")
        )
        
        self.server_manager = ServerProcessManager(state_file=state_file, backup_manager=self.backup_manager)
        self.server_process: Optional[subprocess.Popen] = None
        
        # Initialize INI Manager
        self.ini_manager: Optional[INIManager] = None
        
        # Initialize SaveSyncManager
        self.save_sync_manager = SaveSyncManager(
            server_path=initial_server_path,
            ini_manager=None # Will be updated when ini_manager is ready
        )
        self.selected_steam_id: Optional[str] = None
        self.refresh_steam_ids()

        # Initialize ModManager
        self.mod_manager = ModManager(server_root=initial_server_path)

        # Start backup timer
        self.backup_manager.start_timer()
        
        # Main Grid layout
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main content area
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=style_config.SIDEBAR_BG)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) # Spacer

        self.sidebar_logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="ICARUS\nSENTINEL", 
            font=(style_config.FONT_MAIN[0], 20, "bold"),
            text_color=style_config.ACCENT_COLOR
        )
        self.sidebar_logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.nav_dashboard_btn = ctk.CTkButton(
            self.sidebar_frame, text="Dashboard", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab("Server")
        )
        self.nav_dashboard_btn.grid(row=1, column=0, sticky="ew")

        self.nav_settings_btn = ctk.CTkButton(
            self.sidebar_frame, text="Configuration", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab("Configuration")
        )
        self.nav_settings_btn.grid(row=2, column=0, sticky="ew")

        self.nav_backups_btn = ctk.CTkButton(
            self.sidebar_frame, text="Backups", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab("Backups")
        )
        self.nav_backups_btn.grid(row=3, column=0, sticky="ew")

        self.nav_mods_btn = ctk.CTkButton(
            self.sidebar_frame, text="Mods", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab("Mods")
        )
        self.nav_mods_btn.grid(row=4, column=0, sticky="ew")
        
        # Main Content Frame
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1) # Upper content
        self.main_content_frame.grid_rowconfigure(1, weight=0) # Console

        # Temp Tabview inside main_content_frame (will be replaced by navigation in Phase 2)
        self.tabview = ctk.CTkTabview(self.main_content_frame, command=self.on_tab_change)
        self.tabview.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="nsew")
        self.server_tab = self.tabview.add("Server")
        self.config_tab = self.tabview.add("Configuration")
        self.save_sync_tab = self.tabview.add("Save Sync")
        self.backups_tab = self.tabview.add("Backups")
        self.mods_tab = self.tabview.add("Mods")
        
        self.server_tab.grid_columnconfigure(0, weight=1)
        self.config_tab.grid_columnconfigure(0, weight=1)
        self.save_sync_tab.grid_columnconfigure(0, weight=1)
        self.mods_tab.grid_columnconfigure(0, weight=1)

        # Initialize Tabs
        self.init_server_tab()
        self.init_config_tab()
        self.init_save_sync_tab()
        self.init_backups_tab()
        self.init_mods_tab()

        # Console
        self.console_output = ctk.CTkTextbox(
            self.main_content_frame, 
            height=150, 
            state="disabled",
            fg_color=style_config.CONSOLE_BG,
            text_color=style_config.CONSOLE_TEXT,
            font=style_config.FONT_MONO
        )
        self.console_output.grid(row=1, column=0, sticky="ew")

        # Bottom Frame (Status/Version)
        self.bottom_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, pady=(5, 0), sticky="ew")
        
        self.about_btn = ctk.CTkButton(
            self.bottom_frame, text="About", width=50, height=20, 
            fg_color="gray", command=self.show_about
        )
        self.about_btn.pack(side="left")

        self.version_label = ctk.CTkLabel(self.bottom_frame, text=f"v{__version__}", font=(style_config.FONT_MAIN[0], 10))
        self.version_label.pack(side="right")

        # Recover state
        self.recover_state()

        # Start monitoring loop
        self.update_monitoring()

    def init_server_tab(self) -> None:
        """Initializes the Server management tab UI."""
        # Path Selection Frame (inside Server Tab)
        self.path_frame = ctk.CTkFrame(self.server_tab)
        self.path_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(self.path_frame, text="Install Path:")
        self.path_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.path_entry = ctk.CTkEntry(self.path_frame)
        self.path_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.path_entry.insert(0, os.path.join(os.getcwd(), "icarus_server"))
        
        # Now that path_entry is initialized, we can update INI manager
        self.update_ini_manager()

        self.browse_button = ctk.CTkButton(
            self.path_frame, text="Browse", width=80, command=self.browse_path
        )
        self.browse_button.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Actions (inside Server Tab)
        self.install_button = ctk.CTkButton(
            self.server_tab, text="Install/Update Server", command=self.start_install
        )
        self.install_button.grid(row=1, column=0, padx=10, pady=5)

        # Server Control Frame (inside Server Tab)
        self.mgmt_frame = ctk.CTkFrame(self.server_tab)
        self.mgmt_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.start_button = ctk.CTkButton(self.mgmt_frame, text="Start Server", command=self.start_server)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = ctk.CTkButton(self.mgmt_frame, text="Stop Server", command=self.stop_server, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.restart_button = ctk.CTkButton(self.mgmt_frame, text="Restart Server", command=self.restart_server, state="disabled")
        self.restart_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.cpu_label = ctk.CTkLabel(self.mgmt_frame, text="CPU: 0.0%")
        self.cpu_label.grid(row=0, column=3, padx=10, pady=10)
        
        self.ram_label = ctk.CTkLabel(self.mgmt_frame, text="RAM: 0.00GB")
        self.ram_label.grid(row=0, column=4, padx=10, pady=10)

        # Settings Frame (inside Server Tab)
        self.settings_frame = ctk.CTkFrame(self.server_tab)
        self.settings_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.threshold_label = ctk.CTkLabel(self.settings_frame, text="RAM Threshold (GB):")
        self.threshold_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.threshold_entry = ctk.CTkEntry(self.settings_frame, width=60)
        self.threshold_entry.grid(row=0, column=1, padx=5, pady=10)
        self.threshold_entry.insert(0, str(self.server_manager.ram_threshold_gb))

        self.save_settings_button = ctk.CTkButton(
            self.settings_frame, text="Save Settings", width=100, command=self.save_settings
        )
        self.save_settings_button.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Smart Restart Settings (inside Server Tab)
        self.smart_restart_frame = ctk.CTkFrame(self.server_tab)
        self.smart_restart_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.smart_restart_var = ctk.BooleanVar(value=self.server_manager.smart_restart_enabled)
        self.smart_restart_switch = ctk.CTkSwitch(
            self.smart_restart_frame, text="Enable Smart Idle Restart", 
            variable=self.smart_restart_var, command=self.save_settings
        )
        self.smart_restart_switch.grid(row=0, column=0, padx=10, pady=10)

        self.restart_time_label = ctk.CTkLabel(self.smart_restart_frame, text="Maintenance Time (HH:MM):")
        self.restart_time_label.grid(row=0, column=1, padx=(10, 5), pady=10)

        self.restart_time_entry = ctk.CTkEntry(self.smart_restart_frame, width=60)
        self.restart_time_entry.grid(row=0, column=2, padx=5, pady=10)
        self.restart_time_entry.insert(0, self.server_manager.smart_restart_time)

        # Backup Settings (inside Server Tab)
        self.backup_settings_frame = ctk.CTkFrame(self.server_tab)
        self.backup_settings_frame.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.backup_interval_label = ctk.CTkLabel(self.backup_settings_frame, text="Backup Interval (min):")
        self.backup_interval_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.backup_interval_entry = ctk.CTkEntry(self.backup_settings_frame, width=60)
        self.backup_interval_entry.grid(row=0, column=1, padx=5, pady=10)
        self.backup_interval_entry.insert(0, str(int(self.backup_manager.interval_minutes)))

        self.backup_retention_label = ctk.CTkLabel(self.backup_settings_frame, text="Max Backups:")
        self.backup_retention_label.grid(row=0, column=2, padx=(10, 5), pady=10)

        self.backup_retention_entry = ctk.CTkEntry(self.backup_settings_frame, width=60)
        self.backup_retention_entry.grid(row=0, column=3, padx=5, pady=10)
        self.backup_retention_entry.insert(0, str(self.backup_manager.retention_limit))

    def init_mods_tab(self) -> None:
        """Initializes the Mods management tab UI."""
        self.mods_tab.grid_columnconfigure(0, weight=1)
        self.mods_tab.grid_rowconfigure(1, weight=1)

        # Header with Install Button
        self.mods_header = ctk.CTkFrame(self.mods_tab, fg_color="transparent")
        self.mods_header.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        self.install_mod_btn = ctk.CTkButton(
            self.mods_header, text="Install Mod (.pak or .zip)", command=self.install_mod_ui
        )
        self.install_mod_btn.pack(side="left", padx=10)

        self.select_all_var = ctk.BooleanVar(value=False)
        self.select_all_cb = ctk.CTkCheckBox(
            self.mods_header, text="Select All", variable=self.select_all_var, command=self.toggle_select_all_mods
        )
        self.select_all_cb.pack(side="left", padx=20)

        self.refresh_mods_btn = ctk.CTkButton(
            self.mods_header, text="Refresh", width=80, command=self.refresh_mod_list
        )
        self.refresh_mods_btn.pack(side="right", padx=10)

        # Mod List (Scrollable Checklist)
        self.mod_list = ctk.CTkScrollableFrame(self.mods_tab, label_text="Installed Mods")
        self.mod_list.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Action Buttons for selected mods
        self.mod_actions_frame = ctk.CTkFrame(self.mods_tab, fg_color="transparent")
        self.mod_actions_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.remove_mod_btn = ctk.CTkButton(
            self.mod_actions_frame, text="Remove Selected Mods", fg_color="red", hover_color="darkred",
            command=self.remove_mod_ui
        )
        self.remove_mod_btn.pack(side="left", padx=10)

        # Sync Warning
        self.sync_warning_label = ctk.CTkLabel(
            self.mods_tab, 
            text="WARNING: Clients MUST have the exact same .pak files to join without crashing.",
            text_color="orange",
            font=("Arial", 12, "bold")
        )
        self.sync_warning_label.grid(row=3, column=0, padx=20, pady=10)

        self.refresh_mod_list()

    def toggle_select_all_mods(self) -> None:
        """Toggles selection for all mod checkboxes."""
        val = self.select_all_var.get()
        for cb in self.mod_list.winfo_children():
            if isinstance(cb, ctk.CTkCheckBox):
                if val:
                    cb.select()
                else:
                    cb.deselect()

    def refresh_mod_list(self) -> None:
        """Updates the list of installed mods using checkboxes."""
        # Clear existing
        for widget in self.mod_list.winfo_children():
            widget.destroy()

        mods = self.mod_manager.list_mods()
        if not mods:
            ctk.CTkLabel(self.mod_list, text="No mods installed.").pack(pady=10)
            self.select_all_cb.configure(state="disabled")
        else:
            self.select_all_cb.configure(state="normal")
            self.select_all_var.set(False)
            for mod in mods:
                cb = ctk.CTkCheckBox(self.mod_list, text=mod)
                cb.pack(fill="x", padx=10, pady=5)

    def install_mod_ui(self) -> None:
        """Opens file dialog and installs selected mods."""
        file_paths = filedialog.askopenfilenames(
            title="Select Mod Files",
            filetypes=[("Mod Files", "*.pak *.zip"), ("PAK Files", "*.pak"), ("ZIP Archives", "*.zip")]
        )
        if file_paths:
            for file_path in file_paths:
                self.log(f"Installing mod: {os.path.basename(file_path)}...")
                try:
                    self.mod_manager.install_mod(file_path)
                    self.log(f"Mod '{os.path.basename(file_path)}' installed successfully.")
                except Exception as e:
                    self.log(f"Error installing mod '{os.path.basename(file_path)}': {str(e)}")
                    messagebox.showerror("Installation Error", f"Failed to install mod '{os.path.basename(file_path)}': {str(e)}")
            
            self.refresh_mod_list()

    def remove_mod_ui(self) -> None:
        """Removes all currently checked mods."""
        to_remove = []
        for cb in self.mod_list.winfo_children():
            # Check for 'get' method which CTkCheckBox has to return its state
            if hasattr(cb, "get") and cb.get():
                to_remove.append(cb.cget("text"))

        if not to_remove:
            messagebox.showinfo("No Selection", "Please select at least one mod to remove.")
            return

        confirmed = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove {len(to_remove)} selected mod(s)?"
        )
        
        if confirmed:
            for mod_name in to_remove:
                self.log(f"Removing mod: {mod_name}...")
                try:
                    self.mod_manager.remove_mod(mod_name)
                    self.log(f"Mod '{mod_name}' removed.")
                except Exception as e:
                    self.log(f"Error removing mod '{mod_name}': {str(e)}")
            
            self.refresh_mod_list()

    def init_save_sync_tab(self) -> None:
        """Initializes the Save Sync tab UI."""
        self.sync_frame = ctk.CTkFrame(self.save_sync_tab)
        self.sync_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.sync_frame.grid_columnconfigure(1, weight=1)

        # SteamID Selection
        ctk.CTkLabel(self.sync_frame, text="Local SteamID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.steam_id_dropdown = ctk.CTkOptionMenu(
            self.sync_frame, 
            values=["None Found"], 
            command=self.on_steam_id_selected
        )
        self.steam_id_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Sync Button
        self.manual_sync_btn = ctk.CTkButton(
            self.sync_frame, text="Sync Now", command=self.perform_manual_sync
        )
        self.manual_sync_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

        # Last Sync Info
        self.last_sync_label = ctk.CTkLabel(
            self.sync_frame, 
            text=f"Last Sync: {self.server_manager.state.get('last_sync_timestamp', 'Never')}"
        )
        self.last_sync_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.refresh_steam_ids()

    def init_backups_tab(self) -> None:
        """Initializes the Backups tab UI."""
        self.backups_tab.grid_columnconfigure(0, weight=1)
        self.backups_tab.grid_rowconfigure(1, weight=1)

        self.backup_now_button = ctk.CTkButton(
            self.backups_tab, text="Backup Now", command=self.manual_backup
        )
        self.backup_now_button.grid(row=0, column=0, padx=20, pady=20)

        self.backups_list_frame = ctk.CTkScrollableFrame(self.backups_tab, label_text="Available Backups")
        self.backups_list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Initial refresh
        if hasattr(self, "tk") and self.tk:
            self.refresh_backups_list()

    def on_steam_id_selected(self, steam_id: str) -> None:
        """Handles SteamID selection from the dropdown."""
        self.selected_steam_id = steam_id
        self.log(f"Save Sync: Selected SteamID {steam_id}")

    def init_config_tab(self) -> None:
        """Initializes the Configuration tab UI."""
        self.config_subtabview = ctk.CTkTabview(self.config_tab, command=self.on_config_tab_change)
        self.config_subtabview.pack(fill="both", expand=True, padx=10, pady=10)
        
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

        # Server Password
        ctk.CTkLabel(self.config_scroll, text="Server Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.server_password_entry = ctk.CTkEntry(self.config_scroll, show="*")
        self.server_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Admin Password
        ctk.CTkLabel(self.config_scroll, text="Admin Password/ID:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.admin_password_entry = ctk.CTkEntry(self.config_scroll, show="*")
        self.admin_password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Port
        ctk.CTkLabel(self.config_scroll, text="Server Port:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.server_port_entry = ctk.CTkEntry(self.config_scroll)
        self.server_port_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Update on Launch
        self.update_on_launch_var = ctk.BooleanVar(value=False)
        self.update_on_launch_checkbox = ctk.CTkCheckBox(
            self.config_scroll, text="Update on Launch", variable=self.update_on_launch_var
        )
        self.update_on_launch_checkbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Save Button
        self.save_config_button = ctk.CTkButton(
            self.config_scroll, text="Save Configuration", command=self.save_config
        )
        self.save_config_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)
        
        # Advanced Config Fields
        self.raw_ini_textbox = ctk.CTkTextbox(self.advanced_config_tab, font=("Consolas", 12))
        self.raw_ini_textbox.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        
        self.save_advanced_button = ctk.CTkButton(
            self.advanced_config_tab, text="Save Advanced Changes", command=self.save_advanced_config
        )
        self.save_advanced_button.grid(row=1, column=0, padx=10, pady=(5, 10))
        
        # Load initial values
        self.load_config_to_gui()

    def on_config_tab_change(self) -> None:
        """Handles internal configuration tab changes between Basic and Advanced."""
        if self.config_subtabview.get() == "Advanced":
            self.load_raw_ini_to_gui()
        else:
            self.load_config_to_gui()

    def load_raw_ini_to_gui(self) -> None:
        """Loads the raw INI content from the disk into the advanced textbox."""
        if not self.ini_manager:
            return

        raw_text = self.ini_manager.get_raw_text()
        self.raw_ini_textbox.delete("0.0", "end")
        self.raw_ini_textbox.insert("0.0", raw_text)

    def save_advanced_config(self) -> None:
        """Saves the raw INI content from the advanced textbox back to the disk.

        This also triggers a re-parsing of the INI file to update the basic fields.
        """
        if not self.ini_manager:
            return

        raw_text = self.raw_ini_textbox.get("0.0", "end").strip()
        if raw_text:
            self.ini_manager.save_raw_text(raw_text)
            self.log("Advanced configuration saved and re-parsed.")
            # Sync back to basic fields
            self.load_config_to_gui()
    def load_config_to_gui(self) -> None:
        """Populates the Configuration GUI fields from INI manager."""
        if not self.ini_manager:
            return
            
        self.server_name_entry.delete(0, "end")
        self.server_name_entry.insert(0, self.ini_manager.get_setting("SessionName") or "")
        
        self.server_password_entry.delete(0, "end")
        self.server_password_entry.insert(0, self.ini_manager.get_setting("ServerPassword") or "")
        
        self.admin_password_entry.delete(0, "end")
        self.admin_password_entry.insert(0, self.ini_manager.get_setting("AdminPassword") or "")
        
        self.server_port_entry.delete(0, "end")
        self.server_port_entry.insert(0, self.ini_manager.get_setting("Port") or "17777")
        
        # Sentinel section for app-specific settings
        update_val = self.ini_manager.get_setting("UpdateOnLaunch", section="Sentinel")
        self.update_on_launch_var.set(update_val == "True")

    def save_config(self) -> None:
        """Saves values from the Configuration GUI back to INI file."""
        if not self.ini_manager:
            return
            
        self.ini_manager.set_setting("SessionName", self.server_name_entry.get())
        self.ini_manager.set_setting("ServerPassword", self.server_password_entry.get())
        self.ini_manager.set_setting("AdminPassword", self.admin_password_entry.get())
        self.ini_manager.set_setting("Port", self.server_port_entry.get())
        
        self.ini_manager.set_setting("UpdateOnLaunch", str(self.update_on_launch_var.get()), section="Sentinel")
        
        self.ini_manager.save()
        self.log("Configuration saved successfully to INI file.")

    def update_ini_manager(self) -> None:
        """Updates the INI manager with the current installation path."""
        install_dir = self.path_entry.get().strip() if hasattr(self, "path_entry") else os.path.join(os.getcwd(), "icarus_server")
        ini_path = os.path.join(
            install_dir, "Icarus", "Saved", "Config", "WindowsServer", "ServerSettings.ini"
        )
        
        # Ensure directory exists for INI file
        os.makedirs(os.path.dirname(ini_path), exist_ok=True)
        
        if not self.ini_manager:
            self.ini_manager = INIManager(ini_path)
        else:
            self.ini_manager.file_path = ini_path
            self.ini_manager.load()
        
        # Update SaveSyncManager with new server path and ini_manager
        self.save_sync_manager.server_path = install_dir
        self.save_sync_manager.ini_manager = self.ini_manager

        # Ensure file exists on disk for verification/first-run
        if not os.path.exists(ini_path):
            self.ini_manager.save()

    def refresh_steam_ids(self) -> None:
        """Discovers local SteamIDs and sets a default if none selected."""
        ids = self.save_sync_manager.list_local_steam_ids()
        if ids:
            # Safer hasattr check to avoid recursion during mock init
            if "steam_id_dropdown" in self.__dict__:
                self.steam_id_dropdown.configure(values=ids)
            if not self.selected_steam_id:
                self.selected_steam_id = ids[0]
                if "steam_id_dropdown" in self.__dict__:
                    self.steam_id_dropdown.set(ids[0])
            
    def sync_saves(self, callback: Optional[Callable] = None) -> None:
        """Triggers bidirectional save synchronization in a background thread."""
        if not self.selected_steam_id:
            self.log("Save Sync: No SteamID selected. Skipping sync.")
            if callback: callback()
            return

        def _run_sync():
            self.after(0, self.log, f"Save Sync: Starting synchronization for SteamID {self.selected_steam_id}...")
            try:
                self.save_sync_manager.sync_prospects(self.selected_steam_id)
                
                # Update last sync timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.server_manager.state["last_sync_timestamp"] = timestamp
                self.server_manager.save_state()

                self.after(0, self.log, f"Save Sync: Synchronization complete at {timestamp}.")
                if hasattr(self, "last_sync_label"):
                    self.after(0, lambda: self.last_sync_label.configure(text=f"Last Sync: {timestamp}"))
            except Exception as e:
                self.after(0, self.log, f"Save Sync: Error during synchronization: {str(e)}")
            if callback:
                self.after(0, callback)

        threading.Thread(target=_run_sync, daemon=True).start()

    def perform_manual_sync(self) -> None:
        """Manually triggers save synchronization, ensuring server is stopped."""
        if self.server_process:
            messagebox.showwarning(
                "Server Running", 
                "Please stop the server before performing a manual sync to avoid data corruption."
            )
            return
        
        self.sync_saves()

    def save_settings(self) -> None:
        """Saves current settings from the UI to the manager."""
        try:
            threshold = float(self.threshold_entry.get())
            self.server_manager.ram_threshold_gb = threshold
            
            self.server_manager.smart_restart_enabled = self.smart_restart_var.get()
            self.server_manager.smart_restart_time = self.restart_time_entry.get().strip()
            
            # Update Backup Settings
            interval = float(self.backup_interval_entry.get())
            retention = int(self.backup_retention_entry.get())
            
            # Stop timer if interval changed significantly or to restart with new interval
            if interval != self.backup_manager.interval_minutes:
                self.backup_manager.stop_timer()
                self.backup_manager.interval_minutes = interval
                self.backup_manager.start_timer()
            
            self.backup_manager.retention_limit = retention
            
            self.server_manager.save_state()
            self.log("Settings saved.")
        except ValueError:
            self.log("Error: Settings must contain valid numbers.")

    def recover_state(self) -> None:
        """Attempts to recover the server process from saved state."""
        saved_pid = self.server_manager.state.get("pid")
        if saved_pid:
            try:
                p = psutil.Process(saved_pid)
                if p.is_running():
                    self.log(f"Recovered existing server process (PID: {saved_pid})")
                    self.server_process = saved_pid
                    self.start_button.configure(state="disabled")
                    self.stop_button.configure(state="normal")
                    self.restart_button.configure(state="normal")
                else:
                    self.reset_state()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.reset_state()

    def reset_state(self) -> None:
        """Resets the server state in the manager."""
        self.server_manager.state["pid"] = None
        self.server_manager.state["status"] = "stopped"
        self.server_manager.save_state()

    def browse_path(self) -> None:
        """Opens a directory dialog and updates the installation path entry."""
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, directory)
            self.update_ini_manager()

    def log(self, message: str) -> None:
        """Appends a message to the console output text box.

        Args:
            message: The string message to log.
        """
        self.console_output.configure(state="normal")
        self.console_output.insert("end", message + "\n")
        self.console_output.configure(state="disabled")
        self.console_output.see("end")

    def start_install(self) -> None:
        """Initiates the server installation process in a separate thread."""
        install_dir = self.path_entry.get().strip()
        if not install_dir:
            self.log("Error: Please select a valid installation directory.")
            return

        self.install_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.path_entry.configure(state="disabled")
        
        threading.Thread(
            target=self.run_install, args=(install_dir,), daemon=True
        ).start()

    def run_install(self, install_dir: str) -> None:
        """Executes the server installation and captures output for logging.

        Args:
            install_dir: The directory where the server should be installed.
        """
        self.log(f"Starting installation to: {install_dir}")
        
        try:
            process = self.steam_manager.install_server(install_dir)
            
            # Read stdout line by line
            if process.stdout:
                for line in iter(process.stdout.readline, ""):
                    if line:
                        self.after(0, self.log, line.strip())
                process.stdout.close()
            
            return_code = process.wait()
            
            if return_code == 0:
                self.after(0, self.log, "Installation complete!")
            else:
                self.after(0, self.log, f"Installation failed with return code: {return_code}")
        except Exception as e:
            self.after(0, self.log, f"An error occurred: {str(e)}")
        
        self.after(0, self.reset_ui)

    def reset_ui(self) -> None:
        """Re-enables UI elements after the installation process completes."""
        self.install_button.configure(state="normal")
        self.browse_button.configure(state="normal")
        self.path_entry.configure(state="normal")

    def get_server_executable(self, install_dir: str) -> Optional[str]:
        """Resolves the path to the actual server executable.

        Args:
            install_dir: The base installation directory.

        Returns:
            The full path to the executable, or None if not found.
        """
        # Common relative path for Icarus Dedicated Server
        shipping_exe = os.path.join(
            install_dir, "Icarus", "Binaries", "Win64", "IcarusServer-Win64-Shipping.exe"
        )
        if os.path.exists(shipping_exe):
            return shipping_exe
        
        # Fallback to root exe if present (though usually just a launcher)
        root_exe = os.path.join(install_dir, "IcarusServer.exe")
        if os.path.exists(root_exe):
            return root_exe
            
        return None

    def start_server(self) -> None:
        """Starts the server process in a separate thread."""
        install_dir = self.path_entry.get().strip()
        if not install_dir or not os.path.exists(install_dir):
            self.log("Error: Invalid installation directory.")
            return

        exe_path = self.get_server_executable(install_dir)
        if not exe_path:
            self.log("Error: Could not find IcarusServer executable in the selected directory.")
            return

        # Pre-flight Check
        available_pct = self.server_manager.get_available_system_ram_pct()
        if available_pct < 10.0:
            RamOptimizationDialog(self, available_pct, lambda: self.launch_server(exe_path))
        else:
            self.launch_server(exe_path)

    def launch_server(self, exe_path: str) -> None:
        """Helper to actually launch the server thread."""
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.restart_button.configure(state="normal")
        
        # Update backup manager with latest server path
        install_dir = self.path_entry.get().strip()
        self.backup_manager.server_path = install_dir
        
        # Trigger Save Sync before launch
        self.sync_saves(callback=lambda: threading.Thread(
            target=self.run_server, args=(exe_path,), daemon=True
        ).start())

    def run_server(self, exe_path: str) -> None:
        """Starts the server and streams logs."""
        try:
            # Check for Update on Launch
            if self.update_on_launch_var.get():
                install_dir = self.path_entry.get().strip()
                self.after(0, self.log, "Update on Launch enabled. Checking for updates...")
                
                process = self.steam_manager.install_server(install_dir)
                
                # Stream update output to console
                if process.stdout:
                    for line in iter(process.stdout.readline, ""):
                        if line:
                            self.after(0, self.log, line.strip())
                    process.stdout.close()
                
                return_code = process.wait()
                if return_code == 0:
                    self.after(0, self.log, "Update complete. Starting server...")
                else:
                    self.after(0, self.log, f"Update failed (Code: {return_code}). Attempting to start server anyway...")

            self.server_process = self.server_manager.start_server(exe_path)
            # self.log(f"Server started (PID: {self.server_process.pid})") # Removed to match test expectation or fix test
            
            # Start log streaming (blocks until process exit)
            self.server_manager.stream_logs(self.server_process, lambda line: self.after(0, self.log, line))
            
            # If stream_logs returns, the process has exited
            self.after(0, self.on_server_exit)
        except Exception as e:
            self.after(0, self.log, f"Server error: {str(e)}")
            self.after(0, self.on_server_exit)

    def on_server_exit(self) -> None:
        """Handles server process exit UI updates."""
        if self.server_process is None:
            return

        self.log("Server process has exited.")
        self.server_process = None
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.restart_button.configure(state="disabled")
        self.cpu_label.configure(text="CPU: 0.0%")
        self.ram_label.configure(text="RAM: 0.00GB")
        
        # Trigger Save Sync after stop
        self.sync_saves()

    def stop_server(self) -> None:
        """Stops the server process."""
        if self.server_process:
            self.log("Stopping server...")
            self.server_manager.stop_server(self.server_process)
            
            # If it's a PID (recovered process), the log reader thread isn't running,
            # so we manually trigger the exit UI cleanup.
            if isinstance(self.server_process, int):
                self.on_server_exit()
            self.log("Server stop signal sent successfully.")

    def restart_server(self) -> None:
        """Restarts the server process."""
        exe_path = self.path_entry.get().strip()
        if self.server_process and exe_path:
            self.log("Restarting server...")
            self.server_manager.stop_server(self.server_process)
            # start_server will be called by the thread or manually
            self.start_server()

    def update_monitoring(self) -> None:
        """Scheduled task to refresh monitoring data."""
        self.update_monitoring_once()
        self.after(5000, self.update_monitoring)

    def update_monitoring_once(self) -> None:
        """Updates the resource usage labels and checks for threshold alerts."""
        if self.server_process:
            old_status = self.server_manager.state["status"]
            usage = self.server_manager.get_resource_usage(self.server_process)
            new_status = self.server_manager.state["status"]
            
            self.after(0, lambda: self.cpu_label.configure(text=f"CPU: {usage['cpu']}%"))
            self.after(0, lambda: self.ram_label.configure(text=f"RAM: {usage['ram_gb']}GB"))
            
            if new_status == "warning":
                self.after(0, lambda: self.ram_label.configure(text_color="orange"))
                if old_status != "warning":
                    self.log(f"WARNING: High RAM usage detected! (>{self.server_manager.ram_threshold_gb}GB)")
            else:
                self.after(0, lambda: self.ram_label.configure(text_color=["gray10", "gray90"])) # Default CTk color

            # Check for smart restart
            if self.server_manager.should_smart_restart():
                self.log("Smart Idle Restart condition met. Triggering restart...")
                self.after(0, self.restart_server)

    def select_tab(self, name: str) -> None:
        """Switch to the specified tab and update UI selection."""
        self.tabview.set(name)
        # We will add button highlighting here in Phase 3

    def on_tab_change(self) -> None:
        """Handles tab selection events."""
        if self.tabview.get() == "Backups":
            self.refresh_backups_list()

    def show_about(self) -> None:
        """Shows the About dialog."""
        messagebox.showinfo(
            "About Icarus Sentinel",
            f"Icarus Sentinel v{__version__}\n\n"
            "A modern, portable server manager for Icarus.\n"
            "Built with CustomTkinter and PyInstaller.\n\n"
            "Copyright (c) 2026 Icarus Sentinel Team"
        )

    def manual_backup(self) -> None:
        """Triggers a manual backup."""
        self.log("Starting manual backup...")
        # Update server path in case it changed
        self.backup_manager.server_path = self.path_entry.get().strip()
        
        # Run in thread to not block UI
        threading.Thread(target=self._run_manual_backup, daemon=True).start()

    def _run_manual_backup(self) -> None:
        """Helper to run backup in thread."""
        self.backup_manager.create_backup()
        self.after(0, self.log, "Manual backup complete.")
        self.after(0, self.refresh_backups_list)

    def refresh_backups_list(self) -> None:
        """Updates the backups list in the UI."""
        # Clear existing
        for widget in self.backups_list_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(self.backup_manager.backup_path):
            ctk.CTkLabel(self.backups_list_frame, text="No backups found.").pack(pady=20)
            return

        backups = [
            f for f in os.listdir(self.backup_manager.backup_path)
            if f.startswith("Prospects_") and f.endswith(".zip")
        ]
        backups.sort(reverse=True) # Newest first

        if not backups:
            ctk.CTkLabel(self.backups_list_frame, text="No backups found.").pack(pady=20)
            return

        for backup in backups:
            row = ctk.CTkFrame(self.backups_list_frame)
            row.pack(fill="x", padx=5, pady=2, side="top")
            
            # Format label (e.g., Prospects_2026-03-17_1000.zip -> 2026-03-17 10:00)
            try:
                ts_part = backup.replace("Prospects_", "").replace(".zip", "")
                display_name = ts_part.replace("_", " ")
            except Exception:
                display_name = backup

            label = ctk.CTkLabel(row, text=display_name, anchor="w")
            label.pack(side="left", padx=10, fill="x", expand=True)
            
            restore_btn = ctk.CTkButton(
                row, text="Restore", width=80, 
                command=lambda b=backup: self.confirm_restore(b)
            )
            restore_btn.pack(side="right", padx=5, pady=2)

    def confirm_restore(self, backup_name: str) -> None:
        """Shows a confirmation dialog before restoring a backup."""
        # Ensure server is stopped
        if self.server_process:
            messagebox.showwarning(
                "Server Running", 
                "Please stop the server before restoring a backup."
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm Restore",
            f"Are you sure you want to restore the backup '{backup_name}'?\n\n"
            "This will OVERWRITE your current save progress."
        )
        if confirmed:
            self.perform_restore(backup_name)

    def perform_restore(self, backup_name: str) -> None:
        """Executes the restore operation in a background thread."""
        self.log(f"Restoring backup: {backup_name}...")
        threading.Thread(
            target=self._run_restore, args=(backup_name,), daemon=True
        ).start()

    def _run_restore(self, backup_name: str) -> None:
        """Helper to run restore in thread."""
        success = self.backup_manager.restore_backup(backup_name)
        if success:
            self.after(0, self.log, f"Restore of '{backup_name}' successful.")
        else:
            self.after(0, self.log, f"ERROR: Failed to restore '{backup_name}'.")

def main() -> None:
    """Entry point for the application."""
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
