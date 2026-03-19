from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QCheckBox, QFrame,
    QScrollArea, QFormLayout, QTabWidget, QTextEdit,
    QFileDialog, QGridLayout
)
from PySide6.QtCore import Qt
import os
from icarus_sentinel import style_config, constants

class ConfigView(QWidget):
    """View for managing server configuration with Basic, Advanced, and Sentinel modes."""
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QVBoxLayout()
        header = QLabel("SERVER SETTINGS")
        header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 28px; background: transparent; letter-spacing: 1px;")
        sub_label = QLabel("Configure your dedicated server parameters and management rules.")
        sub_label.setStyleSheet("color: #666; font-family: 'Segoe UI'; font-size: 13px; font-weight: bold; background: transparent; margin-bottom: 10px;")
        header_layout.addWidget(header)
        header_layout.addWidget(sub_label)
        layout.addLayout(header_layout)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #444;
                background-color: rgba(20, 20, 20, 200);
                border-radius: 15px;
                margin-top: -1px;
            }}
            QTabBar::tab {{
                background-color: #222;
                color: #888;
                padding: 10px 20px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border: 1px solid #444;
                margin-right: 5px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: rgba(20, 20, 20, 200);
                color: {style_config.ACCENT_COLOR};
                border-bottom: none;
            }}
        """)
        
        self.basic_tab = self._create_basic_tab()
        self.sentinel_tab = self._create_sentinel_tab()
        self.advanced_tab = self._create_advanced_tab()
        
        self.tabs.addTab(self.basic_tab, "BASIC SETTINGS")
        self.tabs.addTab(self.sentinel_tab, "SENTINEL SETTINGS")
        self.tabs.addTab(self.advanced_tab, "ADVANCED INI EDITOR")
        
        layout.addWidget(self.tabs)

    def _create_basic_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        
        form_frame = QFrame()
        form_frame.setStyleSheet("border: none; background: transparent;")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        
        label_style = "color: #BBB; font-weight: bold; font-size: 13px;"
        input_style = """
            background-color: #111; 
            border: 1px solid #444; 
            border-radius: 5px; 
            color: #EEE; 
            padding: 8px;
            font-family: 'Segoe UI';
        """
        
        self.server_name_entry = QLineEdit()
        self.server_name_entry.setStyleSheet(input_style)
        
        self.server_password_entry = QLineEdit()
        self.server_password_entry.setEchoMode(QLineEdit.Password)
        self.server_password_entry.setStyleSheet(input_style)
        
        self.admin_password_entry = QLineEdit()
        self.admin_password_entry.setEchoMode(QLineEdit.Password)
        self.admin_password_entry.setStyleSheet(input_style)
        
        self.port_entry = QLineEdit()
        self.port_entry.setStyleSheet(input_style)
        
        self.query_port_entry = QLineEdit()
        self.query_port_entry.setStyleSheet(input_style)
        
        self.update_on_launch_cb = QCheckBox("Update Server on Launch")
        self.update_on_launch_cb.setStyleSheet("color: #DDD; font-weight: bold;")
        
        self.no_steam_cb = QCheckBox("Disable Steam Authentication (-NOSTEAM)")
        self.no_steam_cb.setStyleSheet("color: #DDD; font-weight: bold;")

        form_layout.addRow(self._create_label("SESSION NAME", label_style), self.server_name_entry)
        form_layout.addRow(self._create_label("JOIN PASSWORD", label_style), self.server_password_entry)
        form_layout.addRow(self._create_label("ADMIN PASSWORD", label_style), self.admin_password_entry)
        form_layout.addRow(self._create_label("SERVER PORT", label_style), self.port_entry)
        form_layout.addRow(self._create_label("QUERY PORT", label_style), self.query_port_entry)
        form_layout.addRow("", self.update_on_launch_cb)
        form_layout.addRow("", self.no_steam_cb)
        
        layout.addWidget(form_frame)
        
        self.save_btn = QPushButton("SAVE BASIC CONFIGURATION")
        self.save_btn.setFixedSize(280, 45)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #222;
                color: {style_config.ACCENT_COLOR};
                border: 1px solid {style_config.ACCENT_COLOR};
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {style_config.ACCENT_COLOR};
                color: black;
            }}
        """)
        layout.addWidget(self.save_btn, 0, Qt.AlignCenter)
        layout.addStretch()
        return tab

    def _create_sentinel_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 1. Path Selection
        path_frame = QFrame()
        path_layout = QHBoxLayout(path_frame)
        path_layout.setContentsMargins(0, 0, 0, 0)
        
        self.path_entry = QLineEdit()
        self.path_entry.setStyleSheet("background-color: #111; color: #EEE; border: 1px solid #444; padding: 8px; border-radius: 5px;")
        
        browse_btn = QPushButton("BROWSE")
        browse_btn.setFixedSize(100, 35)
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.clicked.connect(self._on_browse_path)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #333; 
                color: white; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #444;
                border: 1px solid #666;
            }
        """)
        
        path_layout.addWidget(QLabel("SERVER INSTALL PATH:"))
        path_layout.addWidget(self.path_entry)
        path_layout.addWidget(browse_btn)
        
        layout.addWidget(path_frame)

        # 2. Settings Grid
        grid_frame = QFrame()
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setSpacing(15)
        
        label_style = "color: #BBB; font-weight: bold; font-size: 12px;"
        input_style = "background-color: #111; color: #EEE; border: 1px solid #444; padding: 5px; border-radius: 3px;"

        self.ram_threshold_entry = QLineEdit()
        self.ram_threshold_entry.setFixedWidth(80)
        self.ram_threshold_entry.setStyleSheet(input_style)
        
        self.smart_restart_cb = QCheckBox("Enable Smart Idle Restart")
        self.smart_restart_cb.setStyleSheet("color: #DDD; font-weight: bold;")
        
        self.restart_time_entry = QLineEdit()
        self.restart_time_entry.setFixedWidth(80)
        self.restart_time_entry.setStyleSheet(input_style)
        
        self.backup_interval_entry = QLineEdit()
        self.backup_interval_entry.setFixedWidth(80)
        self.backup_interval_entry.setStyleSheet(input_style)
        
        self.retention_limit_entry = QLineEdit()
        self.retention_limit_entry.setFixedWidth(80)
        self.retention_limit_entry.setStyleSheet(input_style)

        grid_layout.addWidget(self._create_label("RAM THRESHOLD (GB):", label_style), 0, 0)
        grid_layout.addWidget(self.ram_threshold_entry, 0, 1)
        grid_layout.addWidget(self.smart_restart_cb, 1, 0, 1, 2)
        grid_layout.addWidget(self._create_label("RESTART TIME (HH:MM):", label_style), 2, 0)
        grid_layout.addWidget(self.restart_time_entry, 2, 1)
        grid_layout.addWidget(self._create_label("BACKUP INTERVAL (MIN):", label_style), 3, 0)
        grid_layout.addWidget(self.backup_interval_entry, 3, 1)
        grid_layout.addWidget(self._create_label("MAX BACKUPS:", label_style), 4, 0)
        grid_layout.addWidget(self.retention_limit_entry, 4, 1)
        
        layout.addWidget(grid_frame)

        # 3. Actions
        action_layout = QHBoxLayout()
        
        self.install_server_btn = QPushButton("INSTALL / UPDATE SERVER")
        self.install_server_btn.setFixedSize(220, 45)
        self.install_server_btn.setCursor(Qt.PointingHandCursor)
        self.install_server_btn.clicked.connect(self._on_install_server)
        self.install_server_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #333;
                color: #EEE;
                border: 1px solid #555;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #444;
            }}
        """)
        
        self.save_sentinel_btn = QPushButton("SAVE SENTINEL SETTINGS")
        self.save_sentinel_btn.setFixedSize(220, 45)
        self.save_sentinel_btn.setCursor(Qt.PointingHandCursor)
        self.save_sentinel_btn.clicked.connect(self._on_save_sentinel)
        self.save_sentinel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #222;
                color: {style_config.ACCENT_COLOR};
                border: 1px solid {style_config.ACCENT_COLOR};
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {style_config.ACCENT_COLOR};
                color: black;
            }}
        """)
        
        action_layout.addWidget(self.install_server_btn)
        action_layout.addStretch()
        action_layout.addWidget(self.save_sentinel_btn)
        layout.addLayout(action_layout)
        
        layout.addStretch()
        return tab

    def _create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        
        desc = QLabel("Edit ServerSettings.ini directly. Use with caution.")
        desc.setStyleSheet("color: #AAA; font-size: 12px; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        self.raw_ini_editor = QTextEdit()
        self.raw_ini_editor.setFontFamily(style_config.FONT_MONO[0])
        self.raw_ini_editor.setFontPointSize(10)
        self.raw_ini_editor.setStyleSheet("""
            background-color: #050505; 
            color: #FFA726; 
            border: 1px solid #444; 
            border-radius: 5px; 
            padding: 10px;
        """)
        layout.addWidget(self.raw_ini_editor)
        
        self.save_advanced_btn = QPushButton("SAVE ADVANCED CONFIGURATION")
        self.save_advanced_btn.setFixedSize(280, 45)
        self.save_advanced_btn.setCursor(Qt.PointingHandCursor)
        self.save_advanced_btn.clicked.connect(self.save_advanced_settings)
        self.save_advanced_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #222;
                color: {style_config.ACCENT_COLOR};
                border: 1px solid {style_config.ACCENT_COLOR};
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 15px;
            }}
            QPushButton:hover {{
                background-color: {style_config.ACCENT_COLOR};
                color: black;
            }}
        """)
        layout.addWidget(self.save_advanced_btn, 0, Qt.AlignCenter)
        return tab

    def _create_label(self, text, style):
        l = QLabel(text)
        l.setStyleSheet(style)
        return l

    def _on_browse_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Server Installation Directory")
        if directory:
            self.path_entry.setText(directory)
            if self.app:
                # Update managers with new path
                self.app.update_server_path(directory)

    def _on_install_server(self):
        if self.app:
            self.app.controller.run_install(self.path_entry.text())

    def _on_save_sentinel(self):
        if not self.app: return
        data = {
            "ram_threshold": self.ram_threshold_entry.text(),
            "smart_restart": self.smart_restart_cb.isChecked(),
            "restart_time": self.restart_time_entry.text(),
            "backup_interval": self.backup_interval_entry.text(),
            "retention_limit": self.retention_limit_entry.text()
        }
        self.app.controller.save_sentinel_settings(data)

    def load_settings(self):
        if not self.app: return
        
        # Basic
        if self.app.ini_manager:
            ini = self.app.ini_manager
            self.server_name_entry.setText(ini.get_setting("SessionName") or constants.DEFAULT_SERVER_NAME)
            self.server_password_entry.setText(ini.get_setting("ServerPassword") or "")
            self.admin_password_entry.setText(ini.get_setting("AdminPassword") or "")
            self.port_entry.setText(ini.get_setting("Port") or constants.DEFAULT_PORT)
            self.query_port_entry.setText(ini.get_setting("QueryPort") or constants.DEFAULT_QUERY_PORT)
            update_val = ini.get_setting("UpdateOnLaunch", section=constants.SECTION_SENTINEL)
            self.update_on_launch_cb.setChecked(update_val == "True")
            no_steam_val = ini.get_setting("NoSteam", section=constants.SECTION_SENTINEL)
            self.no_steam_cb.setChecked(no_steam_val == "True")
            self.raw_ini_editor.setPlainText(ini.get_raw_text())

        # Sentinel
        sm = self.app.server_manager
        bm = self.app.backup_manager
        self.path_entry.setText(bm.server_path)
        self.ram_threshold_entry.setText(str(sm.ram_threshold_gb))
        self.smart_restart_cb.setChecked(sm.smart_restart_enabled)
        self.restart_time_entry.setText(sm.smart_restart_time)
        self.backup_interval_entry.setText(str(int(bm.interval_minutes)))
        self.retention_limit_entry.setText(str(bm.retention_limit))

    def save_settings(self):
        if not self.app or not self.app.ini_manager: return
        ini = self.app.ini_manager
        ini.set_setting("SessionName", self.server_name_entry.text())
        ini.set_setting("ServerPassword", self.server_password_entry.text())
        if self.admin_password_entry.text():
            ini.set_setting("AdminPassword", self.admin_password_entry.text())
        ini.set_setting("Port", self.port_entry.text())
        ini.set_setting("QueryPort", self.query_port_entry.text())
        ini.set_setting("UpdateOnLaunch", str(self.update_on_launch_cb.isChecked()), section=constants.SECTION_SENTINEL)
        ini.set_setting("NoSteam", str(self.no_steam_cb.isChecked()), section=constants.SECTION_SENTINEL)
        ini.save()
        self.app.log("Basic configuration saved.")
        self.raw_ini_editor.setPlainText(ini.get_raw_text())

    def save_advanced_settings(self):
        if not self.app or not self.app.ini_manager: return
        ini = self.app.ini_manager
        raw_text = self.raw_ini_editor.toPlainText()
        if raw_text.strip():
            ini.save_raw_text(raw_text)
            self.app.log("Advanced configuration saved.")
            self.load_settings()
