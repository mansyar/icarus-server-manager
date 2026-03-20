import pytest
from PySide6.QtCore import Qt
from unittest.mock import MagicMock, patch
from icarus_sentinel.ui.save_sync import SaveSyncView

@pytest.fixture
def mock_app():
    app = MagicMock()
    app.server_manager = MagicMock()
    app.server_manager.auto_sync_on_start = True
    app.server_manager.auto_sync_on_stop = True
    app.server_manager.selected_steam_id = "123"
    app.server_manager.state = {"last_sync_timestamp": None}
    
    app.save_sync_manager = MagicMock()
    app.save_sync_manager.list_local_steam_ids.return_value = ["123", "456"]
    
    app.controller = MagicMock()
    return app

def test_save_sync_view_load_settings(qtbot, mock_app):
    mock_app.server_manager.auto_sync_on_start = True
    mock_app.server_manager.selected_steam_id = "456"
    
    view = SaveSyncView(app=mock_app)
    qtbot.addWidget(view)
    
    assert view.sync_on_start_toggle.isChecked() is True
    assert view.steam_id_dropdown.currentText() == "456"

def test_save_sync_view_toggle_start(qtbot, mock_app):
    view = SaveSyncView(app=mock_app)
    qtbot.addWidget(view)
    
    # Initially True (per new defaults)
    assert mock_app.server_manager.auto_sync_on_start is True
    
    # Click to toggle OFF
    qtbot.mouseClick(view.sync_on_start_toggle, Qt.LeftButton)
    
    assert view.sync_on_start_toggle.isChecked() is False
    assert mock_app.server_manager.auto_sync_on_start is False
    mock_app.server_manager.save_state.assert_called()

def test_save_sync_view_change_steam_id(qtbot, mock_app):
    view = SaveSyncView(app=mock_app)
    qtbot.addWidget(view)
    
    view.steam_id_dropdown.setCurrentText("456")
    
    assert mock_app.server_manager.selected_steam_id == "456"
    mock_app.server_manager.save_state.assert_called()
