import pytest
from PySide6.QtWidgets import QMainWindow
from icarus_sentinel.ui.main_window import MainWindow

def test_main_window_initialization(qtbot):
    """Test that MainWindow initializes correctly."""
    window = MainWindow()
    qtbot.addWidget(window)
    
    assert isinstance(window, QMainWindow)
    assert window.windowTitle() == "Icarus Sentinel"
