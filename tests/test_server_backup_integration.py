import pytest
from unittest.mock import MagicMock, patch
from icarus_sentinel.server_manager import ServerProcessManager
from icarus_sentinel.backup_manager import BackupManager

def test_server_stop_triggers_backup(tmp_path):
    state_file = tmp_path / "server_state.json"
    mock_backup_mgr = MagicMock(spec=BackupManager)
    mock_backup_mgr.interval_minutes = 30.0
    mock_backup_mgr.retention_limit = 50
    
    # Initialize manager with mock backup manager
    manager = ServerProcessManager(state_file=str(state_file), backup_manager=mock_backup_mgr)
    
    mock_process = MagicMock()
    manager.stop_server(mock_process)
    
    # Verify backup was triggered
    mock_backup_mgr.on_server_stop.assert_called_once()

def test_server_stop_works_without_backup_mgr(tmp_path):
    state_file = tmp_path / "server_state.json"
    # Initialize manager without backup manager (backwards compatibility)
    manager = ServerProcessManager(state_file=str(state_file))
    
    mock_process = MagicMock()
    manager.stop_server(mock_process)
    
    # Should not raise exception
    assert manager.state["status"] == "stopped"
