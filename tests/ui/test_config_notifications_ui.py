import pytest
from unittest.mock import MagicMock
from icarus_sentinel.ui.config import ConfigView

@pytest.fixture
def mock_app():
    app = MagicMock()
    app.ini_manager = MagicMock()
    app.ini_manager.get_setting.return_value = "" 
    app.ini_manager.get_raw_text.return_value = ""
    app.save_sync_manager = MagicMock()
    app.save_sync_manager.list_local_steam_ids.return_value = []
    
    app.server_manager = MagicMock()
    app.server_manager.state = {}
    app.server_manager.ram_threshold_gb = 16.0
    app.server_manager.smart_restart_enabled = False
    app.server_manager.smart_restart_time = "04:00"
    app.server_manager.notify_server_started = True
    app.server_manager.notify_player_activity = True
    app.server_manager.notify_server_error = True
    
    app.backup_manager = MagicMock()
    app.backup_manager.server_path = "/mock/path"
    app.backup_manager.backup_path = "/mock/backups"
    app.backup_manager.interval_minutes = 30.0
    app.backup_manager.retention_limit = 50
    return app

def test_config_view_has_notification_checkboxes(qtbot, mock_app):
    """Verify that notification checkboxes exist in ConfigView."""
    view = ConfigView(app=mock_app)
    qtbot.addWidget(view)
    
    assert hasattr(view, "notify_server_started_cb")
    assert hasattr(view, "notify_player_activity_cb")
    assert hasattr(view, "notify_server_error_cb")

def test_config_view_loads_notification_settings(qtbot, mock_app):
    """Verify that notification settings are loaded into checkboxes."""
    mock_app.server_manager.notify_server_started = False
    mock_app.server_manager.notify_player_activity = True
    mock_app.server_manager.notify_server_error = False
    
    view = ConfigView(app=mock_app)
    qtbot.addWidget(view)
    
    assert view.notify_server_started_cb.isChecked() is False
    assert view.notify_player_activity_cb.isChecked() is True
    assert view.notify_server_error_cb.isChecked() is False

def test_config_view_saves_notification_settings(qtbot, mock_app):
    """Verify that clicking save updates the controller with new settings."""
    view = ConfigView(app=mock_app)
    qtbot.addWidget(view)
    
    # Change UI state
    view.notify_server_started_cb.setChecked(True)
    view.notify_player_activity_cb.setChecked(False)
    view.notify_server_error_cb.setChecked(True)
    
    # Trigger save
    view._on_save_sentinel()
    
    # Verify controller was called with correct data
    mock_app.controller.save_sentinel_settings.assert_called_once()
    saved_data = mock_app.controller.save_sentinel_settings.call_args[0][0]
    assert saved_data["notify_server_started"] is True
    assert saved_data["notify_player_activity"] is False
    assert saved_data["notify_server_error"] is True
