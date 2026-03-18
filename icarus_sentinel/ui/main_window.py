import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel
from PySide6.QtCore import Qt
from icarus_sentinel.controller import Controller
from icarus_sentinel.steam_manager import SteamManager
from icarus_sentinel.server_manager import ServerProcessManager
from icarus_sentinel.backup_manager import BackupManager
from icarus_sentinel.core.ini_manager import INIManager
from icarus_sentinel.core.save_sync_manager import SaveSyncManager
from icarus_sentinel.core.mod_manager import ModManager
from icarus_sentinel.ui.sidebar import SidebarWidget
from icarus_sentinel import constants, style_config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icarus Sentinel")
        self.resize(1200, 800)
        self.setStyleSheet(f"background-color: {style_config.APP_BG}; color: {style_config.TEXT_PRIMARY};")
        
        # Initialize Managers
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
        self.ini_manager = INIManager(os.path.join(initial_server_path, "Icarus", "Saved", "Config", "WindowsServer"))
        self.save_sync_manager = SaveSyncManager(
            server_path=initial_server_path,
            ini_manager=self.ini_manager
        )
        self.mod_manager = ModManager(server_root=initial_server_path)
        
        # Initialize Controller
        self.controller = Controller(self)
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = SidebarWidget(self)
        self.sidebar.nav_requested.connect(self._on_nav_requested)
        layout.addWidget(self.sidebar)
        
        # Stacked Content Area
        self.content_stack = QStackedWidget()
        layout.addWidget(self.content_stack)
        
        # View Placeholders
        self.views = {
            "dashboard": self._create_placeholder("Dashboard View"),
            "settings": self._create_placeholder("Settings View"),
            "backups": self._create_placeholder("Backups View"),
            "sync": self._create_placeholder("Save Sync View"),
            "mods": self._create_placeholder("Mods View")
        }
        
        for nav_id, view in self.views.items():
            self.content_stack.addWidget(view)
            
        # Default view
        self._on_nav_requested("dashboard")
        self.sidebar.dashboard_btn.setChecked(True)

    def _create_placeholder(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #555555;")
        return label

    def _on_nav_requested(self, nav_id):
        if nav_id in self.views:
            self.content_stack.setCurrentWidget(self.views[nav_id])

    def log(self, message: str):
        print(f"[LOG] {message}")

    def show_error(self, message: str):
        print(f"[ERROR] {message}")

    def reset_ui(self):
        pass
