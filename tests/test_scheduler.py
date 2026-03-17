import pytest
from unittest.mock import patch, MagicMock
from server_manager import ServerProcessManager
from datetime import datetime

@pytest.fixture
def manager(tmp_path):
    state_file = tmp_path / "server_state.json"
    return ServerProcessManager(state_file=str(state_file))

def test_smart_restart_logic_restarts_if_empty(manager):
    manager.smart_restart_enabled = True
    manager.smart_restart_time = "04:00"
    manager.state["status"] = "running"
    manager.state["pid"] = 1234
    
    # Mock A2SClient to return 0 players
    mock_a2s = MagicMock()
    mock_a2s.get_player_count.return_value = 0
    manager.a2s_client = mock_a2s
    
    with patch.object(manager, "restart_server") as mock_restart:
        # Simulate it's 04:00
        with patch("server_manager.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 0)
            mock_datetime.strptime = datetime.strptime
            
            manager.check_smart_restart("C:/path/to/exe")
            
            mock_restart.assert_called_once()

def test_smart_restart_logic_skips_if_players_present(manager):
    manager.smart_restart_enabled = True
    manager.smart_restart_time = "04:00"
    manager.state["status"] = "running"
    
    mock_a2s = MagicMock()
    mock_a2s.get_player_count.return_value = 3
    manager.a2s_client = mock_a2s
    
    with patch.object(manager, "restart_server") as mock_restart:
        with patch("server_manager.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 0)
            mock_datetime.strptime = datetime.strptime
            
            manager.check_smart_restart("C:/path/to/exe")
            
            mock_restart.assert_not_called()

def test_smart_restart_logic_skips_if_not_enabled(manager):
    manager.smart_restart_enabled = False
    manager.smart_restart_time = "04:00"
    
    with patch.object(manager, "restart_server") as mock_restart:
        with patch("server_manager.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 0)
            manager.check_smart_restart("C:/path/to/exe")
            mock_restart.assert_not_called()

def test_smart_restart_logic_skips_if_wrong_time(manager):
    manager.smart_restart_enabled = True
    manager.smart_restart_time = "04:00"
    
    with patch.object(manager, "restart_server") as mock_restart:
        with patch("server_manager.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 1) # One minute late
            manager.check_smart_restart("C:/path/to/exe")
            mock_restart.assert_not_called()
