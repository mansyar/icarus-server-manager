import pytest
from unittest.mock import MagicMock, patch
import os
from app import App

@pytest.fixture
def app_instance():
    with patch("app.ctk.CTk.title"), \
         patch("app.ctk.CTk.geometry"), \
         patch("app.BackupManager.start_timer"):
        app = App()
        # Mocking UI elements that might cause issues in non-GUI environment
        app.log = MagicMock()
        app.after = MagicMock()
        yield app
        app.destroy()

def test_run_server_with_update_on_launch(app_instance):
    # Setup: Update on Launch is checked
    app_instance.update_on_launch_var.set(True)
    app_instance.path_entry.delete(0, "end")
    app_instance.path_entry.insert(0, "C:/icarus")
    
    # Mocks
    app_instance.steam_manager.install_server = MagicMock()
    app_instance.server_manager.start_server = MagicMock()
    app_instance.server_manager.stream_logs = MagicMock()
    
    mock_install_process = MagicMock()
    mock_install_process.wait.return_value = 0
    mock_install_process.stdout = None
    app_instance.steam_manager.install_server.return_value = mock_install_process
    
    # Action
    app_instance.run_server("C:/icarus/IcarusServer.exe")
    
    # Verify: install_server was called BEFORE start_server
    app_instance.steam_manager.install_server.assert_called_once_with("C:/icarus")
    app_instance.server_manager.start_server.assert_called_once()

def test_run_server_without_update_on_launch(app_instance):
    # Setup: Update on Launch is UNchecked
    app_instance.update_on_launch_var.set(False)
    
    # Mocks
    app_instance.steam_manager.install_server = MagicMock()
    app_instance.server_manager.start_server = MagicMock()
    app_instance.server_manager.stream_logs = MagicMock()
    
    # Action
    app_instance.run_server("C:/icarus/IcarusServer.exe")
    
    # Verify: install_server was NOT called
    app_instance.steam_manager.install_server.assert_not_called()
    app_instance.server_manager.start_server.assert_called_once()
