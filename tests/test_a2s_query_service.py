import pytest
from unittest.mock import patch, MagicMock
from icarus_sentinel.a2s_client import A2SQueryService

@pytest.fixture
def service():
    return A2SQueryService()

@patch("a2s.info")
@patch("a2s.players")
def test_fetch_server_data_success(mock_players, mock_info, service):
    # Mock Server Info
    mock_info_obj = MagicMock()
    mock_info_obj.server_name = "Icarus Server"
    mock_info_obj.player_count = 2
    mock_info_obj.ping = 0.05 # Note: a2s.info doesn't return ping directly, it's usually measured by the client or part of the query
    mock_info.return_value = mock_info_obj

    # Mock Players
    mock_player1 = MagicMock()
    mock_player1.name = "Player1"
    mock_player1.duration = 3600 # 1 hour
    mock_player1.score = 10
    
    mock_player2 = MagicMock()
    mock_player2.name = "Player2"
    mock_player2.duration = 1800 # 30 mins
    mock_player2.score = 5
    
    mock_players.return_value = [mock_player1, mock_player2]

    data = service.fetch_server_data("127.0.0.1", 27015)

    assert data["status"] == "Online"
    assert data["player_count"] == 2
    assert len(data["players"]) == 2
    assert data["players"][0]["name"] == "Player1"
    assert data["players"][0]["playtime"] == "01:00:00"
    assert data["players"][0]["score"] == 10

@patch("a2s.info")
def test_fetch_server_data_offline(mock_info, service):
    mock_info.side_effect = Exception("Connection refused")

    data = service.fetch_server_data("127.0.0.1", 27015)

    assert data["status"] == "Offline"
    assert data["player_count"] == 0
    assert data["players"] == []
