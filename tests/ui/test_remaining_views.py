import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QWidget
from icarus_sentinel.ui.config import ConfigView
from icarus_sentinel.ui.backups import BackupsView
from icarus_sentinel.ui.save_sync import SaveSyncView

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
    app.backup_manager = MagicMock()
    app.backup_manager.server_path = "/mock/path"
    app.backup_manager.backup_path = "/mock/backups"
    app.backup_manager.interval_minutes = 30.0
    app.backup_manager.retention_limit = 50
    return app

def test_config_view_initialization(qtbot, mock_app):
    view = ConfigView(app=mock_app)
    qtbot.addWidget(view)
    assert isinstance(view, QWidget)

@patch("os.path.exists")
@patch("os.listdir")
def test_backups_view_initialization(mock_listdir, mock_exists, qtbot, mock_app):
    mock_exists.return_value = True
    mock_listdir.return_value = []
    view = BackupsView(app=mock_app)
    qtbot.addWidget(view)
    assert isinstance(view, QWidget)

def test_save_sync_view_initialization(qtbot, mock_app):
    view = SaveSyncView(app=mock_app)
    qtbot.addWidget(view)
    assert isinstance(view, QWidget)
