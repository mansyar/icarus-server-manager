from PySide6.QtCore import QObject, Signal
import datetime
import os

class GenericWorker(QObject):
    """Base class for background workers using Qt signals."""
    finished = Signal(object)
    progress = Signal(str)
    error = Signal(str)

    def run(self):
        """Must be overridden by subclasses."""
        pass

class InstallWorker(GenericWorker):
    """Worker for handling server installation via SteamCMD."""
    def __init__(self, steam_manager, install_dir):
        super().__init__()
        self.steam_manager = steam_manager
        self.install_dir = install_dir

    def run(self):
        try:
            process = self.steam_manager.install_server(self.install_dir)
            if process.stdout:
                for line in iter(process.stdout.readline, ""):
                    if line:
                        self.progress.emit(line.strip())
                process.stdout.close()
            return_code = process.wait()
            if return_code == 0:
                self.finished.emit("Installation complete!")
            else:
                self.error.emit(f"Installation failed with return code: {return_code}")
        except Exception as e:
            self.error.emit(str(e))

class SyncWorker(GenericWorker):
    """Worker for handling save synchronization."""
    def __init__(self, save_sync_manager, steam_id):
        super().__init__()
        self.save_sync_manager = save_sync_manager
        self.steam_id = steam_id

    def run(self):
        try:
            self.save_sync_manager.sync_prospects(self.steam_id)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.finished.emit(timestamp)
        except Exception as e:
            self.error.emit(str(e))

class ServerWorker(GenericWorker):
    """Worker for running the server and streaming logs."""
    started = Signal(int) # Emits PID as soon as it starts

    def __init__(self, server_manager, exe_path, **kwargs):
        super().__init__()
        self.server_manager = server_manager
        self.exe_path = exe_path
        self.kwargs = kwargs

    def run(self):
        try:
            process = self.server_manager.start_server(self.exe_path, **self.kwargs)
            self.started.emit(process.pid)
            
            # stream_logs is blocking until process ends
            self.server_manager.stream_logs(process, self.progress.emit)
            self.finished.emit(process.pid)
        except Exception as e:
            self.error.emit(str(e))

class BackupWorker(GenericWorker):
    """Worker for handling server backups."""
    def __init__(self, backup_manager, mode="create", backup_name=None):
        super().__init__()
        self.backup_manager = backup_manager
        self.mode = mode
        self.backup_name = backup_name

    def run(self):
        try:
            if self.mode == "create":
                self.backup_manager.create_backup()
                self.finished.emit("Manual backup complete.")
            elif self.mode == "restore" and self.backup_name:
                if self.backup_manager.restore_backup(self.backup_name):
                    self.finished.emit(f"Restore of '{self.backup_name}' successful.")
                else:
                    self.error.emit(f"Failed to restore '{self.backup_name}'.")
        except Exception as e:
            self.error.emit(str(e))

class ModWorker(GenericWorker):
    """Worker for handling mod installation and removal."""
    def __init__(self, mod_manager, mode="install", files=None, mod_names=None):
        super().__init__()
        self.mod_manager = mod_manager
        self.mode = mode
        self.files = files or []
        self.mod_names = mod_names or []

    def run(self):
        try:
            if self.mode == "install":
                for f in self.files:
                    self.progress.emit(f"Installing: {os.path.basename(f)}...")
                    self.mod_manager.install_mod(f)
                self.finished.emit("Mod installation complete.")
            elif self.mode == "remove":
                for m in self.mod_names:
                    self.progress.emit(f"Removing: {m}...")
                    self.mod_manager.remove_mod(m)
                self.finished.emit("Mod removal complete.")
        except Exception as e:
            self.error.emit(str(e))

class A2SQueryWorker(GenericWorker):
    """Worker for periodic A2S server querying."""
    data_received = Signal(dict)

    def __init__(self, a2s_service, host="127.0.0.1", port=27015, interval=5.0):
        super().__init__()
        self.a2s_service = a2s_service
        self.host = host
        self.port = port
        self.interval = interval
        self._running = True

    def run(self):
        """Main loop for periodic querying."""
        import time
        while self._running:
            self.run_once()
            # Sleep in small increments to allow responsive stopping
            for _ in range(int(self.interval * 10)):
                if not self._running:
                    break
                time.sleep(0.1)
        self.finished.emit(True)

    def run_once(self):
        """Performs a single query and emits the result."""
        try:
            data = self.a2s_service.fetch_server_data(self.host, self.port)
            self.data_received.emit(data)
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        """Stops the worker loop."""
        self._running = False
