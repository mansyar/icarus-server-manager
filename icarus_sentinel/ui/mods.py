from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QCheckBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import os
from icarus_sentinel import style_config

class ModsView(QWidget):
    """View for managing server mods."""
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        
        if self.app and self.app.controller:
            self.app.controller.mods_updated.connect(self.refresh_mod_list)
            
        self.refresh_mod_list()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        self.container = QFrame()
        self.container.setObjectName("ModsContainer")
        self.container.setStyleSheet(f"""
            QFrame#ModsContainer {{
                background-color: rgba(20, 20, 20, 230);
                border: 1px solid #444;
                border-radius: 25px;
            }}
        """)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(15)
        
        # Header
        header = QLabel("MOD MANAGEMENT")
        header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 28px; border: none; background: transparent;")
        container_layout.addWidget(header)
        
        desc = QLabel("Clients MUST have the exact same .pak files to join without crashing.")
        desc.setStyleSheet("color: #FF5252; font-family: 'Segoe UI'; font-size: 13px; font-weight: bold; border: none; background: transparent; margin-bottom: 10px;")
        container_layout.addWidget(desc)
        
        # Action Row
        action_layout = QHBoxLayout()
        
        self.install_btn = QPushButton("INSTALL MOD (.PAK / .ZIP)")
        self.install_btn.setFixedSize(250, 45)
        self.install_btn.setCursor(Qt.PointingHandCursor)
        self.install_btn.clicked.connect(self._on_install_clicked)
        self.install_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #222;
                color: {style_config.ACCENT_COLOR};
                border: 2px solid {style_config.ACCENT_COLOR};
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {style_config.ACCENT_COLOR};
                color: black;
            }}
        """)
        
        self.select_all_cb = QCheckBox("SELECT ALL")
        self.select_all_cb.setStyleSheet("color: #DDD; font-weight: bold; font-size: 12px;")
        self.select_all_cb.stateChanged.connect(self._on_select_all_changed)
        
        self.refresh_btn = QPushButton("REFRESH")
        self.refresh_btn.setFixedSize(100, 45)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.refresh_mod_list)
        self.refresh_btn.setStyleSheet("background-color: #333; color: #DDD; border: 1px solid #555; border-radius: 10px; font-weight: bold;")
        
        action_layout.addWidget(self.install_btn)
        action_layout.addSpacing(20)
        action_layout.addWidget(self.select_all_cb)
        action_layout.addStretch()
        action_layout.addWidget(self.refresh_btn)
        container_layout.addLayout(action_layout)
        
        # Mod List
        list_header = QLabel("INSTALLED MODS")
        list_header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 14px; margin-top: 10px; background: transparent; border: none;")
        container_layout.addWidget(list_header)

        self.mod_list = QListWidget()
        self.mod_list.setStyleSheet("""
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
        """)
        container_layout.addWidget(self.mod_list)
        
        # Bottom Actions
        self.remove_btn = QPushButton("REMOVE SELECTED MODS")
        self.remove_btn.setFixedSize(250, 45)
        self.remove_btn.setCursor(Qt.PointingHandCursor)
        self.remove_btn.clicked.connect(self._on_remove_clicked)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #300;
                color: #FF5252;
                border: 2px solid #FF5252;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FF5252;
                color: black;
            }
        """)
        container_layout.addWidget(self.remove_btn, 0, Qt.AlignLeft)
        
        layout.addWidget(self.container)

    def _on_install_clicked(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Mod Files", "", "Mod Files (*.pak *.zip)"
        )
        if file_paths and self.app:
            self.app.controller.run_mod_install(file_paths)

    def _on_remove_clicked(self):
        to_remove = []
        for i in range(self.mod_list.count()):
            item = self.mod_list.item(i)
            checkbox = self.mod_list.itemWidget(item)
            if checkbox and checkbox.isChecked():
                to_remove.append(checkbox.text())
        
        if not to_remove:
            return
            
        msg = f"Are you sure you want to remove {len(to_remove)} mod(s)?"
        reply = QMessageBox.question(self, "Confirm Removal", msg, QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes and self.app:
            self.app.controller.run_mod_remove(to_remove)

    def _on_select_all_changed(self, state):
        # In PySide6, state is an integer (0=Unchecked, 2=Checked)
        is_checked = (state == Qt.CheckState.Checked.value or state == 2)
        
        # Block signals to prevent any potential recursion
        self.mod_list.blockSignals(True)
        for i in range(self.mod_list.count()):
            item = self.mod_list.item(i)
            widget = self.mod_list.itemWidget(item)
            if isinstance(widget, QCheckBox):
                widget.setChecked(is_checked)
        self.mod_list.blockSignals(False)

    def refresh_mod_list(self):
        if not self.app or not self.app.mod_manager: return
        self.mod_list.clear()
        
        mods = self.app.mod_manager.list_mods()
        if not mods:
            item = QListWidgetItem("No mods installed.")
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor("#666"))
            self.mod_list.addItem(item)
            self.select_all_cb.setEnabled(False)
            return
            
        self.select_all_cb.setEnabled(True)
        self.select_all_cb.setChecked(False)
        
        for m in mods:
            item = QListWidgetItem()
            self.mod_list.addItem(item)
            
            cb = QCheckBox(m)
            cb.setStyleSheet("color: #EEE; font-size: 13px; font-weight: 500; padding: 10px; border: none; background: transparent;")
            
            item.setSizeHint(cb.sizeHint())
            self.mod_list.setItemWidget(item, cb)
