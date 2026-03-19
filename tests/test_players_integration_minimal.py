import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QStackedWidget, QWidget
from icarus_sentinel.ui.players import PlayersView

def test_players_view_integration_logic(qtbot):
    """Verifies that PlayersView correctly handles data updates in a simulated integration."""
    view = PlayersView()
    qtbot.addWidget(view)
    view.show()
    
    mock_data = {
        "status": "Online",
        "server_name": "Test Server",
        "player_count": 1,
        "players": [{"name": "Crasher", "playtime": "00:01:00", "score": 10}]
    }
    
    # Simulate data received signal from worker
    view.update_data(mock_data)
    
    assert view.table.rowCount() == 1
    assert view.table.item(0, 0).text() == "Crasher"
    assert "Test Server" in view.status_label.text()

def test_players_view_offline_logic(qtbot):
    view = PlayersView()
    qtbot.addWidget(view)
    view.show()
    
    mock_data = {"status": "Offline", "player_count": 0, "players": []}
    view.update_data(mock_data)
    
    assert view.placeholder.isVisible()
    assert not view.table.isVisible()
