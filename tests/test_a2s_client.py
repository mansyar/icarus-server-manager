import pytest
from unittest.mock import patch, MagicMock

from a2s_client import A2SClient

@patch("a2s.info")
def test_get_player_count_success(mock_a2s_info):
    mock_info = MagicMock()
    mock_info.player_count = 5
    mock_a2s_info.return_value = mock_info
    
    client = A2SClient()
    count = client.get_player_count("127.0.0.1", 27015)
    
    assert count == 5
    mock_a2s_info.assert_called_once_with(("127.0.0.1", 27015), timeout=3.0)

@patch("a2s.info")
def test_get_player_count_timeout(mock_a2s_info):
    mock_a2s_info.side_effect = Exception("Timeout")
    
    client = A2SClient()
    count = client.get_player_count("127.0.0.1", 27015)
    
    assert count == 0 # Should handle timeout gracefully and return 0
