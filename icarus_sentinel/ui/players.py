from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame)
from PySide6.QtCore import Qt
from icarus_sentinel import style_config

class PlayersView(QWidget):
    """View for displaying real-time player activity."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PlayersView")
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("CONNECTED PLAYERS")
        title_label.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.status_label = QLabel("Server: Unknown")
        self.status_label.setStyleSheet("color: #888; font-size: 14px;")
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)

        # Players Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["NAME", "PLAYTIME", "SCORE"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)

        # Offline/Empty Placeholder (Hidden by default)
        self.placeholder = QLabel("Server is currently unreachable or no players are connected.")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: #666; font-size: 16px; font-style: italic;")
        self.placeholder.setVisible(False)
        layout.addWidget(self.placeholder)

    def update_data(self, data):
        """Updates the table with new A2S data."""
        status = data.get("status", "Offline")
        server_name = data.get("server_name", "Unknown")
        players = data.get("players", [])
        
        self.status_label.setText(f"Server: {server_name} ({status})")
        
        if status == "Offline":
            self.table.setVisible(False)
            self.placeholder.setText("Server is currently unreachable.")
            self.placeholder.setVisible(True)
            return

        if not players:
            self.table.setVisible(False)
            self.placeholder.setText("No players currently connected.")
            self.placeholder.setVisible(True)
            return

        self.placeholder.setVisible(False)
        self.table.setVisible(True)
        
        self.table.setRowCount(len(players))
        for row, p in enumerate(players):
            self.table.setItem(row, 0, QTableWidgetItem(p["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(p["playtime"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(p["score"])))

    def apply_styles(self):
        self.setStyleSheet(f"""
            QWidget#PlayersView {{
                background-color: {style_config.APP_BG};
            }}
            QTableWidget {{
                background-color: {style_config.FRAME_BG};
                color: {style_config.TEXT_PRIMARY};
                border: 1px solid #444;
                border-radius: {style_config.CORNER_RADIUS}px;
                gridline-color: #333;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 10px;
            }}
            QHeaderView::section {{
                background-color: #333;
                color: #AAA;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }}
            QTableWidget::item:selected {{
                background-color: rgba(255, 140, 0, 40);
                color: {style_config.ACCENT_COLOR};
            }}
        """)
