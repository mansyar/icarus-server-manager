import os
import json
import pytest
from icarus_sentinel.server_manager import ServerProcessManager

@pytest.fixture
def temp_state_file(tmp_path):
    return str(tmp_path / "test_server_state.json")

def test_default_notification_settings(temp_state_file):
    """Verify that notification settings default to True."""
    manager = ServerProcessManager(state_file=temp_state_file)
    assert manager.notify_server_started is True
    assert manager.notify_player_activity is True
    assert manager.notify_server_error is True

def test_save_load_notification_settings(temp_state_file):
    """Verify that notification settings are correctly persisted and loaded."""
    manager = ServerProcessManager(state_file=temp_state_file)
    
    # Change settings
    manager.notify_server_started = False
    manager.notify_player_activity = False
    manager.notify_server_error = False
    manager.save_state()
    
    # Reload and check
    new_manager = ServerProcessManager(state_file=temp_state_file)
    assert new_manager.notify_server_started is False
    assert new_manager.notify_player_activity is False
    assert new_manager.notify_server_error is False

def test_load_partial_notification_settings(temp_state_file):
    """Verify that partial settings in the state file are handled correctly."""
    # Pre-create state file with some settings missing
    with open(temp_state_file, "w") as f:
        json.dump({"notify_server_started": False}, f)
    
    manager = ServerProcessManager(state_file=temp_state_file)
    assert manager.notify_server_started is False
    # Should default to True if missing in file
    assert manager.notify_player_activity is True
    assert manager.notify_server_error is True
