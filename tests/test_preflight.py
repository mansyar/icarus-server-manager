import pytest
from unittest.mock import patch, MagicMock
from server_manager import ServerProcessManager

@pytest.fixture
def manager(tmp_path):
    state_file = tmp_path / "server_state.json"
    return ServerProcessManager(state_file=str(state_file))

@patch("psutil.virtual_memory")
def test_check_system_ram_returns_available_percent(mock_vm, manager):
    mock_mem = MagicMock()
    mock_mem.percent = 85.0 # 85% used, 15% available
    mock_mem.available = 4 * (1024**3) # 4GB available
    mock_mem.total = 32 * (1024**3) # 32GB total
    mock_vm.return_value = mock_mem
    
    # Let's say we want to return available percentage
    available_pct = manager.get_available_system_ram_pct()
    
    assert available_pct == 12.5 # (4/32) * 100
