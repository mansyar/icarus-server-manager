from PySide6.QtCore import QObject, Signal
import datetime

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
    def __init__(self, server_manager, exe_path, **kwargs):
        super().__init__()
        self.server_manager = server_manager
        self.exe_path = exe_path
        self.kwargs = kwargs

    def run(self):
        try:
            process = self.server_manager.start_server(self.exe_path, **self.kwargs)
            # stream_logs is blocking until process ends
            self.server_manager.stream_logs(process, self.progress.emit)
            self.finished.emit(process.pid)
        except Exception as e:
            self.error.emit(str(e))
