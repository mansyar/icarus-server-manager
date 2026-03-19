import pytest
from unittest.mock import MagicMock
from PySide6.QtWidgets import QWidget
from icarus_sentinel.ui.config import ConfigView
from icarus_sentinel.ui.backups import BackupsView
from icarus_sentinel.ui.save_sync import SaveSyncView

@pytest.fixture
def mock_app():
    app = MagicMock()
    app.ini_manager = MagicMock()
    # Ensure get_setting returns a string to avoid PySide6 type errors
    app.ini_manager.get_setting.return_value = "" 
    app.save_sync_manager = MagicMock()
    app.save_sync_manager.list_local_steam_ids.return_value = []
    app.server_manager = MagicMock()
    app.server_manager.state = {}
    return app

def test_config_view_initialization(qtbot, mock_app):
    view = ConfigView(app=mock_app)
    qtbot.addWidget(view)
    assert isinstance(view, QWidget)

def test_backups_view_initialization(qtbot, mock_app):
    view = BackupsView(app=mock_app)
    qtbot.addWidget(view)
    assert isinstance(view, QWidget)

def test_save_sync_view_initialization(qtbot, mock_app):
    view = SaveSyncView(app=mock_app)
    qtbot.addWidget(view)
    assert isinstance(view, QWidget)
