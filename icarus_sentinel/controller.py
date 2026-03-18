import datetime
import os
import threading
import psutil
from typing import Optional, Callable
from icarus_sentinel import constants

class Controller:
    """Orchestrates logic between UI and Managers for Icarus Sentinel."""
    
    def __init__(self, ui_adapter):
        """Initializes the controller with a UI adapter.
        
        Args:
            ui_adapter: Object providing log(msg) and after(ms, func) methods.
        """
        self.ui = ui_adapter
        # Managers will be accessed through ui_adapter for now to maintain state
        # In a full refactor, managers would be owned by Controller
        
    def get_server_executable(self, install_dir: str) -> Optional[str]:
        """Resolves the path to the actual server executable."""
        shipping_exe = os.path.join(install_dir, "Icarus", "Binaries", "Win64", "IcarusServer-Win64-Shipping.exe")
        if os.path.exists(shipping_exe):
            return shipping_exe
        root_exe = os.path.join(install_dir, "IcarusServer.exe")
        if os.path.exists(root_exe):
            return root_exe
        return None

    def run_install(self, install_dir: str) -> None:
        """Executes the server installation in a background thread."""
        self.ui.log(f"Starting installation to: {install_dir}")
        
        def _target():
            try:
                process = self.ui.steam_manager.install_server(install_dir)
                if process.stdout:
                    for line in iter(process.stdout.readline, ""):
                        if line:
                            self.ui.after(0, lambda m=line.strip(): self.ui.log(m))
                    process.stdout.close()
                return_code = process.wait()
                if return_code == 0:
                    self.ui.after(0, lambda: self.ui.log("Installation complete!"))
                else:
                    self.ui.after(0, lambda r=return_code: self.ui.log(f"Installation failed: {r}"))
            except Exception as e:
                self.ui.after(0, lambda s=str(e): self.ui.log(f"An error occurred: {s}"))
            self.ui.after(0, self.ui.reset_ui)
            
        threading.Thread(target=_target, daemon=True).start()

    def sync_saves(self, steam_id: str, callback: Optional[Callable] = None) -> None:
        """Triggers bidirectional save synchronization in a background thread."""
        if not steam_id:
            self.ui.log("Save Sync: No SteamID selected.")
            if callback: callback()
            return

        def _run_sync():
            self.ui.after(0, lambda: self.ui.log(f"Save Sync: Starting synchronization for SteamID {steam_id}..."))
            try:
                self.ui.save_sync_manager.sync_prospects(steam_id)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.ui.server_manager.last_sync_timestamp = timestamp
                self.ui.server_manager.save_state()
                self.ui.after(0, lambda: self.ui.log(f"Save Sync: Synchronization complete at {timestamp}."))
                if hasattr(self.ui, "last_sync_label"):
                    self.ui.after(0, lambda t=timestamp: self.ui.last_sync_label.configure(text=f"Last Sync: {t}"))
            except Exception as e:
                self.ui.after(0, lambda s=str(e): self.ui.log(f"Save Sync: Error during synchronization: {s}"))
            if callback:
                self.ui.after(0, callback)
                
        threading.Thread(target=_run_sync, daemon=True).start()

    def recover_state(self) -> None:
        """Attempts to recover the server process from saved state."""
        saved_pid = self.ui.server_manager.state.get("pid")
        if saved_pid:
            try:
                p = psutil.Process(saved_pid)
                if p.is_running():
                    self.ui.log(f"Recovered existing server process (PID: {saved_pid})")
                    self.ui.server_process = saved_pid
                    if hasattr(self.ui, "orbital_launch_btn"):
                        self.ui.orbital_launch_btn.configure(text="ABORT MISSION", fg_color="red", hover_color="darkred")
                else:
                    self.reset_state()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.reset_state()

    def run_server(self, exe_path: str) -> None:
        """Starts the server and streams logs in a background thread."""
        def _run():
            try:
                if self.ui.update_on_launch_var.get():
                    install_dir = self.ui.path_entry.get().strip()
                    self.ui.after(0, lambda: self.ui.log("Checking for updates..."))
                    process = self.ui.steam_manager.install_server(install_dir)
                    if process.stdout:
                        for line in iter(process.stdout.readline, ""):
                            if line:
                                self.ui.after(0, lambda m=line.strip(): self.ui.log(m))
                        process.stdout.close()
                    process.wait()
                
                port = int(self.ui.ini_manager.get_setting("Port") or constants.DEFAULT_PORT)
                query_port = int(self.ui.ini_manager.get_setting("QueryPort") or constants.DEFAULT_QUERY_PORT)
                server_name = self.ui.ini_manager.get_setting("SessionName") or constants.DEFAULT_SERVER_NAME
                max_players = int(self.ui.ini_manager.get_setting("MaxPlayers") or 8)
                password = self.ui.ini_manager.get_setting("ServerPassword")
                admin_password = self.ui.ini_manager.get_setting("AdminPassword")
                no_steam = self.ui.ini_manager.get_setting("NoSteam", section=constants.SECTION_SENTINEL) == "True"
                
                self.ui.server_process = self.ui.server_manager.start_server(
                    exe_path, 
                    port=port, 
                    query_port=query_port, 
                    server_name=server_name,
                    max_players=max_players,
                    password=password,
                    admin_password=admin_password,
                    no_steam=no_steam
                )
                self.ui.server_manager.stream_logs(self.ui.server_process, lambda line: self.ui.after(0, lambda m=line: self.ui.log(m)))
                self.ui.after(0, self.ui.on_server_exit)
            except Exception as e:
                self.ui.after(0, lambda s=str(e): self.ui.log(f"Server error: {s}"))
                self.ui.after(0, self.ui.on_server_exit)
        
        threading.Thread(target=_run, daemon=True).start()

    def reset_state(self) -> None:
        """Resets the server state."""
        self.ui.server_manager.state["pid"] = None
        self.ui.server_manager.state["status"] = "stopped"
        self.ui.server_manager.save_state()
