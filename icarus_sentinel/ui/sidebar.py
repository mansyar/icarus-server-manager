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
        self.setFixedWidth(220)
        self.setObjectName("Sidebar")
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 30, 15, 30)
        layout.setSpacing(12)

        # Logo with Accent Line
        self.logo_container = QWidget()
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 20)
        
        logo_label = QLabel("ICARUS\nSENTINEL")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"""
            color: {style_config.ACCENT_COLOR}; 
            font-family: 'Segoe UI Black', sans-serif;
            font-weight: bold; 
            font-size: 22px; 
            letter-spacing: 2px;
        """)
        
        accent_line = QFrame()
        accent_line.setFixedHeight(2)
        accent_line.setStyleSheet(f"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.5 {style_config.ACCENT_COLOR}, stop:1 transparent);")
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(accent_line)
        layout.addWidget(self.logo_container)

        # Navigation Buttons
        self.dashboard_btn = self._create_nav_btn("Dashboard", "dashboard", "icon_dashboard.PNG")
        self.settings_btn = self._create_nav_btn("Server Settings", "settings", "icon_settings.PNG")
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
        btn.setFixedHeight(45)
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
                background-color: transparent;
                border: none;
            }}
            QPushButton {{
                color: #DDDDDD;
                background-color: rgba(50, 50, 50, 180);
                border: 1px solid #444;
                border-radius: 10px;
                text-align: left;
                padding-left: 15px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: rgba(60, 60, 60, 200);
                color: white;
                border-color: #555;
            }}
            QPushButton:checked {{
                background-color: rgba(255, 140, 0, 20);
                color: {style_config.ACCENT_COLOR};
                border: 2px solid {style_config.ACCENT_COLOR};
                font-weight: bold;
            }}
        """)
