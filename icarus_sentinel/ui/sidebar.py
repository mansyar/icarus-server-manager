from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
import os
from icarus_sentinel import style_config

class SidebarWidget(QFrame):
    """Sidebar navigation widget for Icarus Sentinel."""
    nav_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setObjectName("Sidebar")
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(5)

        # Logo
        logo_label = QLabel("ICARUS\nSENTINEL")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-weight: bold; font-size: 20px; margin-bottom: 20px;")
        layout.addWidget(logo_label)

        # Navigation Buttons
        self.dashboard_btn = self._create_nav_btn("Dashboard", "dashboard", "icon_dashboard.PNG")
        self.settings_btn = self._create_nav_btn("Configuration", "settings", "icon_settings.PNG")
        self.backups_btn = self._create_nav_btn("Backups", "backups", "icon_backup.PNG")
        self.sync_btn = self._create_nav_btn("Save Sync", "sync", "icon__save_sync.PNG")
        self.mods_btn = self._create_nav_btn("Mods", "mods", "icon_mods.PNG")

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.backups_btn)
        layout.addWidget(self.sync_btn)
        layout.addWidget(self.mods_btn)

        layout.addStretch()

    def _create_nav_btn(self, text, nav_id, icon_name):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setFixedHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Load Icon
        icon_path = os.path.join("assets", icon_name)
        if os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            
        btn.clicked.connect(lambda: self.nav_requested.emit(nav_id))
        return btn

    def apply_styles(self):
        self.setStyleSheet(f"""
            QFrame#Sidebar {{
                background-color: {style_config.SIDEBAR_BG};
                border: none;
            }}
            QPushButton {{
                color: #A0A0A0;
                background-color: transparent;
                border: none;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #2A2A2A;
                color: {style_config.TEXT_PRIMARY};
            }}
            QPushButton:checked {{
                background-color: #333333;
                color: {style_config.ACCENT_COLOR};
                border-left: 3px solid {style_config.ACCENT_COLOR};
            }}
        """)
