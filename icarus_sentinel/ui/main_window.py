import os
from PySide6.QtWidgets import QMainWindow
from icarus_sentinel.controller import Controller
from icarus_sentinel.steam_manager import SteamManager
from icarus_sentinel.server_manager import ServerProcessManager
from icarus_sentinel.backup_manager import BackupManager
from icarus_sentinel.core.ini_manager import INIManager
from icarus_sentinel.core.save_sync_manager import SaveSyncManager
from icarus_sentinel.core.mod_manager import ModManager
from icarus_sentinel import constants

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icarus Sentinel")
        self.resize(1200, 800)
        
        # Initialize Managers (Mirroring logic from old App class)
        self.steam_manager = SteamManager()
        
        initial_server_path = os.path.join(os.getcwd(), constants.DEFAULT_INSTALL_DIR)
        self.backup_manager = BackupManager(
            server_path=initial_server_path,
            backup_path=os.path.join(os.getcwd(), constants.DEFAULT_BACKUP_DIR)
        )
        
        self.server_manager = ServerProcessManager(
            state_file=constants.STATE_FILE, 
            backup_manager=self.backup_manager
        )
        
        # INI Manager needs a path, use default for now
        self.ini_manager = INIManager(os.path.join(initial_server_path, "Icarus", "Saved", "Config", "WindowsServer"))
        
        self.save_sync_manager = SaveSyncManager(
            server_path=initial_server_path,
            ini_manager=self.ini_manager
        )
        
        self.mod_manager = ModManager(server_root=initial_server_path)
        
        # Initialize Controller
        self.controller = Controller(self)
        
        # State placeholders
        self.server_process = None

    def log(self, message: str):
        """Placeholder for logging to a console widget."""
        print(f"[LOG] {message}")

    def show_error(self, message: str):
        """Placeholder for showing error dialogs."""
        print(f"[ERROR] {message}")

    def reset_ui(self):
        """Placeholder for resetting UI state after operations."""
        pass
