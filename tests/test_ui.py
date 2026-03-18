import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# app will be reloaded by conftest.py if needed, but we need to import it here for tests
# However, to avoid import errors before the fixture runs, we can import it inside fixtures or tests
# or just rely on the fact that conftest.py mocks sys.modules before any test in this file runs.

@pytest.fixture
def app_instance():
    from icarus_sentinel.app import App
    with patch("icarus_sentinel.app.App.__init__", return_value=None):
        app = App()
        app.tk = MagicMock()
        
        # Controller
        app.controller = MagicMock()
        
        # Dependencies
        app.steam_manager = MagicMock()
        app.ini_manager = None
        app.save_sync_manager = MagicMock()
        app.server_manager = MagicMock()
        
        # UI Elements
        app.console_output = MagicMock()
        app.install_button = MagicMock()
        app.path_entry = MagicMock()
        app.browse_button = MagicMock()
        
        def side_effect(delay, func, *args):
            if delay == 0 and callable(func):
                func(*args)
            return "mock_after_id"
        app.after = MagicMock(side_effect=side_effect)
        
        # Methods
        app.log = lambda msg: App.log(app, msg)
        app.start_install = lambda: App.start_install(app)
        app.browse_path = lambda: App.browse_path(app)
        app.reset_ui = lambda: App.reset_ui(app)
        
        yield app

def test_app_initialization(app_instance):
    assert hasattr(app_instance, "console_output")
    assert hasattr(app_instance, "install_button")
    assert hasattr(app_instance, "path_entry")
    assert hasattr(app_instance, "browse_button")

def test_log(app_instance):
    app_instance.console_output = MagicMock()
    app_instance.log("test message")
    app_instance.console_output.insert.assert_called_with("end", "test message\n")

def test_start_install(app_instance):
    app_instance.path_entry = MagicMock()
    app_instance.path_entry.get.return_value = "C:/test_path"
    app_instance.install_button = MagicMock()
    
    app_instance.start_install()
    
    app_instance.install_button.configure.assert_called_with(state="disabled")
    app_instance.controller.run_install.assert_called_once_with("C:/test_path")

@patch("icarus_sentinel.app.filedialog.askdirectory")
def test_browse_path(mock_askdirectory, app_instance):
    mock_askdirectory.return_value = "C:/new_path"
    app_instance.path_entry = MagicMock()
    
    app_instance.browse_path()
    
    mock_askdirectory.assert_called_once()
    app_instance.path_entry.delete.assert_called_with(0, "end")
    app_instance.path_entry.insert.assert_called_with(0, "C:/new_path")

def test_main():
    from icarus_sentinel.app import main
    with patch("icarus_sentinel.app.App") as MockApp:
        instance = MockApp.return_value
        main()
        MockApp.assert_called_once()
        instance.mainloop.assert_called_once()

@patch("icarus_sentinel.app.messagebox.showinfo")
def test_show_about(mock_showinfo, app_instance):
    from icarus_sentinel.app import App
    app_instance.show_about = lambda: App.show_about(app_instance)
    app_instance.show_about()
    mock_showinfo.assert_called_once()
    args, kwargs = mock_showinfo.call_args
    assert "Icarus Sentinel" in args[0]
    assert "v1.0.0" in args[1]
