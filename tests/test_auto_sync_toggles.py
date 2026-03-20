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
    assert manager.auto_sync_on_start is False
    assert manager.auto_sync_on_stop is False
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
