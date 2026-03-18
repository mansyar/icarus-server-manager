"""Integration tests for the server launch sequence with update checks."""

import pytest
from unittest.mock import MagicMock, patch
import os
from icarus_sentinel.app import App
from icarus_sentinel.controller import Controller

@pytest.fixture
def app_instance():
    with patch("icarus_sentinel.app.App.__init__", return_value=None):
        app = App()
        app.tk = MagicMock()
        app.log = MagicMock()
        
        def side_effect(delay, func, *args):
            if delay == 0 and callable(func):
                func(*args)
            return "mock_after_id"
        app.after = MagicMock(side_effect=side_effect)
        
        # Controller
        app.controller = Controller(app)
        
        # Dependencies
        app.server_manager = MagicMock()
        app.steam_manager = MagicMock()
        
        # UI Elements
        app.update_on_launch_var = MagicMock()
        app.path_entry = MagicMock()
        app.on_server_exit = MagicMock()
        
        yield app

def test_run_server_with_update_on_launch(app_instance):
    # Setup: Update on Launch is checked
    app_instance.update_on_launch_var.get.return_value = True
    app_instance.path_entry.get.return_value = "C:/icarus"
    
    # Mocks
    app_instance.steam_manager.install_server = MagicMock()
    app_instance.server_manager.start_server = MagicMock()
    app_instance.server_manager.stream_logs = MagicMock()
    
    mock_install_process = MagicMock()
    mock_install_process.wait.return_value = 0
    mock_install_process.stdout = None
    app_instance.steam_manager.install_server.return_value = mock_install_process
    
    # Action
    app_instance.controller.run_server("C:/icarus/IcarusServer.exe")
    
    # Verify: install_server was called BEFORE start_server
    app_instance.steam_manager.install_server.assert_called_once_with("C:/icarus")
    app_instance.server_manager.start_server.assert_called_once()

def test_run_server_without_update_on_launch(app_instance):
    # Setup: Update on Launch is UNchecked
    app_instance.update_on_launch_var.get.return_value = False
    
    # Mocks
    app_instance.steam_manager.install_server = MagicMock()
    app_instance.server_manager.start_server = MagicMock()
    app_instance.server_manager.stream_logs = MagicMock()
    
    # Action
    app_instance.controller.run_server("C:/icarus/IcarusServer.exe")
    
    # Verify: install_server was NOT called
    app_instance.steam_manager.install_server.assert_not_called()
    app_instance.server_manager.start_server.assert_called_once()
