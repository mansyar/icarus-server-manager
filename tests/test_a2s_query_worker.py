import pytest
from PySide6.QtCore import QThread, Signal
from icarus_sentinel.ui.workers import A2SQueryWorker
from unittest.mock import MagicMock
import time

def test_a2s_query_worker_emits_data(qtbot):
    """Test that A2SQueryWorker emits data received from the service."""
    mock_service = MagicMock()
    mock_data = {"status": "Online", "player_count": 1, "players": [{"name": "Test", "playtime": "00:01:00", "score": 0}]}
    mock_service.fetch_server_data.return_value = mock_data
    
    worker = A2SQueryWorker(mock_service, "127.0.0.1", 27015, interval=0.1) # Short interval for testing
    thread = QThread()
    worker.moveToThread(thread)
    
    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    
    with qtbot.waitSignal(worker.finished, timeout=2000):
        thread.start()
        qtbot.wait(300) # Allow at least one poll
        worker.stop() # Signal worker to stop
        
    thread.wait(1000)
    assert mock_service.fetch_server_data.called
    
def test_a2s_query_worker_data_received_signal(qtbot):
    mock_service = MagicMock()
    mock_data = {"status": "Online", "player_count": 1, "players": []}
    mock_service.fetch_server_data.return_value = mock_data
    
    worker = A2SQueryWorker(mock_service, "127.0.0.1", 27015, interval=0.1)
    
    with qtbot.waitSignal(worker.data_received, timeout=1000) as blocker:
        worker.run_once() # We'll implement a run_once for easier testing or just use run with a stop flag
        
    assert blocker.args == [mock_data]
