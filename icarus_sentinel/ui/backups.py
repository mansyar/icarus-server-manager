from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton, QFrame, QListWidget
)
from PySide6.QtCore import Qt
from icarus_sentinel import style_config

class BackupsView(QWidget):
    """View for managing server backups."""
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        self.container = QFrame()
        self.container.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(20, 20, 20, 200);
                border: 1px solid #444;
                border-radius: 20px;
            }}
        """)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("SERVER BACKUPS")
        header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 24px; border: none; background: transparent;")
        container_layout.addWidget(header)
        
        desc = QLabel("Automated backups are running in the background.")
        desc.setStyleSheet("color: #AAA; font-size: 13px; border: none; background: transparent;")
        container_layout.addWidget(desc)
        
        # Placeholder List
        self.backup_list = QListWidget()
        self.backup_list.setStyleSheet("""
            background-color: #111; 
            border: 1px solid #333; 
            border-radius: 10px;
            color: #EEE;
            padding: 10px;
        """)
        container_layout.addWidget(self.backup_list)
        
        self.refresh_btn = QPushButton("REFRESH BACKUPS")
        self.refresh_btn.setFixedSize(200, 40)
        self.refresh_btn.setStyleSheet(f"background-color: #222; color: {style_config.ACCENT_COLOR}; border: 1px solid {style_config.ACCENT_COLOR}; border-radius: 5px;")
        container_layout.addWidget(self.refresh_btn, 0, Qt.AlignCenter)
        
        layout.addWidget(self.container)
