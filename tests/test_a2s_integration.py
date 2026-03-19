import pytest
from PySide6.QtCore import QObject, Signal, QThread
from icarus_sentinel.ui.players import PlayersView
from icarus_sentinel.ui.workers import A2SQueryWorker
from unittest.mock import MagicMock

def test_integration_worker_to_view(qtbot):
    """Test that data emitted by the worker reaches the view."""
    view = PlayersView()
    qtbot.addWidget(view)
    
    # Mock data
    mock_data = {
        "status": "Online", 
        "server_name": "Integration Test", 
        "player_count": 1, 
        "players": [{"name": "Tester", "playtime": "00:05:00", "score": 50}]
    }
    
    # We don't need a real thread for this signal test
    mock_service = MagicMock()
    worker = A2SQueryWorker(mock_service)
    
    # Connect signal
    worker.data_received.connect(view.update_data)
    
    # Trigger signal manually
    with qtbot.waitSignal(worker.data_received, timeout=1000):
        worker.data_received.emit(mock_data)
        
    # Verify view updated
    assert view.table.rowCount() == 1
    assert view.table.item(0, 0).text() == "Tester"
    assert "Integration Test" in view.status_label.text()
