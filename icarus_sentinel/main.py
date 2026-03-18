import sys
from PySide6.QtWidgets import QApplication
from icarus_sentinel.ui.main_window import MainWindow

def main():
    """Main entry point for Icarus Sentinel (PySide6)."""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
