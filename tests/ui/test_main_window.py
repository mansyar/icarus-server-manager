import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QMainWindow

@patch("icarus_sentinel.ui.main_window.SteamManager")
@patch("icarus_sentinel.ui.main_window.BackupManager")
@patch("icarus_sentinel.ui.main_window.ServerProcessManager")
@patch("icarus_sentinel.ui.main_window.INIManager")
@patch("icarus_sentinel.ui.main_window.SaveSyncManager")
@patch("icarus_sentinel.ui.main_window.ModManager")
def test_main_window_initialization(mock_mod, mock_sync, mock_ini, mock_server, mock_backup, mock_steam, qtbot):
    """Test that MainWindow initializes correctly with mocked managers."""
    from icarus_sentinel.ui.main_window import MainWindow
    
    window = MainWindow()
    qtbot.addWidget(window)
    
    assert isinstance(window, QMainWindow)
    assert window.windowTitle() == "Icarus Sentinel"
    assert window.controller is not None
    assert window.width() == 1200
    assert window.height() == 800
