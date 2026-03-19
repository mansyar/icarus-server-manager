import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPalette, QBrush
from icarus_sentinel.controller import Controller
from icarus_sentinel.steam_manager import SteamManager
from icarus_sentinel.server_manager import ServerProcessManager
from icarus_sentinel.backup_manager import BackupManager
from icarus_sentinel.core.ini_manager import INIManager
from icarus_sentinel.core.save_sync_manager import SaveSyncManager
from icarus_sentinel.core.mod_manager import ModManager
from icarus_sentinel.ui.sidebar import SidebarWidget
from icarus_sentinel.ui.dashboard import DashboardView, ConsoleWidget
from icarus_sentinel.ui.config import ConfigView
from icarus_sentinel.ui.backups import BackupsView
from icarus_sentinel.ui.save_sync import SaveSyncView
from icarus_sentinel.ui.mods import ModsView
from icarus_sentinel.ui.players import PlayersView
from icarus_sentinel.ui.about_view import AboutView
from icarus_sentinel import constants, style_config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icarus Sentinel")
        self.resize(1250, 800)
        
        # Set Window Background
        self.apply_window_background()
        
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
        # INI Manager needs a file path, ensure directory exists
        ini_dir = os.path.join(initial_server_path, "Icarus", "Saved", "Config", "WindowsServer")
        os.makedirs(ini_dir, exist_ok=True)
        self.ini_manager = INIManager(os.path.join(ini_dir, "ServerSettings.ini"))
        self.save_sync_manager = SaveSyncManager(
            server_path=initial_server_path,
            ini_manager=self.ini_manager
        )
        self.mod_manager = ModManager(server_root=initial_server_path)
        
        # Initialize Controller
        self.controller = Controller(self)
        self.controller.server_started.connect(self._on_server_started)
        
        self.server_process = None
        self.setup_ui()
        self.setup_timer()
        self.controller.recover_state()

    def apply_window_background(self):
        bg_path = constants.get_resource_path(os.path.join("assets", "backgound_space.png"))
        if os.path.exists(bg_path):
            original_pixmap = QPixmap(bg_path)
            scaled_pixmap = original_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            from PySide6.QtGui import QPainter
            dimmed_pixmap = QPixmap(scaled_pixmap.size())
            dimmed_pixmap.fill(Qt.black)
            
            painter = QPainter(dimmed_pixmap)
            painter.setOpacity(0.4)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(dimmed_pixmap))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            self.setStyleSheet(f"background-color: {style_config.APP_BG};")

    def resizeEvent(self, event):
        self.apply_window_background()
        super().resizeEvent(event)

    def setup_ui(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Sidebar
        self.sidebar = SidebarWidget(self)
        self.sidebar.nav_requested.connect(self._on_nav_requested)
        main_layout.addWidget(self.sidebar)
        
        # 2. Right Content Area (Stack + Console)
        content_container = QWidget()
        content_container.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Stacked Content
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background: transparent;")
        
        # Views
        self.dashboard = DashboardView()
        self.dashboard.control.action_triggered.connect(self._on_launch_clicked)
        
        self.players_view = PlayersView()
        self.config_view = ConfigView(app=self)
        self.backups_view = BackupsView(app=self)
        self.sync_view = SaveSyncView(app=self)
        self.mods_view = ModsView(app=self)
        self.about_view = AboutView()
        
        self.views = {
            "dashboard": self.dashboard,
            "players": self.players_view,
            "settings": self.config_view,
            "backups": self.backups_view,
            "sync": self.sync_view,
            "mods": self.mods_view,
            "about": self.about_view
        }
        
        for nav_id, view in self.views.items():
            self.content_stack.addWidget(view)
            
        # Global Console (Persistent)
        self.console = ConsoleWidget()
        self.console.setFixedHeight(180)
        
        content_layout.addWidget(self.content_stack, 1)
        content_layout.addWidget(self.console)
        
        main_layout.addWidget(content_container, 1)
            
        # Default view
        self._on_nav_requested("dashboard")
        self.sidebar.dashboard_btn.setChecked(True)

    def setup_timer(self):
        from PySide6.QtCore import QTimer
        self.metrics_timer = QTimer(self)
        self.metrics_timer.timeout.connect(self._update_metrics)
        self.metrics_timer.start(5000)

    def _update_metrics(self):
        if self.server_process:
            usage = self.server_manager.get_resource_usage(self.server_process)
            self.dashboard.update_metrics(usage["cpu"], usage["ram_gb"])

            # Check for Smart Restart
            query_port_str = self.ini_manager.get_setting("QueryPort") or constants.DEFAULT_QUERY_PORT
            query_port = int(query_port_str)
            if self.server_manager.should_smart_restart(query_port=query_port):
                self.log("Smart Idle Restart condition met. Restarting server...")
                self._on_launch_clicked(False) # Stop
                self._on_launch_clicked(True)  # Start
        else:
            self.dashboard.update_metrics(0.0, 0.0)

    def update_last_sync(self, timestamp):
        """Updates the last sync label in the sync view."""
        if hasattr(self, "sync_view"):
            self.sync_view.last_sync_label.setText(f"Last Sync: {timestamp}")

    def _on_launch_clicked(self, should_start):
        if should_start:
            install_dir = os.path.join(os.getcwd(), constants.DEFAULT_INSTALL_DIR)
            exe_path = self.controller.get_server_executable(install_dir)
            if exe_path:
                self.controller.run_server(exe_path)
            else:
                self.log("ERROR: Server executable not found.")
        else:
            if self.server_process:
                self.server_manager.stop_server(self.server_process)
                self.server_process = None
                self.log("Server stopped.")
                # Update UI state
                self.dashboard.control.set_running_state(False)

    def _on_server_started(self, pid):
        self.server_process = pid
        self.log(f"Server tracked with PID: {pid}")
        # Update UI state
        self.dashboard.control.set_running_state(True)

    def _on_nav_requested(self, nav_id):
        if nav_id in self.views:
            self.content_stack.setCurrentWidget(self.views[nav_id])

    def update_server_path(self, new_path: str):
        """Updates the installation path for all managers."""
        self.backup_manager.server_path = new_path
        self.save_sync_manager.server_path = new_path
        self.mod_manager.server_root = new_path
        
        # Update INI Manager
        ini_dir = os.path.join(new_path, "Icarus", "Saved", "Config", "WindowsServer")
        os.makedirs(ini_dir, exist_ok=True)
        ini_path = os.path.join(ini_dir, "ServerSettings.ini")
        self.ini_manager.file_path = ini_path
        self.ini_manager.load()
        
        # Refresh UI
        self.config_view.load_settings()
        self.mods_view.refresh_mod_list()
        self.log(f"Server path updated to: {new_path}")

    def log(self, message: str):
        self.console.log(message)

    def on_server_exit(self, result=None):
        self.server_process = None
        self.log("Server process exited.")
        self.dashboard.control.set_running_state(False)

    def show_error(self, message: str):
        self.log(f"ERROR: {message}")

    def reset_ui(self):
        pass

    def _create_placeholder(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #555555; background-color: rgba(20,20,20,200); border-radius: 20px; margin: 20px;")
        return label
