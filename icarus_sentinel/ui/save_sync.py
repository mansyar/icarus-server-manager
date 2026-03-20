from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton, QFrame, QComboBox, QHBoxLayout
)
from PySide6.QtCore import Qt
from icarus_sentinel import style_config
from icarus_sentinel.ui.components import ToggleSwitch

class SaveSyncView(QWidget):
    """View for managing bidirectional save synchronization."""
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        self.refresh_steam_ids()
        self.load_settings()
        
        # Connect signals after initial load to avoid overwriting settings
        self.steam_id_dropdown.currentTextChanged.connect(self._on_settings_changed)
        self.sync_on_start_toggle.clicked.connect(self._on_settings_changed)
        self.sync_on_stop_toggle.clicked.connect(self._on_settings_changed)

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
        
        header = QLabel("SAVE SYNCHRONIZATION")
        header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 24px; border: none; background: transparent;")
        container_layout.addWidget(header)
        
        desc = QLabel("Sync your local characters and prospects with the dedicated server.")
        desc.setStyleSheet("color: #AAA; font-size: 13px; border: none; background: transparent; margin-bottom: 20px;")
        container_layout.addWidget(desc)
        
        # SteamID Selection
        self.id_label = QLabel("SELECT STEAM ID")
        self.id_label.setStyleSheet("color: #BBB; font-weight: bold; font-size: 12px; background: transparent; border: none;")
        container_layout.addWidget(self.id_label)
        
        self.steam_id_dropdown = QComboBox()
        self.steam_id_dropdown.setFixedHeight(40)
        self.steam_id_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #111; 
                border: 1px solid #444; 
                border-radius: 5px;
                color: #EEE;
                padding-left: 10px;
            }
            QComboBox::drop-down { border: none; }
        """)
        container_layout.addWidget(self.steam_id_dropdown)
        
        container_layout.addSpacing(20)
        
        # SYNC AUTOMATION Section
        auto_header = QLabel("SYNC AUTOMATION")
        auto_header.setStyleSheet("color: #BBB; font-weight: bold; font-size: 12px; background: transparent; border: none; margin-bottom: 5px;")
        container_layout.addWidget(auto_header)

        self.automation_frame = QFrame()
        self.automation_frame.setStyleSheet("background: transparent; border: none;")
        auto_layout = QVBoxLayout(self.automation_frame)
        auto_layout.setContentsMargins(0, 0, 0, 0)
        auto_layout.setSpacing(15)

        # Sync on Start
        start_layout = QHBoxLayout()
        start_label = QLabel("Auto-Sync on Server Start (Local -> Server)")
        start_label.setStyleSheet("color: #EEE; font-size: 13px; background: transparent;")
        self.sync_on_start_toggle = ToggleSwitch()
        start_layout.addWidget(start_label)
        start_layout.addStretch()
        start_layout.addWidget(self.sync_on_start_toggle)
        auto_layout.addLayout(start_layout)

        # Sync on Stop
        stop_layout = QHBoxLayout()
        stop_label = QLabel("Auto-Sync on Server Stop (Server -> Local)")
        stop_label.setStyleSheet("color: #EEE; font-size: 13px; background: transparent;")
        self.sync_on_stop_toggle = ToggleSwitch()
        stop_layout.addWidget(stop_label)
        stop_layout.addStretch()
        stop_layout.addWidget(self.sync_on_stop_toggle)
        auto_layout.addLayout(stop_layout)

        container_layout.addWidget(self.automation_frame)
        container_layout.addSpacing(30)
        
        self.sync_btn = QPushButton("PERFORM BIDIRECTIONAL SYNC NOW")
        self.sync_btn.setFixedSize(300, 50)
        self.sync_btn.setCursor(Qt.PointingHandCursor)
        self.sync_btn.clicked.connect(self.perform_sync)
        self.sync_btn.setStyleSheet(f"""
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
        container_layout.addWidget(self.sync_btn, 0, Qt.AlignCenter)
        
        self.last_sync_label = QLabel("Last Sync: Never")
        self.last_sync_label.setStyleSheet("color: #666; font-size: 11px; border: none; background: transparent; margin-top: 10px;")
        container_layout.addWidget(self.last_sync_label, 0, Qt.AlignCenter)
        
        container_layout.addStretch()
        layout.addWidget(self.container)

    def load_settings(self):
        if not self.app or not self.app.server_manager: return
        sm = self.app.server_manager
        self.sync_on_start_toggle.setChecked(sm.auto_sync_on_start)
        self.sync_on_stop_toggle.setChecked(sm.auto_sync_on_stop)
        
        index = self.steam_id_dropdown.findText(sm.selected_steam_id or "")
        if index >= 0:
            self.steam_id_dropdown.setCurrentIndex(index)

    def _on_settings_changed(self):
        if not self.app or not self.app.server_manager: return
        sm = self.app.server_manager
        sm.auto_sync_on_start = self.sync_on_start_toggle.isChecked()
        sm.auto_sync_on_stop = self.sync_on_stop_toggle.isChecked()
        sm.selected_steam_id = self.steam_id_dropdown.currentText()
        sm.save_state()

    def refresh_steam_ids(self):
        if not self.app or not self.app.save_sync_manager: return
        ids = self.app.save_sync_manager.list_local_steam_ids()
        self.steam_id_dropdown.clear()
        self.steam_id_dropdown.addItems(ids)
        
        last_sync = self.app.server_manager.state.get("last_sync_timestamp")
        if last_sync:
            self.last_sync_label.setText(f"Last Sync: {last_sync}")

    def perform_sync(self):
        steam_id = self.steam_id_dropdown.currentText()
        if not steam_id:
            self.app.log("ERROR: No SteamID selected for sync.")
            return
        
        self.sync_btn.setEnabled(False)
        self.sync_btn.setText("SYNCING...")
        
        def on_done():
            self.sync_btn.setEnabled(True)
            self.sync_btn.setText("PERFORM BIDIRECTIONAL SYNC")
            self.refresh_steam_ids()
            
        self.app.controller.sync_saves(steam_id, callback=on_done)
