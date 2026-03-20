import pytest
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel
from icarus_sentinel.ui.main_window import MainWindow
from unittest.mock import MagicMock, patch

@patch("icarus_sentinel.ui.main_window.SteamManager")
@patch("icarus_sentinel.ui.main_window.BackupManager")
@patch("icarus_sentinel.ui.main_window.ServerProcessManager")
@patch("icarus_sentinel.ui.main_window.INIManager")
@patch("icarus_sentinel.ui.main_window.SaveSyncManager")
@patch("icarus_sentinel.ui.main_window.ModManager")
@patch("os.makedirs")
@patch("os.path.exists")
@patch("os.listdir")
def test_main_window_has_correct_icon(mock_listdir, mock_exists, mock_makedirs, mock_mod, mock_sync, mock_ini, mock_server, mock_backup, mock_steam, qtbot):
    """Verifies that the MainWindow has the correct icon set."""
    # Configure mocks
    mock_ini.return_value.get_setting.return_value = ""
    mock_ini.return_value.get_raw_text.return_value = ""
    mock_server.return_value.state = {"pid": None, "status": "stopped"}
    mock_server.return_value.ram_threshold_gb = 16.0
    mock_server.return_value.smart_restart_enabled = False
    mock_server.return_value.smart_restart_time = "04:00"
    mock_backup.return_value.server_path = "/mock/path"
    mock_backup.return_value.backup_path = "/mock/backups"
    mock_exists.return_value = True
    mock_listdir.return_value = []

    window = MainWindow()
    qtbot.addWidget(window)
    
    icon = window.windowIcon()
    assert not icon.isNull(), "Main window icon should not be null."

def test_about_view_has_icon(qtbot):
    """Verifies that the AboutView displays the app icon."""
    from icarus_sentinel.ui.about_view import AboutView
    view = AboutView()
    qtbot.addWidget(view)
    
    # Find the QLabel that should contain the icon
    # We'll need to check the implementation of AboutView to see how to identify it
    icon_label = None
    for child in view.findChildren(QLabel):
        if child.pixmap() and not child.pixmap().isNull():
            icon_label = child
            break
            
    assert icon_label is not None, "AboutView should have a QLabel with a pixmap."
