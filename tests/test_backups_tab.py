import pytest
from unittest.mock import MagicMock, patch
import os
from app import App

@pytest.fixture
def app_instance(tmp_path):
    state_file = tmp_path / "server_state.json"
    with patch("app.ctk.CTk.title"), \
         patch("app.ctk.CTk.geometry"), \
         patch("tkinter.Misc.after"), \
         patch("app.App.update_monitoring"):
        
        app = App(state_file=str(state_file))
        app.log = MagicMock()
        yield app
        if hasattr(app, "destroy"):
            app.destroy()

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
    
    app_instance.refresh_backups_list()
    
    # Verify that the UI list contains these backups
    # (Implementation detail: I'll likely use a scrollable frame with labels/buttons)
    assert hasattr(app_instance, "backups_list_frame")
    # This might be tricky to test without deeper inspection of CTk elements
    # I'll just check if a method was called or a list was updated for now
    # Or check children of the frame
    children = app_instance.backups_list_frame.winfo_children()
    # Depending on how I implement it, this might change. 
    # Let's assume 2 backups = at least 2 widgets in the list.
    assert len(children) >= 2
