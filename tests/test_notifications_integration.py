import pytest
from unittest.mock import MagicMock, patch
import io
from icarus_sentinel.server_manager import ServerProcessManager

@pytest.fixture
def mock_notifications():
    return MagicMock()

@pytest.fixture
def manager(mock_notifications, tmp_path):
    state_file = tmp_path / "test_state.json"
    return ServerProcessManager(state_file=str(state_file), notification_manager=mock_notifications)

def test_stream_logs_triggers_notifications(manager, mock_notifications):
    """Verify that streaming logs triggers correct notifications."""
    mock_process = MagicMock()
    # Simulate log lines
    logs = [
        "LogIcarus: Display: Server started",
        "LogNet: Join succeeded: PlayerOne",
        "LogNet: Client (PlayerOne) closed connection"
    ]
    mock_process.stdout = io.StringIO("\n".join(logs) + "\n")
    
    callback = MagicMock()
    manager.stream_logs(mock_process, callback)
    
    # Check notifications
    assert mock_notifications.notify.call_count == 3
    mock_notifications.notify.assert_any_call("Icarus Server", "Server has started and is ready for players.")
    mock_notifications.notify.assert_any_call("Player Joined", "PlayerOne has joined the server.")
    mock_notifications.notify.assert_any_call("Player Left", "PlayerOne has left the server.")

def test_notifications_respect_preferences(manager, mock_notifications):
    """Verify that notifications are not sent if disabled in settings."""
    manager.notify_server_started = False
    manager.notify_player_activity = False
    
    mock_process = MagicMock()
    logs = [
        "LogIcarus: Display: Server started",
        "LogNet: Join succeeded: PlayerOne"
    ]
    mock_process.stdout = io.StringIO("\n".join(logs) + "\n")
    
    manager.stream_logs(mock_process, MagicMock())
    
    # Should NOT have called notify
    mock_notifications.notify.assert_not_called()

def test_crash_notification(manager, mock_notifications):
    """Verify notification on server crash."""
    mock_process = MagicMock()
    mock_process.pid = 1234
    
    import threading
    event_finished = threading.Event()
    
    def mock_wait():
        event_finished.set()
        return 1 # Exit code 1 (error)
    
    mock_process.wait.side_effect = mock_wait
    
    with patch("subprocess.Popen", return_value=mock_process):
        with patch("psutil.Process"):
            manager.start_server("mock_exe")
            
            # Wait for the monitor thread to finish
            assert event_finished.wait(timeout=2)
            
            # Give a tiny bit of time for state to update after wait() returns
            import time
            time.sleep(0.1)
            
            assert manager.state["status"] == "error"
            mock_notifications.notify.assert_called_with("Server Crash", "Icarus Server has crashed with code 1.")
