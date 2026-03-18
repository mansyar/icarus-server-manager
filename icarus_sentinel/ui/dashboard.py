from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QProgressBar, QFrame,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QPalette, QBrush, QColor, QFont
import os
import datetime
from icarus_sentinel import style_config

# Pure QSS Industrial Style Helper
PANEL_STYLE = f"""
    background-color: rgba(30, 30, 30, 240);
    border: 1px solid #555;
    border-top: 1px solid #777;
    border-left: 1px solid #666;
    border-radius: 12px;
"""

class StatusBanner(QFrame):
    """Top status banner from the mockup."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("StatusBanner")
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 15)
        
        self.icon_label = QLabel()
        icon_path = os.path.join("assets", "rocket.PNG")
        if os.path.exists(icon_path):
            self.icon_label.setPixmap(QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        text_layout = QVBoxLayout()
        self.status_title = QLabel("SYSTEM STATUS: OFFLINE")
        self.status_title.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 16px; border: none; background: transparent;")
        
        # Increased brightness from 0.8 opacity to 1.0/White for better contrast
        self.status_desc = QLabel("PRE-FLIGHT CHECKS OPTIMAL - SYSTEMS READY FOR INITIATION")
        self.status_desc.setStyleSheet(f"color: #EEE; font-family: 'Segoe UI'; font-size: 11px; font-weight: bold; border: none; background: transparent;")
        
        text_layout.addWidget(self.status_title)
        text_layout.addWidget(self.status_desc)
        
        layout.addWidget(self.icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        self.setStyleSheet(f"QFrame#StatusBanner {{ {PANEL_STYLE} }}")

class MetricsWidget(QFrame):
    """Displays CPU and RAM metrics with an industrial look."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("MetricsPanel")
        self.title_text = title
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.header = QLabel(self.title_text)
        self.header.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 12px; letter-spacing: 1px; border: none; background: transparent;")
        
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(12)

        # Increased brightness from #888 to #DDD
        self.status_label = QLabel("0% LOAD / 100% AVAILABLE")
        self.status_label.setStyleSheet("color: #DDD; font-family: 'Segoe UI'; font-size: 11px; font-weight: bold; border: none; background: transparent;")

        layout.addWidget(self.header)
        layout.addWidget(self.bar)
        layout.addWidget(self.status_label)

        self.setStyleSheet(f"""
            QFrame#MetricsPanel {{
                {PANEL_STYLE}
            }}
            QProgressBar {{
                background-color: #000;
                border: 1px solid #444;
                border-radius: 6px;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #E65100, stop:1 {style_config.ACCENT_COLOR});
                border-radius: 5px;
            }}
        """)

    def update_value(self, value: float, text: str):
        self.bar.setValue(int(value))
        self.status_label.setText(text)

class ControlWidget(QFrame):
    """The main orbital launch control panel with caution stripes."""
    action_triggered = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ControlPanel")
        self.is_running = False
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setFixedSize(360, 90)

        caution_path = os.path.join("assets", "caution_stripe.png").replace("\\", "/")
        
        self.left_stripe = QFrame()
        self.left_stripe.setFixedWidth(40)
        self.left_stripe.setStyleSheet(f"background-image: url({caution_path}); border-top-left-radius: 12px; border-bottom-left-radius: 12px; border: 1px solid #555;")
        
        self.right_stripe = QFrame()
        self.right_stripe.setFixedWidth(40)
        self.right_stripe.setStyleSheet(f"background-image: url({caution_path}); border-top-right-radius: 12px; border-bottom-right-radius: 12px; border: 1px solid #555;")

        self.launch_btn = QPushButton("INITIATE ORBITAL LAUNCH")
        self.launch_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.launch_btn.setCursor(Qt.PointingHandCursor)
        self.launch_btn.clicked.connect(self._on_click)
        
        self.launch_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #222;
                color: {style_config.ACCENT_COLOR};
                border-top: 1px solid #555;
                border-bottom: 1px solid #000;
                font-family: 'Segoe UI Black';
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #333;
                color: white;
            }}
        """)

        layout.addWidget(self.left_stripe)
        layout.addWidget(self.launch_btn)
        layout.addWidget(self.right_stripe)
        
        self.setStyleSheet("QFrame#ControlPanel { border-radius: 12px; }")

    def _on_click(self):
        self.is_running = not self.is_running
        self.action_triggered.emit(self.is_running)
        if self.is_running:
            self.launch_btn.setText("ABORT MISSION")
            self.launch_btn.setStyleSheet(self.launch_btn.styleSheet().replace(style_config.ACCENT_COLOR, "#FF5252"))
        else:
            self.launch_btn.setText("INITIATE ORBITAL LAUNCH")
            self.launch_btn.setStyleSheet(self.launch_btn.styleSheet().replace("#FF5252", style_config.ACCENT_COLOR))

class ConsoleWidget(QFrame):
    """The persistent log terminal with metallic look."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ConsolePanel")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 35, 15, 15)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFontFamily(style_config.FONT_MONO[0])
        self.text_area.setFontPointSize(10)
        # Using a solid but dark background for logs to ensure text pop
        self.text_area.setStyleSheet("background-color: #050505; border: 1px solid #222; color: #FFA726; border-radius: 5px; padding: 10px;")
        
        layout.addWidget(self.text_area)

        self.setStyleSheet(f"QFrame#ConsolePanel {{ {PANEL_STYLE} }}")
        
        # Title contrast and size increased to match user request
        self.title_label = QLabel("CONSOLE LOGS", self)
        self.title_label.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 14px; background: transparent; letter-spacing: 1px;")
        self.title_label.move(25, 10)

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.text_area.append(f"{timestamp} {message}")
        self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())

class DashboardView(QWidget):
    """The main high-fidelity dashboard view."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(30, 30, 30, 30)
        
        self.main_container = QFrame()
        self.main_container.setObjectName("DashboardContainer")
        
        self.main_container.setStyleSheet(f"""
            QFrame#DashboardContainer {{
                background-color: rgba(15, 15, 15, 230);
                border: 1px solid #444;
                border-radius: 25px;
            }}
        """)
        
        layout = QVBoxLayout(self.main_container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header contrast: Sub-label increased from #555 to #999
        header_layout = QVBoxLayout()
        header_label = QLabel("SERVER DASHBOARD")
        header_label.setStyleSheet(f"color: {style_config.ACCENT_COLOR}; font-family: 'Segoe UI Black'; font-size: 28px; background: transparent; letter-spacing: 1px;")
        sub_label = QLabel("GAME: ICARUS")
        sub_label.setStyleSheet("color: #999; font-family: 'Segoe UI'; font-size: 12px; font-weight: bold; background: transparent; margin-bottom: 5px;")
        header_layout.addWidget(header_label)
        header_layout.addWidget(sub_label)
        layout.addLayout(header_layout)

        # 1. Status Banner
        self.status_banner = StatusBanner()
        layout.addWidget(self.status_banner)

        # 2. Metrics Row
        metrics_layout = QHBoxLayout()
        self.cpu_metrics = MetricsWidget("CPU CORE LOAD")
        self.ram_metrics = MetricsWidget("MEMORY BANK ALLOCATION")
        metrics_layout.addWidget(self.cpu_metrics)
        metrics_layout.addWidget(self.ram_metrics)
        layout.addLayout(metrics_layout)

        # 3. Control Panel
        self.control = ControlWidget()
        layout.addWidget(self.control, 0, Qt.AlignCenter)

        # 4. Console
        self.console = ConsoleWidget()
        layout.addWidget(self.console, 1)

        self.outer_layout.addWidget(self.main_container)

        self.metrics = self 
        
    def update_metrics(self, cpu: float, ram: float, total_ram: float = 16.0):
        self.cpu_metrics.update_value(cpu, f"{cpu:.1f}% LOAD / {100-cpu:.1f}% AVAILABLE")
        self.ram_metrics.update_value((ram / total_ram) * 100 if total_ram > 0 else 0, 
                                     f"{ram:.1f}GB ALLOCATED / {total_ram:.1f}GB TOTAL")
