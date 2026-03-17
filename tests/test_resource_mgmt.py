import pytest
from unittest.mock import patch, MagicMock
from server_manager import ServerProcessManager
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

def test_ram_threshold_is_configurable(manager):
    assert manager.ram_threshold_gb == 16.0 # Default
    manager.ram_threshold_gb = 20.0
    assert manager.ram_threshold_gb == 20.0
