from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import icarus_sentinel.ui.resources_rc
from icarus_sentinel import style_config
from icarus_sentinel.core.sys_info import get_app_version, get_system_info

# Pure QSS Industrial Style Helper
PANEL_STYLE = f"""
    background-color: rgba(30, 30, 30, 240);
    border: 1px solid #555;
    border-top: 1px solid #777;
    border-left: 1px solid #666;
    border-radius: 12px;
"""

class AboutView(QWidget):
    """The About view displaying app version, credits, and system info."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Initializes the UI components and layout for the About view."""
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        
        self.main_container = QFrame()
        self.main_container.setObjectName("AboutContainer")
        self.main_container.setStyleSheet(f"""
            QFrame#AboutContainer {{
                background-color: rgba(15, 15, 15, 230);
                border: 1px solid #444;
                border-radius: 25px;
            }}
        """)
        
        layout = QVBoxLayout(self.main_container)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)

        # Header
        header_h_layout = QHBoxLayout()
        header_h_layout.setSpacing(25)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap(":/icons/app_icon.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_label.setStyleSheet("background: transparent; border: none;")
        
        header_text_layout = QVBoxLayout()
        self.title_label = QLabel("ICARUS SENTINEL")
        self.title_label.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 32px; background: transparent; letter-spacing: 2px;")
        
        version = get_app_version()
        self.version_label = QLabel(f"VERSION: {version}")
        self.version_label.setStyleSheet("color: #999; font-family: 'Segoe UI'; font-size: 14px; font-weight: bold; background: transparent;")
        
        header_text_layout.addWidget(self.title_label)
        header_text_layout.addWidget(self.version_label)
        
        header_h_layout.addWidget(self.icon_label)
        header_h_layout.addLayout(header_text_layout)
        header_h_layout.addStretch()
        
        layout.addLayout(header_h_layout)

        # Content Panels
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Credits Panel
        credits_panel = QFrame()
        credits_panel.setStyleSheet(PANEL_STYLE)
        credits_layout = QVBoxLayout(credits_panel)
        credits_layout.setContentsMargins(20, 20, 20, 20)
        
        credits_header = QLabel("DEVELOPER CREDITS")
        credits_header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 14px; border: none; background: transparent;")       
        
        self.credits_label = QLabel("Icarus Sentinel Team\n\nLead Developer: Ansyar\nContributors: Open Source Community")
        self.credits_label.setStyleSheet("color: #EEE; font-family: 'Segoe UI'; font-size: 12px; border: none; background: transparent;")
        self.credits_label.setWordWrap(True)
        
        credits_layout.addWidget(credits_header)
        credits_layout.addWidget(self.credits_label)
        credits_layout.addStretch()
        
        # System Info Panel
        sys_info_panel = QFrame()
        sys_info_panel.setStyleSheet(PANEL_STYLE)
        sys_info_layout = QVBoxLayout(sys_info_panel)
        sys_info_layout.setContentsMargins(20, 20, 20, 20)
        
        sys_header = QLabel("SYSTEM ENVIRONMENT")
        sys_header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 14px; border: none; background: transparent;")
        
        sys_info = get_system_info()
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        def add_info_row(label_text, value_text, row):
            l = QLabel(label_text)
            l.setStyleSheet("color: #888; font-family: 'Segoe UI'; font-size: 11px; font-weight: bold; border: none; background: transparent;")
            v = QLabel(value_text)
            v.setStyleSheet("color: #EEE; font-family: 'Segoe UI'; font-size: 12px; border: none; background: transparent;")
            grid.addWidget(l, row, 0)
            grid.addWidget(v, row, 1)
            return v

        self.os_label = add_info_row("OPERATING SYSTEM:", sys_info["os"], 0)
        self.cpu_label = add_info_row("CPU ARCHITECTURE:", sys_info["cpu"], 1)
        self.ram_label = add_info_row("TOTAL SYSTEM RAM:", sys_info["ram"], 2)
        
        sys_info_layout.addWidget(sys_header)
        sys_info_layout.addLayout(grid)
        sys_info_layout.addStretch()

        content_layout.addWidget(credits_panel, 1)
        content_layout.addWidget(sys_info_panel, 1)
        
        layout.addLayout(content_layout)
        layout.addStretch()

        self.outer_layout.addWidget(self.main_container)
