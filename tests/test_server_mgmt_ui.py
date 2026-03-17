import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Define a mock base class
class MockCTk:
    def __init__(self, *args, **kwargs):
        pass
    def title(self, title):
        pass
    def geometry(self, geometry):
        pass
    def mainloop(self):
        pass
    def grid_columnconfigure(self, *args, **kwargs):
        pass
    def grid_rowconfigure(self, *args, **kwargs):
        pass
    def after(self, ms, func, *args):
        # Call immediately if ms is 0 (UI update), but not for long waits (monitoring loop)
        if ms == 0:
            func(*args)
    def configure(self, *args, **kwargs):
        pass
    def grid(self, *args, **kwargs):
        pass

class MockCTkFrame(MockCTk):
    pass

# Mock the entire customtkinter module
customtkinter = MagicMock()
customtkinter.CTk = MockCTk
customtkinter.CTkFrame = MockCTkFrame
customtkinter.CTkButton = MagicMock()
customtkinter.CTkTextbox = MagicMock()
customtkinter.CTkLabel = MagicMock()
customtkinter.CTkEntry = MagicMock()
sys.modules["customtkinter"] = customtkinter

# Mock steam_manager and server_manager
sys.modules["steam_manager"] = MagicMock()
mock_server_manager = MagicMock()
sys.modules["server_manager"] = mock_server_manager
# Set default state to avoid psutil errors in App.__init__
mock_server_manager.ServerProcessManager.return_value.state = {"pid": None, "status": "stopped"}

import app
from app import App

@pytest.fixture
def app_instance():
    with patch("app.ctk.CTk.title"), \
         patch("app.ctk.CTk.geometry"):
        return App()

def test_ui_has_server_mgmt_buttons(app_instance):
    assert hasattr(app_instance, "start_button")
    assert hasattr(app_instance, "stop_button")
    assert hasattr(app_instance, "restart_button")
    assert hasattr(app_instance, "cpu_label")
    assert hasattr(app_instance, "ram_label")

@patch("app.threading.Thread")
@patch("app.os.path.exists")
def test_start_server_ui(mock_exists, mock_thread, app_instance):
    mock_exists.return_value = True
    app_instance.path_entry = MagicMock()
    # Mock the entry to return a path
    app_instance.path_entry.get.return_value = "C:/icarus/IcarusServer.exe"
    
    app_instance.start_server()
    
    mock_thread.assert_called_once()
    args, kwargs = mock_thread.call_args
    assert kwargs["target"] == app_instance.run_server

def test_run_server_streams_logs(app_instance):
    app_instance.server_manager = MagicMock()
    mock_process = MagicMock()
    app_instance.server_manager.start_server.return_value = mock_process
    
    # Mock stream_logs to call the callback once
    def mock_stream(proc, callback):
        callback("test log line")
        
    app_instance.server_manager.stream_logs.side_effect = mock_stream
    app_instance.log = MagicMock()
    app_instance.on_server_exit = MagicMock()
    
    app_instance.run_server("C:/test.exe")
    
    app_instance.server_manager.start_server.assert_called_once_with("C:/test.exe")
    app_instance.log.assert_any_call("test log line")
    app_instance.on_server_exit.assert_called_once()

def test_update_monitoring(app_instance):
    app_instance.server_manager = MagicMock()
    app_instance.server_process = MagicMock()
    app_instance.server_manager.get_resource_usage.return_value = {"cpu": 25.0, "ram_gb": 1.2}
    
    app_instance.cpu_label = MagicMock()
    app_instance.ram_label = MagicMock()
    # We want to use the REAL after mock from the class, not a new MagicMock
    # Actually, app_instance.after is already the mock from MockCTk
    
    app_instance.update_monitoring()
    
    app_instance.cpu_label.configure.assert_any_call(text="CPU: 25.0%")
    app_instance.ram_label.configure.assert_any_call(text="RAM: 1.2GB")

def test_stop_server_ui(app_instance):
    app_instance.server_manager = MagicMock()
    app_instance.server_process = MagicMock()
    app_instance.log = MagicMock()
    
    app_instance.stop_server()
    
    app_instance.server_manager.stop_server.assert_called_once_with(app_instance.server_process)
    app_instance.log.assert_any_call("Stopping server...")

@patch("app.os.path.exists")
def test_restart_server_ui(mock_exists, app_instance):
    mock_exists.return_value = True
    app_instance.server_manager = MagicMock()
    app_instance.server_process = MagicMock()
    app_instance.log = MagicMock()
    app_instance.start_server = MagicMock()
    
    app_instance.restart_server()
    
    app_instance.server_manager.stop_server.assert_called_once_with(app_instance.server_process)
    app_instance.start_server.assert_called_once()
