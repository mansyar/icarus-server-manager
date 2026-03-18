from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QProgressBar, QFrame,
    QGridLayout
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QPalette, QBrush, QColor
import os
from icarus_sentinel import style_config

class MetricsWidget(QFrame):
    """Displays CPU and RAM metrics with an industrial look."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MetricsPanel")
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout(self)
        
        self.cpu_label = QLabel("CPU USAGE: 0.0%")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setFixedHeight(15)

        self.ram_label = QLabel("RAM USAGE: 0.0GB / 0.0GB")
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setTextVisible(False)
        self.ram_bar.setFixedHeight(15)

        layout.addWidget(self.cpu_label, 0, 0)
        layout.addWidget(self.cpu_bar, 1, 0)
        layout.addWidget(self.ram_label, 2, 0)
        layout.addWidget(self.ram_bar, 3, 0)

        self.setStyleSheet(f"""
            QFrame#MetricsPanel {{
                background-color: rgba(30, 30, 30, 200);
                border: 2px solid #444;
                border-radius: 5px;
                padding: 10px;
            }}
            QLabel {{
                color: {style_config.ACCENT_COLOR};
                font-family: 'Segoe UI Black', sans-serif;
                font-size: 12px;
                text-transform: uppercase;
            }}
            QProgressBar {{
                background-color: #111;
                border: 1px solid #555;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff4500, stop:1 #ff8c00);
            }}
        """)

    def update_metrics(self, cpu: float, ram: float, total_ram: float = 16.0):
        self.cpu_label.setText(f"CPU USAGE: {cpu:.1f}%")
        self.cpu_bar.setValue(int(cpu))
        self.ram_label.setText(f"RAM USAGE: {ram:.1f}GB / {total_ram:.1f}GB")
        self.ram_bar.setValue(int((ram / total_ram) * 100) if total_ram > 0 else 0)

class ControlWidget(QFrame):
    """The main orbital launch control panel."""
    action_triggered = Signal(bool) # True for start, False for stop

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ControlPanel")
        self.is_running = False
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.launch_btn = QPushButton("INITIATE ORBITAL LAUNCH")
        self.launch_btn.setFixedSize(300, 80)
        self.launch_btn.setCursor(Qt.PointingHandCursor)
        self.launch_btn.clicked.connect(self._on_click)
        
        # Rocket Icon Label
        self.status_icon = QLabel()
        icon_path = os.path.join("assets", "rocket.PNG")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.status_icon.setPixmap(pixmap)
        self.status_icon.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.status_icon)
        layout.addWidget(self.launch_btn)

        self.apply_styles()

    def apply_styles(self):
        # Using a border-image for the caution stripe would be ideal, 
        # but for now we use QSS with background-color fallback.
        caution_path = os.path.join("assets", "caution_stripe.png").replace("\\", "/")
        
        self.setStyleSheet(f"""
            QFrame#ControlPanel {{
                background: transparent;
            }}
            QPushButton {{
                background-image: url({caution_path});
                background-repeat: repeat-x;
                border: 4px solid #333;
                border-radius: 10px;
                color: white;
                font-family: 'Segoe UI Black', sans-serif;
                font-size: 18px;
                font-weight: bold;
                text-shadow: 2px 2px black;
            }}
            QPushButton:hover {{
                border-color: {style_config.ACCENT_COLOR};
            }}
            QPushButton:pressed {{
                padding-top: 5px;
                padding-left: 5px;
            }}
        """)

    def _on_click(self):
        self.is_running = not self.is_running
        self.action_triggered.emit(self.is_running)
        if self.is_running:
            self.launch_btn.setText("ABORT MISSION")
            self.launch_btn.setStyleSheet(self.launch_btn.styleSheet() + "QPushButton { color: #ff4444; }")
        else:
            self.launch_btn.setText("INITIATE ORBITAL LAUNCH")
            self.launch_btn.setStyleSheet(self.launch_btn.styleSheet() + "QPushButton { color: white; }")

class ConsoleWidget(QFrame):
    """The persistent log terminal."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ConsolePanel")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setUndoRedoEnabled(False)
        self.text_area.setFontFamily(style_config.FONT_MONO[0])
        self.text_area.setFontPointSize(style_config.FONT_MONO[1])
        
        layout.addWidget(self.text_area)

        self.setStyleSheet(f"""
            QFrame#ConsolePanel {{
                background-color: {style_config.CONSOLE_BG};
                border: 2px solid #333;
                border-radius: 5px;
            }}
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {style_config.CONSOLE_TEXT};
            }}
        """)

    def log(self, message: str):
        self.text_area.append(message)
        # Scroll to bottom
        self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())

class DashboardView(QWidget):
    """The main high-fidelity dashboard view."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_background()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Upper row: Metrics and Controls
        upper_layout = QHBoxLayout()
        
        self.metrics = MetricsWidget()
        self.control = ControlWidget()
        
        upper_layout.addWidget(self.metrics, 1)
        upper_layout.addWidget(self.control, 2)
        
        # Lower row: Console
        self.console = ConsoleWidget()
        
        layout.addLayout(upper_layout, 2)
        layout.addWidget(self.console, 1)

    def apply_background(self):
        bg_path = os.path.join("assets", "backgound_space.png").replace("\\", "/")
        hex_path = os.path.join("assets", "hex.png").replace("\\", "/")
        
        # We use a combined background if possible or just the space one
        self.setStyleSheet(f"""
            QWidget {{
                background-image: url({bg_path});
                background-position: center;
                background-repeat: no-repeat;
            }}
        """)
