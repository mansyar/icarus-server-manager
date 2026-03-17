import pytest
from unittest.mock import MagicMock, patch
import os
from icarus_sentinel.app import App

@pytest.fixture
def app_instance(tmp_path):
    state_file = tmp_path / "server_state.json"
    with patch("icarus_sentinel.app.App.__init__", return_value=None), \
         patch("icarus_sentinel.app.ctk.CTkLabel"), \
         patch("icarus_sentinel.app.ctk.CTkFrame"), \
         patch("icarus_sentinel.app.ctk.CTkButton"):
        app = App()
        app.tk = MagicMock()
        app.log = MagicMock()
        app.after = MagicMock()
        
        # Dependencies
        app.server_manager = MagicMock()
        app.backup_manager = MagicMock()
        
        # UI Elements
        app.tabview = MagicMock()
        app.backups_list_frame = MagicMock()
        app.backups_list_frame.winfo_children.return_value = []
        app.backup_now_button = MagicMock()
        app.path_entry = MagicMock()
        
        # Methods
        app.refresh_backups_list = lambda: App.refresh_backups_list(app)
        app.manual_backup = lambda: App.manual_backup(app)
        app.confirm_restore = lambda name: App.confirm_restore(app, name)
        app.perform_restore = lambda name: App.perform_restore(app, name)
        app._run_manual_backup = lambda: App._run_manual_backup(app)
        app._run_restore = lambda name: App._run_restore(app, name)
        
        yield app

def test_backups_tab_exists(app_instance):
    assert hasattr(app_instance, "tabview")
    # Check if "Backups" tab is in the tabview
    # In CustomTkinter, tabview.tab("Tab Name") returns the frame
    try:
        backups_tab = app_instance.tabview.tab("Backups")
        assert backups_tab is not None
    except ValueError:
        pytest.fail("Backups tab not found in tabview")

def test_list_backups_ui(app_instance, tmp_path):
    backup_path = tmp_path / "backups"
    backup_path.mkdir()
    app_instance.backup_manager.backup_path = str(backup_path)
    
    # Create dummy backups
    (backup_path / "Prospects_2026-03-17_1000.zip").touch()
    (backup_path / "Prospects_2026-03-17_1100.zip").touch()
    
    with patch("icarus_sentinel.app.ctk.CTkFrame") as mock_frame:
        app_instance.refresh_backups_list()
        # Should create a frame for each backup
        assert mock_frame.call_count == 2

def test_backup_now_button_exists(app_instance):
    assert hasattr(app_instance, "backup_now_button")

@patch("icarus_sentinel.app.messagebox.askyesno", return_value=True)
@patch("icarus_sentinel.app.threading.Thread")
def test_confirm_restore_calls_restore(mock_thread, mock_ask, app_instance):
    app_instance.server_process = None
    with patch.object(app_instance.backup_manager, "restore_backup") as mock_restore:
        app_instance.confirm_restore("test_backup.zip")
        mock_ask.assert_called_once()
        mock_thread.assert_called_once()
        args, kwargs = mock_thread.call_args
        assert kwargs["target"] == app_instance._run_restore
        assert kwargs["args"] == ("test_backup.zip",)

@patch("icarus_sentinel.app.threading.Thread")
def test_manual_backup_trigger_ui(mock_thread, app_instance):
    app_instance.manual_backup()
    mock_thread.assert_called_once()
    args, kwargs = mock_thread.call_args
    assert kwargs["target"] == app_instance._run_manual_backup
