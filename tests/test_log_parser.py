import pytest
from icarus_sentinel.server_manager import ServerProcessManager

@pytest.fixture
def manager():
    return ServerProcessManager(state_file="test_state.json")

def test_parse_server_started(manager):
    """Verify detection of 'Server started' message."""
    line = "[12:41:02] LogIcarusGameStateRecording: Display: ReadFromProspectSaveState complete"
    event = manager.parse_log_line(line)
    assert event["type"] == "server_started"

def test_parse_player_join(manager):
    """Verify detection of player join message."""
    line = "[2026.03.20-10.05.00:000][123]LogNet: Join succeeded: PlayerOne"
    event = manager.parse_log_line(line)
    assert event["type"] == "player_join"
    assert event["player"] == "PlayerOne"

def test_parse_player_leave(manager):
    """Verify detection of player leave message."""
    line = "[2026.03.20-10.10.00:000][456]LogNet: Client (PlayerOne) closed connection"
    event = manager.parse_log_line(line)
    assert event["type"] == "player_leave"
    assert event["player"] == "PlayerOne"

def test_parse_unrelated_line(manager):
    """Verify that unrelated lines return None."""
    line = "[2026.03.20-10.00.00:000][  0]LogIcarus: Some other log message"
    event = manager.parse_log_line(line)
    assert event is None
