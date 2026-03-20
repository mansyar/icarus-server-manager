import sys
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import icarus_sentinel.ui.resources_rc
from icarus_sentinel.ui.main_window import MainWindow

def main():
    """Main entry point for Icarus Sentinel (PySide6)."""
    app = QApplication(sys.argv)
    
    # Create and show splash screen
    pixmap = QPixmap(":/icons/app_icon.png")
    splash = QSplashScreen(pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    splash.show()
    
    # Allow the event loop to process so the splash screen renders
    app.processEvents()
    
    window = MainWindow()
    window.show()
    
    # Close splash screen when main window is ready
    splash.finish(window)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
