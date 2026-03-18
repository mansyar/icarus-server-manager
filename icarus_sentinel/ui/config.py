from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QCheckBox, QFrame,
    QScrollArea, QFormLayout
)
from PySide6.QtCore import Qt
from icarus_sentinel import style_config, constants

class ConfigView(QWidget):
    """View for managing server configuration."""
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Container
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
        
        # Header
        header = QLabel("SERVER SETTINGS")
        header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 24px; border: none; background: transparent;")
        container_layout.addWidget(header)
        
        # Form
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
        self.update_on_launch_cb.setStyleSheet("color: #BBB; font-weight: bold;")
        
        self.no_steam_cb = QCheckBox("Disable Steam Authentication (-NOSTEAM)")
        self.no_steam_cb.setStyleSheet("color: #BBB; font-weight: bold;")

        form_layout.addRow(self._create_label("SESSION NAME", label_style), self.server_name_entry)
        form_layout.addRow(self._create_label("JOIN PASSWORD", label_style), self.server_password_entry)
        form_layout.addRow(self._create_label("ADMIN PASSWORD", label_style), self.admin_password_entry)
        form_layout.addRow(self._create_label("SERVER PORT", label_style), self.port_entry)
        form_layout.addRow(self._create_label("QUERY PORT", label_style), self.query_port_entry)
        form_layout.addRow("", self.update_on_launch_cb)
        form_layout.addRow("", self.no_steam_cb)
        
        container_layout.addWidget(form_frame)
        
        # Save Button
        self.save_btn = QPushButton("SAVE CONFIGURATION")
        self.save_btn.setFixedSize(250, 45)
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
        container_layout.addWidget(self.save_btn, 0, Qt.AlignCenter)
        container_layout.addStretch()
        
        layout.addWidget(self.container)

    def _create_label(self, text, style):
        l = QLabel(text)
        l.setStyleSheet(style)
        return l

    def load_settings(self):
        if not self.app or not self.app.ini_manager: return
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
        self.app.log("Configuration saved successfully.")
