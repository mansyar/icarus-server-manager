import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QMainWindow

@patch("icarus_sentinel.ui.main_window.SteamManager")
@patch("icarus_sentinel.ui.main_window.BackupManager")
@patch("icarus_sentinel.ui.main_window.ServerProcessManager")
@patch("icarus_sentinel.ui.main_window.INIManager")
@patch("icarus_sentinel.ui.main_window.SaveSyncManager")
@patch("icarus_sentinel.ui.main_window.ModManager")
@patch("os.makedirs")
@patch("os.path.exists")
@patch("os.listdir")
def test_main_window_initialization(mock_listdir, mock_exists, mock_makedirs, mock_mod, mock_sync, mock_ini, mock_server, mock_backup, mock_steam, qtbot):
    """Test that MainWindow initializes correctly with mocked managers."""
    # Configure mocks to return strings where needed
    mock_ini.return_value.get_setting.return_value = ""
    mock_ini.return_value.get_raw_text.return_value = ""
    mock_server.return_value.state = {"pid": None, "status": "stopped"}
    mock_server.return_value.ram_threshold_gb = 16.0
    mock_server.return_value.smart_restart_enabled = False
    mock_server.return_value.smart_restart_time = "04:00"
    mock_backup.return_value.server_path = "/mock/path"
    mock_backup.return_value.backup_path = "/mock/backups"
    mock_backup.return_value.interval_minutes = 30.0
    mock_backup.return_value.retention_limit = 50
    mock_sync.return_value.list_local_steam_ids.return_value = []
    mock_exists.return_value = True
    mock_listdir.return_value = []

    from icarus_sentinel.ui.main_window import MainWindow
    
    window = MainWindow()
    qtbot.addWidget(window)
    
    assert isinstance(window, QMainWindow)
    assert window.windowTitle() == "Icarus Sentinel"
    assert window.controller is not None
    assert window.width() == 1250
    assert window.height() == 800
    
    # Check if AboutView is in the stack
    assert "about" in window.views
    from icarus_sentinel.ui.about_view import AboutView
    assert isinstance(window.views["about"], AboutView)
