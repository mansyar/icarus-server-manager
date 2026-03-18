import pytest
from unittest.mock import MagicMock, patch
import os

def test_app_grid_weights():
    # Import App here to ensure it uses the mocks from conftest
    from icarus_sentinel.app import App
    
    with patch("icarus_sentinel.app.DashboardView"), \
         patch("icarus_sentinel.app.ConfigView"), \
         patch("icarus_sentinel.app.SaveSyncView"), \
         patch("icarus_sentinel.app.BackupsView"), \
         patch("icarus_sentinel.app.ModsView"), \
         patch("icarus_sentinel.app.Controller"), \
         patch("icarus_sentinel.app.SteamManager"), \
         patch("icarus_sentinel.app.ServerProcessManager"), \
         patch("icarus_sentinel.app.BackupManager"), \
         patch("icarus_sentinel.app.ModManager"), \
         patch("icarus_sentinel.app.App.recover_state"), \
         patch("icarus_sentinel.app.App.update_monitoring"):
        
        # We manually call __init__ or let it run normally since CTk base is MockBase
        app = App()
        
        # Verify main window weights (called on self)
        app.grid_columnconfigure.assert_any_call(0, weight=0)
        app.grid_columnconfigure.assert_any_call(1, weight=1)
        
        # main_content_frame is also a MockBase
        app.main_content_frame.grid_rowconfigure.assert_any_call(0, weight=1)
        app.main_content_frame.grid_rowconfigure.assert_any_call(1, weight=0)

def test_server_view_responsiveness():
    from icarus_sentinel.ui.dashboard import DashboardView
    mock_app = MagicMock()
    mock_parent = MagicMock()
    
    # DashboardView inherits from CTkScrollableFrame which is MockBase
    view = DashboardView(mock_parent, mock_app)
    
    # In DashboardView.__init__, it should configure its columns
    view.grid_columnconfigure.assert_any_call(0, weight=1)
    
    # It also configures its own metrics_frame
    view.metrics_frame.grid_columnconfigure.assert_any_call(0, weight=1)
