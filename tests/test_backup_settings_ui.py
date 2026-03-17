import pytest
from unittest.mock import MagicMock, patch
import json
import os
from app import App
from server_manager import ServerProcessManager
from backup_manager import BackupManager

@pytest.fixture
def app_instance(tmp_path):
    state_file = tmp_path / "server_state.json"
    with patch("app.ctk.CTk.title"), \
         patch("app.ctk.CTk.geometry"), \
         patch("tkinter.Misc.after"), \
         patch("app.App.update_monitoring"):
        
        app = App(state_file=str(state_file))
        app.log = MagicMock()
        yield app
        if hasattr(app, "destroy"):
            app.destroy()

def test_backup_settings_ui_elements_exist(app_instance):
    assert hasattr(app_instance, "backup_interval_entry")
    assert hasattr(app_instance, "backup_retention_entry")

def test_save_settings_updates_backup_config(app_instance):
    # Mock entries
    app_instance.threshold_entry = MagicMock()
    app_instance.threshold_entry.get.return_value = "16.0"
    app_instance.smart_restart_var = MagicMock()
    app_instance.smart_restart_var.get.return_value = False
    app_instance.restart_time_entry = MagicMock()
    app_instance.restart_time_entry.get.return_value = "04:00"
    
    app_instance.backup_interval_entry = MagicMock()
    app_instance.backup_interval_entry.get.return_value = "45"
    app_instance.backup_retention_entry = MagicMock()
    app_instance.backup_retention_entry.get.return_value = "100"
    
    app_instance.save_settings()
    
    assert app_instance.backup_manager.interval_minutes == 45
    assert app_instance.backup_manager.retention_limit == 100
    app_instance.log.assert_called_with("Settings saved.")

def test_server_manager_persists_backup_settings(tmp_path):
    state_file = tmp_path / "server_state.json"
    mock_backup_mgr = MagicMock(spec=BackupManager)
    mock_backup_mgr.interval_minutes = 45
    mock_backup_mgr.retention_limit = 100
    
    manager = ServerProcessManager(state_file=str(state_file), backup_manager=mock_backup_mgr)
    manager.save_state()
    
    with open(str(state_file), "r") as f:
        state = json.load(f)
    
    assert state["backup_interval_minutes"] == 45
    assert state["backup_retention_limit"] == 100

def test_server_manager_loads_backup_settings(tmp_path):
    state_file = tmp_path / "server_state.json"
    initial_state = {
        "pid": None,
        "status": "stopped",
        "backup_interval_minutes": 60,
        "backup_retention_limit": 10
    }
    with open(str(state_file), "w") as f:
        json.dump(initial_state, f)
    
    mock_backup_mgr = MagicMock(spec=BackupManager)
    manager = ServerProcessManager(state_file=str(state_file), backup_manager=mock_backup_mgr)
    
    assert mock_backup_mgr.interval_minutes == 60
    assert mock_backup_mgr.retention_limit == 10
