import datetime
import os
import psutil
from typing import Optional, Callable, List, Dict
from PySide6.QtCore import QThread, QObject, Signal
from icarus_sentinel import constants
from icarus_sentinel.ui.workers import InstallWorker, SyncWorker, ServerWorker, BackupWorker, ModWorker, A2SQueryWorker

class Controller(QObject):
    """Orchestrates logic between UI and Managers for Icarus Sentinel (PySide6)."""
    backups_updated = Signal()
    mods_updated = Signal()
    server_started = Signal(int)
    
    def __init__(self, ui_adapter):
        """Initializes the controller with a UI adapter.
        
        Args:
            ui_adapter: Object providing log(msg) and other UI update methods.
        """
        super().__init__()
        self.ui = ui_adapter
        self.threads: List[QThread] = []
        self.workers: List[QObject] = [] # Keep references to prevent GC
        self.a2s_worker: Optional[A2SQueryWorker] = None
        self.a2s_thread: Optional[QThread] = None
        
    @property
    def last_sync_timestamp(self):
        return self.ui.server_manager.last_sync_timestamp

    def _run_worker(self, worker):
        """Helper to run a worker in a new thread."""
        thread = QThread()
        worker.moveToThread(thread)
        
        # Connect basic thread management
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        
        # Connect UI updates
        if hasattr(self.ui, "log"):
            worker.progress.connect(self.ui.log)
            worker.progress_source.connect(self.ui.log)
            worker.finished.connect(lambda m: self.ui.log(str(m), source="success") if isinstance(m, str) else None)
        
        if hasattr(self.ui, "show_error"):
            worker.error.connect(self.ui.show_error)
        elif hasattr(self.ui, "log"):
            worker.error.connect(lambda e: self.ui.log(f"ERROR: {e}", source="error"))

        # Cleanup thread when finished
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: self._prune_threads(thread, worker))
        
        self.threads.append(thread)
        self.workers.append(worker)
        thread.start()
        return thread, worker

    def _prune_threads(self, thread, worker):
        """Removes finished thread and worker from active lists."""
        if thread in self.threads:
            self.threads.remove(thread)
        if worker in self.workers:
            self.workers.remove(worker)

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
                    if hasattr(self.ui, "dashboard") and hasattr(self.ui.dashboard.control, "is_running"):
                        if not self.ui.dashboard.control.is_running:
                            # Safely toggle UI state
                            self.ui.dashboard.control.is_running = True
                            self.ui.dashboard.control.launch_btn.setText("ABORT MISSION")
                            self.ui.dashboard.control.launch_btn.setStyleSheet(self.ui.dashboard.control.launch_btn.styleSheet().replace("#FF8C00", "#FF5252"))
                else:
                    self.reset_state()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.reset_state()

    def run_server(self, exe_path: str) -> None:
        """Starts the server and streams logs using a QThread."""
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
        
        # Connect signals
        worker.started.connect(self.server_started.emit)
        worker.ready.connect(lambda: self.ui.log("Server is ready for players!", source="success"))

        if hasattr(self.ui, "on_server_exit"):
            worker.finished.connect(self.ui.on_server_exit)
            worker.error.connect(self.ui.on_server_exit)
            
        self._run_worker(worker)

    def run_backup(self) -> None:
        """Triggers a manual backup using a QThread."""
        self.ui.log("Manual Backup: Starting...")
        worker = BackupWorker(self.ui.backup_manager, mode="create")
        worker.finished.connect(lambda _: self.backups_updated.emit())
        self._run_worker(worker)

    def run_restore(self, backup_name: str) -> None:
        """Triggers a backup restore using a QThread."""
        if self.ui.server_process:
            self.ui.show_error("Please stop the server before restoring a backup.")
            return
            
        self.ui.log(f"Restore: Starting restore of {backup_name}...")
        worker = BackupWorker(self.ui.backup_manager, mode="restore", backup_name=backup_name)
        self._run_worker(worker)

    def run_mod_install(self, file_paths):
        """Installs mods from provided paths using a QThread."""
        worker = ModWorker(self.ui.mod_manager, mode="install", files=file_paths)
        worker.finished.connect(lambda _: self.mods_updated.emit())
        self._run_worker(worker)

    def run_mod_remove(self, mod_names):
        """Removes mods by name using a QThread."""
        worker = ModWorker(self.ui.mod_manager, mode="remove", mod_names=mod_names)
        worker.finished.connect(lambda _: self.mods_updated.emit())
        self._run_worker(worker)

    def save_sentinel_settings(self, data: Dict):
        """Saves Sentinel-specific manager settings."""
        try:
            if data.get("restart_time") != self.ui.server_manager.smart_restart_time:
                self.ui.server_manager.last_smart_restart_date = None
            
            self.ui.server_manager.ram_threshold_gb = float(data.get("ram_threshold", 12.0))
            self.ui.server_manager.smart_restart_enabled = data.get("smart_restart", False)
            self.ui.server_manager.smart_restart_time = data.get("restart_time", "04:00")
            
            interval = float(data.get("backup_interval", 30.0))
            if interval != self.ui.backup_manager.interval_minutes:
                self.ui.backup_manager.stop_timer()
                self.ui.backup_manager.interval_minutes = interval
                self.ui.backup_manager.start_timer()
            
            self.ui.backup_manager.retention_limit = int(data.get("retention_limit", 50))
            
            # Notifications
            self.ui.server_manager.notify_server_started = data.get("notify_server_started", True)
            self.ui.server_manager.notify_player_activity = data.get("notify_player_activity", True)
            self.ui.server_manager.notify_server_error = data.get("notify_server_error", True)
            
            self.ui.server_manager.save_state()
            self.ui.log("Sentinel settings saved.")
        except Exception as e:
            self.ui.log(f"ERROR saving settings: {e}")

    def reset_state(self) -> None:
        """Resets the server state."""
        self.ui.server_manager.state["pid"] = None
        self.ui.server_manager.state["status"] = "stopped"
        self.ui.server_manager.save_state()

    def run_a2s_query(self, service, host, port, interval=5.0):
        """Starts periodic A2S querying in a background thread."""
        if self.a2s_worker:
            self.stop_a2s_query()
            
        self.a2s_worker = A2SQueryWorker(service, host, port, interval)
        self.a2s_thread = QThread()
        self.a2s_worker.moveToThread(self.a2s_thread)
        
        self.a2s_thread.started.connect(self.a2s_worker.run)
        self.a2s_worker.finished.connect(self.a2s_thread.quit)
        self.a2s_worker.finished.connect(self.a2s_thread.deleteLater)
        
        # Connect to UI
        if hasattr(self.ui, "players_view"):
            self.a2s_worker.data_received.connect(self.ui.players_view.update_data)
        
        self.a2s_thread.start()

    def stop_a2s_query(self):
        """Stops the A2S query worker."""
        if self.a2s_worker and self.a2s_thread:
            self.a2s_worker.stop()
            if self.a2s_thread.isRunning():
                self.a2s_thread.quit()
                if not self.a2s_thread.wait(1000):
                    self.a2s_thread.terminate()
            self.a2s_worker = None
            self.a2s_thread = None

    def stop_all_threads(self):
        """Gracefully stops all active background threads and workers."""
        self.stop_a2s_query()
        
        # Stop any other active workers
        for worker in list(self.workers):
            if hasattr(worker, "stop"):
                worker.stop()
        
        # Quit and wait for all threads
        for thread in list(self.threads):
            if thread.isRunning():
                thread.quit()
                if not thread.wait(500):
                    thread.terminate()
        
        self.threads.clear()
        self.workers.clear()
