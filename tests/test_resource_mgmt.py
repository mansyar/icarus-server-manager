import pytest
from unittest.mock import patch, MagicMock
from icarus_sentinel.server_manager import ServerProcessManager
import psutil

@pytest.fixture
def manager(tmp_path):
    state_file = tmp_path / "server_state.json"
    return ServerProcessManager(state_file=str(state_file))

@patch("psutil.Process")
def test_get_resource_usage_updates_status_to_warning_on_high_ram(mock_psutil_process, manager):
    # Setup mock process with high RAM (17GB)
    mock_proc_instance = mock_psutil_process.return_value
    mock_proc_instance.is_running.return_value = True
    mock_proc_instance.cpu_percent.return_value = 10.0
    mock_memory_info = MagicMock()
    mock_memory_info.rss = 17 * (1024**3) # 17GB
    mock_proc_instance.memory_info.return_value = mock_memory_info
    
    manager.ram_threshold_gb = 16.0
    manager.state["status"] = "running"
    
    usage = manager.get_resource_usage(1234)
    
    assert usage["ram_gb"] == 17.0
    assert manager.state["status"] == "warning"

@patch("psutil.Process")
def test_get_resource_usage_resets_status_from_warning_on_normal_ram(mock_psutil_process, manager):
    # Setup mock process with normal RAM (8GB)
    mock_proc_instance = mock_psutil_process.return_value
    mock_proc_instance.is_running.return_value = True
    mock_proc_instance.cpu_percent.return_value = 10.0
    mock_memory_info = MagicMock()
    mock_memory_info.rss = 8 * (1024**3) # 8GB
    mock_proc_instance.memory_info.return_value = mock_memory_info
    
    manager.ram_threshold_gb = 16.0
    manager.state["status"] = "warning"
    
    usage = manager.get_resource_usage(1234)
    
    assert usage["ram_gb"] == 8.0
    assert manager.state["status"] == "running"

@patch("psutil.Process")
def test_get_resource_usage_triggers_notification_on_high_ram(mock_psutil_process, manager):
    # Setup mock process with high RAM (17GB)
    mock_proc_instance = mock_psutil_process.return_value
    mock_proc_instance.is_running.return_value = True
    mock_proc_instance.cpu_percent.return_value = 10.0
    mock_memory_info = MagicMock()
    mock_memory_info.rss = 17 * (1024**3) # 17GB
    mock_proc_instance.memory_info.return_value = mock_memory_info
    
    # Mock NotificationManager
    mock_notifications = MagicMock()
    manager.notifications = mock_notifications
    manager.ram_threshold_gb = 16.0
    manager.state["status"] = "running"
    
    manager.get_resource_usage(1234)
    
    mock_notifications.notify.assert_called_once_with(
        "High RAM Usage Alert",
        "Icarus Server is using 17.0GB of RAM, exceeding the 16.0GB threshold."
    )

@patch("psutil.Process")
def test_get_resource_usage_does_not_spam_notifications(mock_psutil_process, manager):
    # Setup mock process with high RAM (17GB)
    mock_proc_instance = mock_psutil_process.return_value
    mock_proc_instance.is_running.return_value = True
    mock_proc_instance.cpu_percent.return_value = 10.0
    mock_memory_info = MagicMock()
    mock_memory_info.rss = 17 * (1024**3) # 17GB
    mock_proc_instance.memory_info.return_value = mock_memory_info
    
    # Mock NotificationManager
    mock_notifications = MagicMock()
    manager.notifications = mock_notifications
    manager.ram_threshold_gb = 16.0
    manager.state["status"] = "running"
    
    # First call - should notify
    manager.get_resource_usage(1234)
    assert manager.state["status"] == "warning"
    assert mock_notifications.notify.call_count == 1
    
    # Second call - status already 'warning', should NOT notify again
    manager.get_resource_usage(1234)
    assert mock_notifications.notify.call_count == 1

def test_ram_threshold_is_configurable(manager):
    assert manager.ram_threshold_gb == 16.0 # Default
    manager.ram_threshold_gb = 20.0
    assert manager.ram_threshold_gb == 20.0

def test_save_state_includes_ram_threshold(manager):
    manager.ram_threshold_gb = 18.5
    manager.save_state()
    
    import json
    with open(manager.state_file, "r") as f:
        saved_state = json.load(f)
    assert saved_state["ram_threshold_gb"] == 18.5

def test_load_state_restores_ram_threshold(tmp_path):
    state_file = tmp_path / "server_state.json"
    initial_state = {"pid": None, "status": "stopped", "ram_threshold_gb": 22.0}
    import json
    with open(str(state_file), "w") as f:
        json.dump(initial_state, f)
    
    manager = ServerProcessManager(state_file=str(state_file))
    assert manager.ram_threshold_gb == 22.0
