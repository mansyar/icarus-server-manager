import pytest
from icarus_sentinel.ui.players import PlayersView

def test_players_view_shows_offline_placeholder(qtbot):
    view = PlayersView()
    qtbot.addWidget(view)
    view.show()
    
    # Mock data for offline server
    data = {"status": "Offline", "player_count": 0, "players": []}
    view.update_data(data)
    
    assert view.placeholder.isVisible()
    assert "unreachable" in view.placeholder.text().lower()
    assert not view.table.isVisible()

def test_players_view_shows_empty_placeholder(qtbot):
    view = PlayersView()
    qtbot.addWidget(view)
    view.show()
    
    # Mock data for online server with no players
    data = {"status": "Online", "server_name": "Test", "player_count": 0, "players": []}
    view.update_data(data)
    
    assert view.placeholder.isVisible()
    assert "no players" in view.placeholder.text().lower()
    assert not view.table.isVisible()

def test_players_view_updates_table(qtbot):
    view = PlayersView()
    qtbot.addWidget(view)
    view.show()
    
    # Mock data for online server with players
    data = {
        "status": "Online", 
        "server_name": "Test", 
        "player_count": 1, 
        "players": [{"name": "Player1", "playtime": "00:10:00", "score": 100}]
    }
    view.update_data(data)
    
    assert not view.placeholder.isVisible()
    assert view.table.isVisible()
    assert view.table.rowCount() == 1
    assert view.table.item(0, 0).text() == "Player1"
    assert view.table.item(0, 1).text() == "00:10:00"
    assert view.table.item(0, 2).text() == "100"
