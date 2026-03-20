from PySide6.QtWidgets import QAbstractButton
from PySide6.QtCore import Qt, QPropertyAnimation, Property, QEasingCurve, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from icarus_sentinel import style_config

class ToggleSwitch(QAbstractButton):
    def __init__(self, parent=None, active_color=style_config.ACCENT_COLOR, bg_color="#333333"):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(60, 28)
        
        self._active_color = QColor(active_color)
        self._bg_color = QColor(bg_color)
        self._circle_color = QColor("#E0E0E0")
        
        # Handle position (0.0 to 1.0)
        self._handle_position = 0.0
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def nextCheckState(self):
        super().nextCheckState()
        self.start_animation()

    def setChecked(self, checked):
        super().setChecked(checked)
        self.animation.stop()
        self._handle_position = 1.0 if checked else 0.0
        self.update()

    def start_animation(self):
        self.animation.stop()
        self.animation.setStartValue(self._handle_position)
        self.animation.setEndValue(1.0 if self.isChecked() else 0.0)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Define toggle background (track)
        rect = QRect(0, 0, self.width(), self.height())
        radius = self.height() / 2
        
        # Interpolate color based on handle position
        bg_color = self._bg_color
        if self._handle_position > 0:
            # Simple color blend (rough approximation)
            r = int(self._bg_color.red() + (self._active_color.red() - self._bg_color.red()) * self._handle_position)
            g = int(self._bg_color.green() + (self._active_color.green() - self._bg_color.green()) * self._handle_position)
            b = int(self._bg_color.blue() + (self._active_color.blue() - self._bg_color.blue()) * self._handle_position)
            bg_color = QColor(r, g, b)

        painter.setPen(Qt.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(rect, radius, radius)
        
        # Draw Handle (Circle)
        handle_radius = radius - 3
        handle_x = 3 + (self.width() - (handle_radius * 2) - 6) * self._handle_position
        handle_y = 3
        
        painter.setBrush(self._circle_color)
        painter.drawEllipse(QRect(handle_x, handle_y, handle_radius * 2, handle_radius * 2))
        
        painter.end()
