import datetime
import os
import psutil
from typing import Optional, Callable, List
from PySide6.QtCore import QThread
from icarus_sentinel import constants
from icarus_sentinel.ui.workers import InstallWorker, SyncWorker, ServerWorker

class Controller:
    """Orchestrates logic between UI and Managers for Icarus Sentinel (PySide6)."""
    
    def __init__(self, ui_adapter):
        """Initializes the controller with a UI adapter.
        
        Args:
            ui_adapter: Object providing log(msg) and other UI update methods.
        """
        self.ui = ui_adapter
        self.threads: List[QThread] = []
        
    def _run_worker(self, worker):
        """Helper to run a worker in a new thread."""
        thread = QThread()
        worker.moveToThread(thread)
        
        # Connect basic thread management
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        
        # Connect UI updates (assumes ui_adapter has log/error methods)
        if hasattr(self.ui, "log"):
            worker.progress.connect(self.ui.log)
            worker.finished.connect(lambda m: self.ui.log(str(m)) if isinstance(m, str) else None)
        
        if hasattr(self.ui, "show_error"):
            worker.error.connect(self.ui.show_error)
        elif hasattr(self.ui, "log"):
            worker.error.connect(lambda e: self.ui.log(f"ERROR: {e}"))

        # Cleanup thread when finished
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: self._prune_threads(thread))
        
        self.threads.append(thread)
        thread.start()
        return thread, worker

    def _prune_threads(self, thread):
        """Removes a finished thread from the active list."""
        if thread in self.threads:
            self.threads.remove(thread)

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
        """Executes the server installation using a QThread."""
        self.ui.log(f"Starting installation to: {install_dir}")
        worker = InstallWorker(self.ui.steam_manager, install_dir)
        
        # Reset UI when done
        if hasattr(self.ui, "reset_ui"):
            worker.finished.connect(self.ui.reset_ui)
            worker.error.connect(self.ui.reset_ui)
            
        self._run_worker(worker)

    def sync_saves(self, steam_id: str, callback: Optional[Callable] = None) -> None:
        """Triggers bidirectional save synchronization using a QThread."""
        if not steam_id:
            self.ui.log("Save Sync: No SteamID selected.")
            if callback: callback()
            return

        self.ui.log(f"Save Sync: Starting synchronization for SteamID {steam_id}...")
        worker = SyncWorker(self.ui.save_sync_manager, steam_id)
        
        def _on_finish(timestamp):
            self.ui.server_manager.last_sync_timestamp = timestamp
            self.ui.server_manager.save_state()
            self.ui.log(f"Save Sync: Synchronization complete at {timestamp}.")
            if hasattr(self.ui, "update_last_sync"):
                self.ui.update_last_sync(timestamp)
            if callback:
                callback()

        worker.finished.connect(_on_finish)
        if callback:
            worker.error.connect(callback)
            
        self._run_worker(worker)

    def recover_state(self) -> None:
        """Attempts to recover the server process from saved state."""
        saved_pid = self.ui.server_manager.state.get("pid")
        if saved_pid:
            try:
                p = psutil.Process(saved_pid)
                if p.is_running():
                    self.ui.log(f"Recovered existing server process (PID: {saved_pid})")
                    self.ui.server_process = saved_pid
                    if hasattr(self.ui, "set_server_running_state"):
                        self.ui.set_server_running_state(True)
                else:
                    self.reset_state()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.reset_state()

    def run_server(self, exe_path: str) -> None:
        """Starts the server and streams logs using a QThread."""
        # Handle update on launch (simplified for now - ideally chained workers)
        if hasattr(self.ui, "update_on_launch_var") and self.ui.update_on_launch_var.get():
            # This is complex to do with QThreads without blocking. 
            # For Phase 2, we will assume non-blocking workers.
            # A full implementation might chain workers or use a single "LaunchWorker".
            pass

        port = int(self.ui.ini_manager.get_setting("Port") or constants.DEFAULT_PORT)
        query_port = int(self.ui.ini_manager.get_setting("QueryPort") or constants.DEFAULT_QUERY_PORT)
        server_name = self.ui.ini_manager.get_setting("SessionName") or constants.DEFAULT_SERVER_NAME
        max_players = int(self.ui.ini_manager.get_setting("MaxPlayers") or 8)
        password = self.ui.ini_manager.get_setting("ServerPassword")
        admin_password = self.ui.ini_manager.get_setting("AdminPassword")
        no_steam = self.ui.ini_manager.get_setting("NoSteam", section=constants.SECTION_SENTINEL) == "True"

        kwargs = {
            "port": port,
            "query_port": query_port,
            "server_name": server_name,
            "max_players": max_players,
            "password": password,
            "admin_password": admin_password,
            "no_steam": no_steam
        }

        worker = ServerWorker(self.ui.server_manager, exe_path, **kwargs)
        
        if hasattr(self.ui, "on_server_exit"):
            worker.finished.connect(self.ui.on_server_exit)
            worker.error.connect(self.ui.on_server_exit)
            
        self._run_worker(worker)

    def reset_state(self) -> None:
        """Resets the server state."""
        self.ui.server_manager.state["pid"] = None
        self.ui.server_manager.state["status"] = "stopped"
        self.ui.server_manager.save_state()
