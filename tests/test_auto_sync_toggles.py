import pytest
import os
import json
from icarus_sentinel.server_manager import ServerProcessManager

@pytest.fixture
def state_file(tmp_path):
    return tmp_path / "server_state.json"

@pytest.fixture
def manager(state_file):
    return ServerProcessManager(state_file=str(state_file))

def test_server_manager_auto_sync_state_defaults(manager):
    assert hasattr(manager, "auto_sync_on_start")
    assert hasattr(manager, "auto_sync_on_stop")
    assert hasattr(manager, "selected_steam_id")
    assert manager.auto_sync_on_start is True
    assert manager.auto_sync_on_stop is True
    assert manager.selected_steam_id is None

def test_server_manager_save_load_auto_sync_state(state_file):
    manager = ServerProcessManager(state_file=str(state_file))
    manager.auto_sync_on_start = True
    manager.auto_sync_on_stop = True
    manager.selected_steam_id = "123456789"
    manager.save_state()
    
    # Reload
    new_manager = ServerProcessManager(state_file=str(state_file))
    assert new_manager.auto_sync_on_start is True
    assert new_manager.auto_sync_on_stop is True
    assert new_manager.selected_steam_id == "123456789"

def test_controller_save_sentinel_settings_auto_sync(manager):
    from icarus_sentinel.controller import Controller
    from unittest.mock import MagicMock
    
    mock_ui = MagicMock()
    mock_ui.server_manager = manager
    mock_ui.backup_manager = MagicMock()
    mock_ui.backup_manager.interval_minutes = 30.0
    
    controller = Controller(mock_ui)
    
    settings_data = {
        "auto_sync_on_start": True,
        "auto_sync_on_stop": True,
        "selected_steam_id": "987654321",
        "ram_threshold": "14.0",
        "smart_restart": True,
        "restart_time": "05:00",
        "backup_interval": "60.0",
        "retention_limit": "100",
        "notify_server_started": False,
        "notify_player_activity": False,
        "notify_server_error": False
    }
    
    controller.save_sentinel_settings(settings_data)
    
    assert manager.auto_sync_on_start is True
    assert manager.auto_sync_on_stop is True
    assert manager.selected_steam_id == "987654321"
    assert manager.ram_threshold_gb == 14.0
    assert manager.smart_restart_enabled is True
    assert manager.smart_restart_time == "05:00"
    assert manager.notify_server_started is False
