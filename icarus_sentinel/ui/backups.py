from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt, QSize
import os
from icarus_sentinel import style_config

class BackupsView(QWidget):
    """View for managing server backups."""
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        
        if self.app and self.app.controller:
            self.app.controller.backups_updated.connect(self.refresh_backups)
        
        self.refresh_backups()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        self.container = QFrame()
        self.container.setObjectName("BackupsContainer")
        self.container.setStyleSheet(f"""
            QFrame#BackupsContainer {{
                background-color: rgba(20, 20, 20, 230);
                border: 1px solid #444;
                border-radius: 25px;
            }}
        """)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(15)
        
        # Header
        header = QLabel("SERVER BACKUPS")
        header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 28px; border: none; background: transparent;")
        container_layout.addWidget(header)
        
        desc = QLabel("Restore previous server states or create a manual backup.")
        desc.setStyleSheet("color: #EEE; font-family: 'Segoe UI'; font-size: 13px; font-weight: bold; border: none; background: transparent; margin-bottom: 10px;")
        container_layout.addWidget(desc)
        
        # Action Row (Backup Now + Refresh)
        action_layout = QHBoxLayout()
        
        self.backup_now_btn = QPushButton("BACKUP CURRENT STATE")
        self.backup_now_btn.setFixedSize(250, 45)
        self.backup_now_btn.setCursor(Qt.PointingHandCursor)
        self.backup_now_btn.clicked.connect(self._on_backup_now)
        self.backup_now_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #222;
                color: {style_config.ACCENT_COLOR};
                border: 2px solid {style_config.ACCENT_COLOR};
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {style_config.ACCENT_COLOR};
                color: black;
            }}
        """)
        
        self.refresh_btn = QPushButton("REFRESH LIST")
        self.refresh_btn.setFixedSize(150, 45)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.refresh_backups)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: #DDD;
                border: 1px solid #555;
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #444;
                color: white;
            }
        """)
        
        action_layout.addWidget(self.backup_now_btn)
        action_layout.addStretch()
        action_layout.addWidget(self.refresh_btn)
        container_layout.addLayout(action_layout)
        
        # Available Backups List
        list_header = QLabel("AVAILABLE BACKUPS")
        list_header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 14px; margin-top: 20px; background: transparent; border: none;")
        container_layout.addWidget(list_header)

        self.backup_list = QListWidget()
        self.backup_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 180); 
                border: 1px solid #333; 
                border-radius: 15px;
                color: #EEE;
                padding: 10px;
            }
            QListWidget::item {
                border-bottom: 1px solid #222;
            }
            QListWidget::item:selected {
                background-color: rgba(255, 140, 0, 20);
            }
        """)
        container_layout.addWidget(self.backup_list)
        
        layout.addWidget(self.container)

    def _on_backup_now(self):
        if self.app:
            self.app.controller.run_backup()

    def refresh_backups(self):
        if not self.app or not self.app.backup_manager: return
        self.backup_list.clear()
        
        backup_path = self.app.backup_manager.backup_path
        if not os.path.exists(backup_path):
            return
            
        backups = [f for f in os.listdir(backup_path) if f.startswith("Prospects_") and f.endswith(".zip")]
        backups.sort(reverse=True)
        
        for b in backups:
            item = QListWidgetItem()
            self.backup_list.addItem(item)
            
            # Row Widget
            row_widget = QWidget()
            row_widget.setMinimumHeight(50) # Ensure enough height
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(15, 5, 15, 5)
            
            try: 
                display_name = b.replace("Prospects_", "").replace(".zip", "").replace("_", " ")
            except: 
                display_name = b
                
            name_label = QLabel(display_name)
            name_label.setStyleSheet("color: #EEE; font-size: 14px; font-weight: bold; border: none; background: transparent;")
            
            restore_btn = QPushButton("RESTORE")
            restore_btn.setFixedSize(100, 30)
            restore_btn.setCursor(Qt.PointingHandCursor)
            # Use functools.partial or default arg to capture 'b' correctly in lambda
            restore_btn.clicked.connect(lambda checked=False, name=b: self._confirm_restore(name))
            restore_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #222;
                    color: {style_config.ACCENT_COLOR};
                    border: 1px solid {style_config.ACCENT_COLOR};
                    border-radius: 5px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {style_config.ACCENT_COLOR};
                    color: black;
                }}
            """)
            
            row_layout.addWidget(name_label)
            row_layout.addStretch()
            row_layout.addWidget(restore_btn)
            
            item.setSizeHint(row_widget.sizeHint())
            self.backup_list.setItemWidget(item, row_widget)

    def _confirm_restore(self, backup_name):
        msg = f"Are you sure you want to restore '{backup_name}'?\n\nThis will OVERWRITE your current progress. This action cannot be undone."
        reply = QMessageBox.question(self, "Confirm Restore", msg, QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.app:
                self.app.controller.run_restore(backup_name)
