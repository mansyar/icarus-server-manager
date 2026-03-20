import pytest
from unittest.mock import MagicMock, patch, call, ANY
import os
from icarus_sentinel.ui.main_window import MainWindow

@pytest.fixture
def mock_managers():
    with patch("icarus_sentinel.ui.main_window.SteamManager"), \
         patch("icarus_sentinel.ui.main_window.BackupManager") as mock_backup, \
         patch("icarus_sentinel.ui.main_window.ServerProcessManager") as mock_server, \
         patch("icarus_sentinel.ui.main_window.INIManager") as mock_ini, \
         patch("icarus_sentinel.ui.main_window.SaveSyncManager"), \
         patch("icarus_sentinel.ui.main_window.ModManager"), \
         patch("os.makedirs"), \
         patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=[]), \
         patch("icarus_sentinel.ui.main_window.Controller") as mock_controller:
        
        mock_server_inst = mock_server.return_value
        mock_server_inst.state = {"pid": None, "status": "stopped"}
        mock_server_inst.auto_sync_on_start = False
        mock_server_inst.auto_sync_on_stop = False
        mock_server_inst.selected_steam_id = None
        mock_server_inst.ram_threshold_gb = 16.0
        mock_server_inst.smart_restart_enabled = False
        mock_server_inst.smart_restart_time = "04:00"
        
        mock_ini_inst = mock_ini.return_value
        mock_ini_inst.get_setting.return_value = ""
        mock_ini_inst.get_raw_text.return_value = ""
        
        mock_backup_inst = mock_backup.return_value
        mock_backup_inst.server_path = "/mock/path"
        mock_backup_inst.backup_path = "/mock/backups"
        
        yield mock_server_inst, mock_controller.return_value

def test_on_launch_clicked_sync_on_start_enabled(qtbot, mock_managers):
    mock_server, mock_controller = mock_managers
    mock_server.auto_sync_on_start = True
    mock_server.selected_steam_id = "12345"
    
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Trigger start
    window._on_launch_clicked(True)
    
    # Verify sync_saves was called
    mock_controller.sync_saves.assert_called_once_with("12345", callback=ANY)
    # run_server should NOT be called yet (it should be in the callback)
    mock_controller.run_server.assert_not_called()

def test_on_launch_clicked_sync_on_start_disabled(qtbot, mock_managers):
    mock_server, mock_controller = mock_managers
    mock_server.auto_sync_on_start = False
    mock_server.selected_steam_id = "12345"
    
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Trigger start
    window._on_launch_clicked(True)
    
    # Verify sync_saves was NOT called
    mock_controller.sync_saves.assert_not_called()
    # run_server SHOULD be called
    mock_controller.run_server.assert_called_once()

def test_on_launch_clicked_sync_on_stop_enabled(qtbot, mock_managers):
    mock_server, mock_controller = mock_managers
    mock_server.auto_sync_on_stop = True
    mock_server.selected_steam_id = "12345"
    window = MainWindow()
    qtbot.addWidget(window)
    window.server_process = 999
    
    # Trigger stop
    window._on_launch_clicked(False)
    
    # Verify stop_server was called
    mock_server.stop_server.assert_called_once_with(999)
    # Verify sync_saves was called AFTER stop
    mock_controller.sync_saves.assert_called_once_with("12345")

def test_on_launch_clicked_sync_on_stop_disabled(qtbot, mock_managers):
    mock_server, mock_controller = mock_managers
    mock_server.auto_sync_on_stop = False
    mock_server.selected_steam_id = "12345"
    window = MainWindow()
    qtbot.addWidget(window)
    window.server_process = 999
    
    # Trigger stop
    window._on_launch_clicked(False)
    
    # Verify sync_saves was NOT called
    mock_controller.sync_saves.assert_not_called()
