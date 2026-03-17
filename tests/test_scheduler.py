import pytest
from unittest.mock import patch, MagicMock
from icarus_sentinel.server_manager import ServerProcessManager
from datetime import datetime

@pytest.fixture
def manager(tmp_path):
    state_file = tmp_path / "server_state.json"
    return ServerProcessManager(state_file=str(state_file))

def test_smart_restart_logic_returns_true_if_empty(manager):
    manager.smart_restart_enabled = True
    manager.smart_restart_time = "04:00"
    manager.state["status"] = "running"
    manager.state["pid"] = 1234
    
    # Mock A2SClient to return 0 players
    mock_a2s = MagicMock()
    mock_a2s.get_player_count.return_value = 0
    manager.a2s_client = mock_a2s
    
    # Simulate it's 04:00
    with patch("icarus_sentinel.server_manager.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 0)
        mock_datetime.strptime = datetime.strptime
        
        should_restart = manager.should_smart_restart()
        
        assert should_restart is True
        assert manager.last_smart_restart_date == "2026-03-17"

def test_smart_restart_logic_returns_false_if_players_present(manager):
    manager.smart_restart_enabled = True
    manager.smart_restart_time = "04:00"
    manager.state["status"] = "running"
    manager.state["pid"] = 1234
    
    mock_a2s = MagicMock()
    mock_a2s.get_player_count.return_value = 3
    manager.a2s_client = mock_a2s
    
    with patch("icarus_sentinel.server_manager.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 0)
        
        should_restart = manager.should_smart_restart()
        
        assert should_restart is False

def test_smart_restart_logic_returns_false_if_not_enabled(manager):
    manager.smart_restart_enabled = False
    manager.smart_restart_time = "04:00"
    
    with patch("icarus_sentinel.server_manager.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 0)
        
        assert manager.should_smart_restart() is False

def test_smart_restart_logic_cooldown_same_day(manager):
    manager.smart_restart_enabled = True
    manager.smart_restart_time = "04:00"
    manager.state["status"] = "running"
    manager.state["pid"] = 1234
    manager.last_smart_restart_date = "2026-03-17"
    
    mock_a2s = MagicMock()
    mock_a2s.get_player_count.return_value = 0
    manager.a2s_client = mock_a2s
    
    with patch("icarus_sentinel.server_manager.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 3, 17, 4, 0)
        
        # Should be False because it already triggered today
        assert manager.should_smart_restart() is False
