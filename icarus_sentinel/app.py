import datetime
import os
import subprocess
import threading
from tkinter import filedialog, messagebox
from typing import Optional, Callable

import customtkinter as ctk
import psutil

from icarus_sentinel import __version__, style_config, constants
from icarus_sentinel.steam_manager import SteamManager
from icarus_sentinel.server_manager import ServerProcessManager
from icarus_sentinel.backup_manager import BackupManager
from icarus_sentinel.core.ini_manager import INIManager
from icarus_sentinel.core.save_sync_manager import SaveSyncManager
from icarus_sentinel.core.mod_manager import ModManager
from icarus_sentinel.controller import Controller
from icarus_sentinel.ui import (
    RamOptimizationDialog, DashboardView, ConfigView, 
    BackupsView, SaveSyncView, ModsView
)

# Set appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") # We will override with our own colors

class App(ctk.CTk):
    """Main application class for Icarus Sentinel."""

    def __init__(self, state_file: str = constants.STATE_FILE) -> None:
        """Initializes the main application window and its components."""
        super().__init__()
        self.title("Icarus Sentinel")
        self.geometry("1100x700")
        self.minsize(800, 600)
        self.configure(fg_color=style_config.APP_BG)
        
        self.controller = Controller(self)
        self.steam_manager = SteamManager()
        
        # Initialize BackupManager
        initial_server_path = os.path.join(os.getcwd(), constants.DEFAULT_INSTALL_DIR)
        self.backup_manager = BackupManager(
            server_path=initial_server_path,
            backup_path=os.path.join(os.getcwd(), constants.DEFAULT_BACKUP_DIR)
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
        
        # Initialize ModManager
        self.mod_manager = ModManager(server_root=initial_server_path)

        # Initialize INI Manager with default path
        self.update_ini_manager()

        # Start backup timer
        self.backup_manager.start_timer()
        
        # Main Grid layout
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main content area
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=style_config.SIDEBAR_BG)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Spacer

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
            anchor="w", command=lambda: self.select_tab(constants.VIEW_SERVER)
        )
        self.nav_dashboard_btn.grid(row=1, column=0, sticky="ew")

        self.nav_settings_btn = ctk.CTkButton(
            self.sidebar_frame, text="Configuration", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab(constants.VIEW_CONFIG)
        )
        self.nav_settings_btn.grid(row=2, column=0, sticky="ew")

        self.nav_backups_btn = ctk.CTkButton(
            self.sidebar_frame, text="Backups", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab(constants.VIEW_BACKUPS)
        )
        self.nav_backups_btn.grid(row=3, column=0, sticky="ew")

        self.nav_sync_btn = ctk.CTkButton(
            self.sidebar_frame, text="Save Sync", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab(constants.VIEW_SYNC)
        )
        self.nav_sync_btn.grid(row=4, column=0, sticky="ew")

        self.nav_mods_btn = ctk.CTkButton(
            self.sidebar_frame, text="Mods", corner_radius=0, height=40, border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.select_tab(constants.VIEW_MODS)
        )
        self.nav_mods_btn.grid(row=5, column=0, sticky="ew")
        
        # Main Content Frame
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1) # Upper content
        self.main_content_frame.grid_rowconfigure(1, weight=0) # Console

        # View Frames (Using separate classes)
        self.views = {}
        self.views[constants.VIEW_SERVER] = DashboardView(self.main_content_frame, self)
        self.views[constants.VIEW_CONFIG] = ConfigView(self.main_content_frame, self)
        self.views[constants.VIEW_SYNC] = SaveSyncView(self.main_content_frame, self)
        self.views[constants.VIEW_BACKUPS] = BackupsView(self.main_content_frame, self)
        self.views[constants.VIEW_MODS] = ModsView(self.main_content_frame, self)

        # Console
        self.console_output = ctk.CTkTextbox(
            self.main_content_frame, 
            height=150, 
            state="disabled",
            fg_color=style_config.CONSOLE_BG,
            text_color=style_config.CONSOLE_TEXT,
            font=style_config.FONT_MONO
        )
        self.console_output.grid(row=1, column=0, sticky="ew", pady=(10, 0))

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

        # Show initial view
        self.select_tab(constants.VIEW_SERVER)

        # Recover state
        self.recover_state()

        # Start monitoring loop
        self.update_monitoring()

    def select_tab(self, name: str) -> None:
        """Switch to the specified view and update UI selection."""
        # Hide all views
        for view in self.views.values():
            view.grid_forget()
        
        # Show selected view
        self.views[name].grid(row=0, column=0, sticky="nsew")

        # Update button highlighting
        self.nav_dashboard_btn.configure(fg_color=("gray75", "gray25") if name == constants.VIEW_SERVER else "transparent")
        self.nav_settings_btn.configure(fg_color=("gray75", "gray25") if name == constants.VIEW_CONFIG else "transparent")
        self.nav_backups_btn.configure(fg_color=("gray75", "gray25") if name == constants.VIEW_BACKUPS else "transparent")
        self.nav_sync_btn.configure(fg_color=("gray75", "gray25") if name == constants.VIEW_SYNC else "transparent")
        self.nav_mods_btn.configure(fg_color=("gray75", "gray25") if name == constants.VIEW_MODS else "transparent")

        if name == constants.VIEW_BACKUPS:
            self.refresh_backups_list()

    def on_steam_id_selected(self, steam_id: str) -> None:
        """Handles SteamID selection from the dropdown."""
        self.selected_steam_id = steam_id
        self.log(f"Save Sync: Selected SteamID {steam_id}")

    def on_config_tab_change(self) -> None:
        """Handles internal configuration tab changes."""
        if hasattr(self, "config_subtabview") and self.config_subtabview.get() == "Advanced":
            self.load_raw_ini_to_gui()
        else:
            self.load_config_to_gui()

    def load_raw_ini_to_gui(self) -> None:
        """Loads the raw INI content from the disk."""
        if not self.ini_manager or not hasattr(self, "raw_ini_textbox"): return
        raw_text = self.ini_manager.get_raw_text()
        self.raw_ini_textbox.delete("0.0", "end")
        self.raw_ini_textbox.insert("0.0", raw_text)

    def save_advanced_config(self) -> None:
        """Saves the raw INI content back to the disk."""
        if not self.ini_manager or not hasattr(self, "raw_ini_textbox"): return
        raw_text = self.raw_ini_textbox.get("0.0", "end").strip()
        if raw_text:
            self.ini_manager.save_raw_text(raw_text)
            self.log("Advanced configuration saved.")
            self.load_config_to_gui()

    def load_config_to_gui(self) -> None:
        """Populates the Configuration GUI fields from INI manager."""
        if not self.ini_manager or not hasattr(self, "server_name_entry"): return
        self.server_name_entry.delete(0, "end")
        self.server_name_entry.insert(0, self.ini_manager.get_setting("SessionName") or constants.DEFAULT_SERVER_NAME)
        self.server_password_entry.delete(0, "end")
        self.server_password_entry.insert(0, self.ini_manager.get_setting("ServerPassword") or "")
        self.admin_password_entry.delete(0, "end")
        self.admin_password_entry.insert(0, self.ini_manager.get_setting("AdminPassword") or "")
        self.server_port_entry.delete(0, "end")
        self.server_port_entry.insert(0, self.ini_manager.get_setting("Port") or constants.DEFAULT_PORT)
        if hasattr(self, "query_port_entry"):
            self.query_port_entry.delete(0, "end")
            self.query_port_entry.insert(0, self.ini_manager.get_setting("QueryPort") or constants.DEFAULT_QUERY_PORT)
        update_val = self.ini_manager.get_setting("UpdateOnLaunch", section=constants.SECTION_SENTINEL)
        self.update_on_launch_var.set(update_val == "True")
        if hasattr(self, "no_steam_var"):
            no_steam_val = self.ini_manager.get_setting("NoSteam", section=constants.SECTION_SENTINEL)
            self.no_steam_var.set(no_steam_val == "True")

    def save_config(self) -> None:
        """Saves values from the Configuration GUI back to INI file."""
        if not self.ini_manager or not hasattr(self, "server_name_entry"): return
        self.ini_manager.set_setting("SessionName", self.server_name_entry.get())
        self.ini_manager.set_setting("ServerPassword", self.server_password_entry.get())
        self.admin_password_entry.get() and self.ini_manager.set_setting("AdminPassword", self.admin_password_entry.get())
        self.ini_manager.set_setting("Port", self.server_port_entry.get())
        if hasattr(self, "query_port_entry"):
            self.ini_manager.set_setting("QueryPort", self.query_port_entry.get())
        self.ini_manager.set_setting("UpdateOnLaunch", str(self.update_on_launch_var.get()), section=constants.SECTION_SENTINEL)
        if hasattr(self, "no_steam_var"):
            self.ini_manager.set_setting("NoSteam", str(self.no_steam_var.get()), section=constants.SECTION_SENTINEL)
        self.ini_manager.save()
        self.log("Configuration saved successfully.")

    def update_ini_manager(self) -> None:
        """Updates the INI manager with the current installation path."""
        install_dir = self.path_entry.get().strip() if hasattr(self, "path_entry") else os.path.join(os.getcwd(), constants.DEFAULT_INSTALL_DIR)
        ini_path = os.path.join(install_dir, "Icarus", "Saved", "Config", "WindowsServer", "ServerSettings.ini")
        os.makedirs(os.path.dirname(ini_path), exist_ok=True)
        if not self.ini_manager: self.ini_manager = INIManager(ini_path)
        else:
            self.ini_manager.file_path = ini_path
            self.ini_manager.load()
        self.save_sync_manager.server_path = install_dir
        self.save_sync_manager.ini_manager = self.ini_manager
        if not os.path.exists(ini_path): self.ini_manager.save()
        
        # Refresh Config GUI if widgets are ready
        self.load_config_to_gui()
        self.load_raw_ini_to_gui()

    def refresh_steam_ids(self) -> None:
        """Discovers local SteamIDs."""
        ids = self.save_sync_manager.list_local_steam_ids()
        if ids:
            if hasattr(self, "steam_id_dropdown"):
                self.steam_id_dropdown.configure(values=ids)
            if not self.selected_steam_id:
                self.selected_steam_id = ids[0]
                if hasattr(self, "steam_id_dropdown"):
                    self.steam_id_dropdown.set(ids[0])
            
    def perform_manual_sync(self) -> None:
        """Manually triggers save synchronization."""
        if self.server_process:
            messagebox.showwarning("Server Running", "Please stop the server before sync.")
            return
        self.controller.sync_saves(self.selected_steam_id)

    def recover_state(self) -> None:
        """Attempts to recover the server process from saved state."""
        self.controller.recover_state()

    def reset_state(self) -> None:
        """Resets the server state."""
        self.controller.reset_state()

    def browse_path(self) -> None:
        """Opens a directory dialog."""
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, directory)
            self.update_ini_manager()

    def log(self, message: str) -> None:
        """Appends a message to the console output."""
        self.console_output.configure(state="normal")
        self.console_output.insert("end", message + "\n")
        self.console_output.configure(state="disabled")
        self.console_output.see("end")

    def start_install(self) -> None:
        """Initiates the server installation process."""
        install_dir = self.path_entry.get().strip()
        if not install_dir:
            self.log("Error: Please select a valid installation directory.")
            return
        self.install_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.path_entry.configure(state="disabled")
        self.controller.run_install(install_dir)

    def reset_ui(self) -> None:
        """Re-enables UI elements after installation."""
        if hasattr(self, "install_button"): self.install_button.configure(state="normal")
        if hasattr(self, "browse_button"): self.browse_button.configure(state="normal")
        if hasattr(self, "path_entry"): self.path_entry.configure(state="normal")

    def start_server(self) -> None:
        """Starts the server process."""
        install_dir = self.path_entry.get().strip()
        if not install_dir or not os.path.exists(install_dir):
            self.log("Error: Invalid installation directory.")
            return
        exe_path = self.controller.get_server_executable(install_dir)
        if not exe_path:
            self.log("Error: Could not find IcarusServer executable.")
            return
        available_pct = self.server_manager.get_available_system_ram_pct()
        if available_pct < 10.0: RamOptimizationDialog(self, available_pct, lambda: self.launch_server(exe_path))
        else: self.launch_server(exe_path)

    def toggle_server(self) -> None:
        """Toggles the server state."""
        if self.server_process: self.stop_server()
        else: self.start_server()

    def launch_server(self, exe_path: str) -> None:
        """Helper to actually launch the server thread."""
        if hasattr(self, "orbital_launch_btn"):
            self.orbital_launch_btn.configure(text="ABORT MISSION", fg_color="red", hover_color="darkred")
        self.backup_manager.server_path = self.path_entry.get().strip()
        self.controller.sync_saves(self.selected_steam_id, callback=lambda: self.controller.run_server(exe_path))

    def on_server_exit(self) -> None:
        """Handles server process exit UI updates."""
        if self.server_process is None: return
        self.log("Server process has exited.")
        self.server_process = None
        if hasattr(self, "orbital_launch_btn"):
            self.orbital_launch_btn.configure(text="INITIATE ORBITAL LAUNCH", fg_color=style_config.ACCENT_COLOR, hover_color="#e67e00")
        self.controller.sync_saves(self.selected_steam_id)

    def stop_server(self) -> None:
        """Stops the server process."""
        if self.server_process:
            self.log("Stopping server...")
            self.server_manager.stop_server(self.server_process)
            if isinstance(self.server_process, int): self.on_server_exit()

    def restart_server(self) -> None:
        """Restarts the server process."""
        if self.server_process:
            self.log("Restarting server...")
            self.server_manager.stop_server(self.server_process)
            self.start_server()

    def update_monitoring(self) -> None:
        """Scheduled task to refresh monitoring data."""
        self.update_monitoring_once()
        self.after(constants.MONITORING_INTERVAL_MS, self.update_monitoring)

    def update_monitoring_once(self) -> None:
        """Updates resource usage labels."""
        if self.server_process:
            old_status = self.server_manager.state["status"]
            usage = self.server_manager.get_resource_usage(self.server_process)
            new_status = self.server_manager.state["status"]
            cpu_val, ram_val = usage["cpu"], usage["ram_gb"]
            ram_limit = self.server_manager.ram_threshold_gb
            
            if hasattr(self, "cpu_usage_label"):
                self.after(0, lambda: self.cpu_usage_label.configure(text=f"CPU USAGE: {cpu_val}%"))
            if hasattr(self, "cpu_progress_bar"):
                self.after(0, lambda: self.cpu_progress_bar.set(cpu_val / 100.0))
            if hasattr(self, "ram_usage_label"):
                self.after(0, lambda: self.ram_usage_label.configure(text=f"RAM USAGE: {ram_val}GB / {ram_limit}GB"))
            if hasattr(self, "ram_progress_bar"):
                self.after(0, lambda: self.ram_progress_bar.set(min(1.0, ram_val / ram_limit) if ram_limit > 0 else 0))
            
            if new_status == "warning":
                if hasattr(self, "ram_usage_label"): self.after(0, lambda: self.ram_usage_label.configure(text_color="orange"))
                if hasattr(self, "ram_progress_bar"): self.after(0, lambda: self.ram_progress_bar.configure(progress_color="orange"))
                if old_status != "warning": self.log(f"WARNING: High RAM usage! (>{ram_limit}GB)")
            else:
                if hasattr(self, "ram_usage_label"): self.after(0, lambda: self.ram_usage_label.configure(text_color=style_config.TEXT_PRIMARY))
                if hasattr(self, "ram_progress_bar"): self.after(0, lambda: self.ram_progress_bar.configure(progress_color=style_config.ACCENT_COLOR))
            
            if self.server_manager.should_smart_restart():
                self.log("Smart Idle Restart condition met.")
                self.after(0, self.restart_server)

    def save_settings(self) -> None:
        """Saves current settings from the UI."""
        try:
            self.server_manager.ram_threshold_gb = float(self.threshold_entry.get())
            self.server_manager.smart_restart_enabled = self.smart_restart_var.get()
            self.server_manager.smart_restart_time = self.restart_time_entry.get().strip()
            interval = float(self.backup_interval_entry.get())
            if interval != self.backup_manager.interval_minutes:
                self.backup_manager.stop_timer()
                self.backup_manager.interval_minutes = interval
                self.backup_manager.start_timer()
            self.backup_manager.retention_limit = int(self.backup_retention_entry.get())
            self.server_manager.save_state()
            self.log("Settings saved.")
        except (ValueError, AttributeError):
            self.log("Error: Settings must contain valid numbers.")

    def show_about(self) -> None:
        """Shows the About dialog."""
        messagebox.showinfo("About Icarus Sentinel", f"Icarus Sentinel v{__version__}\n\nA modern server manager for Icarus.\nCopyright (c) 2026")

    def manual_backup(self) -> None:
        """Triggers a manual backup."""
        self.log("Starting manual backup...")
        self.backup_manager.server_path = self.path_entry.get().strip()
        threading.Thread(target=self._run_manual_backup, daemon=True).start()

    def _run_manual_backup(self) -> None:
        """Helper to run backup in thread."""
        self.backup_manager.create_backup()
        self.after(0, self.log, "Manual backup complete.")
        self.after(0, self.refresh_backups_list)

    def refresh_backups_list(self) -> None:
        """Updates the backups list in the UI."""
        if not hasattr(self, "backups_list_frame"): return
        for widget in self.backups_list_frame.winfo_children(): widget.destroy()
        if not os.path.exists(self.backup_manager.backup_path):
            ctk.CTkLabel(self.backups_list_frame, text="No backups found.").pack(pady=20)
            return
        backups = [f for f in os.listdir(self.backup_manager.backup_path) if f.startswith("Prospects_") and f.endswith(".zip")]
        backups.sort(reverse=True)
        if not backups:
            ctk.CTkLabel(self.backups_list_frame, text="No backups found.").pack(pady=20)
            return
        for backup in backups:
            row = ctk.CTkFrame(self.backups_list_frame)
            row.pack(fill="x", padx=5, pady=2, side="top")
            try: display_name = backup.replace("Prospects_", "").replace(".zip", "").replace("_", " ")
            except Exception: display_name = backup
            ctk.CTkLabel(row, text=display_name, anchor="w").pack(side="left", padx=10, fill="x", expand=True)
            ctk.CTkButton(row, text="Restore", width=80, command=lambda b=backup: self.confirm_restore(b)).pack(side="right", padx=5, pady=2)

    def confirm_restore(self, backup_name: str) -> None:
        """Shows confirmation before restoring."""
        if self.server_process:
            messagebox.showwarning("Server Running", "Please stop the server before restore.")
            return
        if messagebox.askyesno("Confirm Restore", f"Overwrite current progress with '{backup_name}'?"):
            self.perform_restore(backup_name)

    def perform_restore(self, backup_name: str) -> None:
        """Executes restore in a background thread."""
        self.log(f"Restoring backup: {backup_name}...")
        threading.Thread(target=self._run_restore, args=(backup_name,), daemon=True).start()

    def _run_restore(self, backup_name: str) -> None:
        """Helper to run restore in thread."""
        if self.backup_manager.restore_backup(backup_name):
            self.after(0, self.log, f"Restore of '{backup_name}' successful.")
        else: self.after(0, self.log, f"ERROR: Failed to restore '{backup_name}'.")

    def toggle_select_all_mods(self) -> None:
        """Toggles all mod checkboxes."""
        if not hasattr(self, "mod_list"): return
        val = self.select_all_var.get()
        for cb in self.mod_list.winfo_children():
            if isinstance(cb, ctk.CTkCheckBox):
                if val: cb.select()
                else: cb.deselect()

    def refresh_mod_list(self) -> None:
        """Updates the installed mods list."""
        if not hasattr(self, "mod_list"): return
        for widget in self.mod_list.winfo_children(): widget.destroy()
        mods = self.mod_manager.list_mods()
        if not mods:
            ctk.CTkLabel(self.mod_list, text="No mods installed.").pack(pady=10)
            if hasattr(self, "select_all_cb"): self.select_all_cb.configure(state="disabled")
        else:
            if hasattr(self, "select_all_cb"): self.select_all_cb.configure(state="normal")
            self.select_all_var.set(False)
            for mod in mods: ctk.CTkCheckBox(self.mod_list, text=mod).pack(fill="x", padx=10, pady=5)

    def install_mod_ui(self) -> None:
        """Installs selected mods."""
        file_paths = filedialog.askopenfilenames(title="Select Mod Files", filetypes=[("Mod Files", "*.pak *.zip")])
        if file_paths:
            for f in file_paths:
                self.log(f"Installing: {os.path.basename(f)}...")
                try:
                    self.mod_manager.install_mod(f)
                    self.log("Success.")
                except Exception as e: self.log(f"Error: {str(e)}")
            self.refresh_mod_list()

    def remove_mod_ui(self) -> None:
        """Removes checked mods."""
        if not hasattr(self, "mod_list"): return
        to_remove = [cb.cget("text") for cb in self.mod_list.winfo_children() if isinstance(cb, ctk.CTkCheckBox) and cb.get()]
        if not to_remove: return
        if messagebox.askyesno("Confirm", f"Remove {len(to_remove)} mod(s)?"):
            for m in to_remove:
                self.log(f"Removing: {m}...")
                try: self.mod_manager.remove_mod(m)
                except Exception as e: self.log(f"Error: {str(e)}")
            self.refresh_mod_list()

def main() -> None:
    """Entry point for the application.
    
    Initializes and starts the main application loop.
    """
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
