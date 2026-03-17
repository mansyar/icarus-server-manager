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
        # Immediately call the func to simulate it being called
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

# Mock steam_manager
mock_steam_manager = MagicMock()
sys.modules["steam_manager"] = mock_steam_manager

import app
from app import App

@pytest.fixture
def app_instance():
    with patch.object(App, "title"), \
         patch.object(App, "geometry"):
        return App()

def test_app_initialization(app_instance):
    assert hasattr(app_instance, "console_output")
    assert hasattr(app_instance, "install_button")
    assert hasattr(app_instance, "path_entry")
    assert hasattr(app_instance, "browse_button")

def test_log(app_instance):
    app_instance.console_output = MagicMock()
    app_instance.log("test message")
    app_instance.console_output.insert.assert_called_with("end", "test message\n")

@patch("threading.Thread")
def test_start_install(mock_thread, app_instance):
    app_instance.path_entry = MagicMock()
    app_instance.path_entry.get.return_value = "C:/test_path"
    app_instance.install_button = MagicMock()
    
    app_instance.start_install()
    
    app_instance.install_button.configure.assert_called_with(state="disabled")
    mock_thread.assert_called_once()
    args, kwargs = mock_thread.call_args
    assert kwargs["target"] == app_instance.run_install
    assert kwargs["args"] == ("C:/test_path",)

@patch("app.SteamManager")
def test_run_install(mock_steam_manager_class, app_instance):
    mock_steam_manager_instance = mock_steam_manager_class.return_value
    app_instance.steam_manager = mock_steam_manager_instance
    
    mock_process = MagicMock()
    mock_steam_manager_instance.install_server.return_value = mock_process
    mock_process.stdout.readline.side_effect = ["line1", "line2", ""]
    mock_process.wait.return_value = 0
    
    app_instance.log = MagicMock()
    app_instance.install_button = MagicMock()
    app_instance.browse_button = MagicMock()
    app_instance.path_entry = MagicMock()
    
    app_instance.run_install("C:/test_path")
    
    mock_steam_manager_instance.install_server.assert_called_once_with("C:/test_path")
    assert app_instance.log.call_count >= 3
    app_instance.install_button.configure.assert_called_with(state="normal")

@patch("app.filedialog.askdirectory")
def test_browse_path(mock_askdirectory, app_instance):
    mock_askdirectory.return_value = "C:/new_path"
    app_instance.path_entry = MagicMock()
    
    app_instance.browse_path()
    
    mock_askdirectory.assert_called_once()
    app_instance.path_entry.delete.assert_called_with(0, "end")
    app_instance.path_entry.insert.assert_called_with(0, "C:/new_path")

def test_main():
    with patch("app.App") as MockApp:
        instance = MockApp.return_value
        app.main()
        MockApp.assert_called_once()
        instance.mainloop.assert_called_once()
