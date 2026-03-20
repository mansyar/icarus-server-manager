import pytest
from unittest.mock import MagicMock
from icarus_sentinel.controller import Controller

@pytest.fixture
def mock_ui():
    ui = MagicMock()
    ui.server_manager = MagicMock()
    ui.backup_manager = MagicMock()
    return ui

def test_save_sentinel_settings_persists_notifications(mock_ui):
    controller = Controller(mock_ui)
    
    data = {
        "ram_threshold": "12.0",
        "smart_restart": True,
        "restart_time": "04:00",
        "backup_interval": "30.0",
        "retention_limit": "50",
        "notify_server_started": False,
        "notify_player_activity": True,
        "notify_server_error": False
    }
    
    controller.save_sentinel_settings(data)
    
    assert mock_ui.server_manager.notify_server_started is False
    assert mock_ui.server_manager.notify_player_activity is True
    assert mock_ui.server_manager.notify_server_error is False
    mock_ui.server_manager.save_state.assert_called_once()

def test_stop_all_threads_cleans_up(mock_ui):
    controller = Controller(mock_ui)
    
    mock_thread = MagicMock()
    mock_thread.isRunning.return_value = True
    controller.threads.append(mock_thread)
    
    mock_worker = MagicMock()
    controller.workers.append(mock_worker)
    
    controller.stop_all_threads()
    
    mock_thread.quit.assert_called_once()
    mock_thread.wait.assert_called_once()
    assert len(controller.threads) == 0
    assert len(controller.workers) == 0
