import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import psutil
from icarus_sentinel.app import App
from icarus_sentinel.controller import Controller

@pytest.fixture
def app_instance():
    from icarus_sentinel.app import App
    with patch("icarus_sentinel.app.App.__init__", return_value=None):
        app = App()
        # Controller
        app.controller = Controller(app)
        
        # Setup minimal state for tests
        app.server_manager = MagicMock()
        app.steam_manager = MagicMock()
        app.backup_manager = MagicMock()
        
        app.orbital_launch_btn = MagicMock()
        app.cpu_usage_label = MagicMock()
        app.ram_usage_label = MagicMock()
        app.cpu_progress_bar = MagicMock()
        app.ram_progress_bar = MagicMock()
        app.path_entry = MagicMock()
        
        app.log = MagicMock()
        
        # Mock 'after' to execute the callback immediately
        def mock_after(delay, func, *args):
            if callable(func):
                func(*args)
            return "mock_after_id"
        app.after = MagicMock(side_effect=mock_after)
        
        app.server_process = None
        app.selected_steam_id = "test_steam_id"
        app.update_on_launch_var = MagicMock()
        app.update_on_launch_var.get.return_value = False
        
        # Link methods we want to test
        app.start_server = lambda: App.start_server(app)
        app.stop_server = lambda: App.stop_server(app)
        app.restart_server = lambda: App.restart_server(app)
        app.on_server_exit = lambda: App.on_server_exit(app)
        app.update_monitoring_once = lambda: App.update_monitoring_once(app)
        app.launch_server = lambda path: App.launch_server(app, path)
        
        yield app

def test_ui_has_server_mgmt_buttons(app_instance):
    assert hasattr(app_instance, "orbital_launch_btn")
    assert hasattr(app_instance, "cpu_usage_label")
    assert hasattr(app_instance, "ram_usage_label")

@patch("icarus_sentinel.app.os.path.exists")
def test_start_server_ui(mock_exists, app_instance):
    mock_exists.return_value = True
    app_instance.path_entry.get.return_value = "C:/icarus"
    
    with patch.object(app_instance.controller, "get_server_executable") as mock_get_exe, \
         patch.object(app_instance.controller, "sync_saves") as mock_sync_saves, \
         patch.object(app_instance.server_manager, "get_available_system_ram_pct", return_value=50.0):
        mock_get_exe.return_value = "C:/icarus/IcarusServer.exe"
        app_instance.start_server()
        
    mock_sync_saves.assert_called_once()

def test_run_server_streams_logs(app_instance):
    app_instance.server_manager = MagicMock()
    mock_process = MagicMock()
    app_instance.server_manager.start_server.return_value = mock_process
    
    def mock_stream(proc, callback):
        callback("test log line")
        
    app_instance.server_manager.stream_logs.side_effect = mock_stream
    app_instance.log = MagicMock()
    app_instance.on_server_exit = MagicMock()
    
    app_instance.controller.run_server("C:/test.exe")
    
    app_instance.server_manager.start_server.assert_called_once_with("C:/test.exe")
    app_instance.log.assert_any_call("test log line")
    app_instance.on_server_exit.assert_called_once()

def test_update_monitoring(app_instance):
    app_instance.server_manager.get_resource_usage.return_value = {"cpu": 25.0, "ram_gb": 1.2}
    app_instance.server_manager.should_smart_restart.return_value = False
    app_instance.server_process = MagicMock()
    app_instance.server_manager.state = {"status": "running"}
    app_instance.server_manager.ram_threshold_gb = 16.0
    
    app_instance.update_monitoring_once()
    
    app_instance.cpu_usage_label.configure.assert_any_call(text="CPU USAGE: 25.0%")
    app_instance.ram_usage_label.configure.assert_any_call(text="RAM USAGE: 1.2GB / 16.0GB")

def test_stop_server_ui_popen(app_instance):
    app_instance.server_manager = MagicMock()
    app_instance.server_process = MagicMock() # Not an int
    app_instance.log = MagicMock()
    
    app_instance.stop_server()
    
    app_instance.server_manager.stop_server.assert_called_once_with(app_instance.server_process)
    app_instance.log.assert_any_call("Stopping server...")

def test_stop_server_ui_recovered(app_instance):
    app_instance.server_manager = MagicMock()
    app_instance.server_process = 1234 # Recovered PID
    app_instance.log = MagicMock()
    app_instance.on_server_exit = MagicMock()
    
    app_instance.stop_server()
    
    app_instance.server_manager.stop_server.assert_called_once_with(1234)
    app_instance.on_server_exit.assert_called_once()

@patch("icarus_sentinel.app.os.path.exists")
def test_restart_server_ui(mock_exists, app_instance):
    mock_exists.return_value = True
    app_instance.server_manager = MagicMock()
    app_instance.server_process = MagicMock()
    app_instance.log = MagicMock()
    app_instance.start_server = MagicMock()
    
    app_instance.restart_server()
    
    app_instance.server_manager.stop_server.assert_called_once_with(app_instance.server_process)
    app_instance.start_server.assert_called_once()

@patch("psutil.Process")
def test_recover_state_success(mock_psutil_process, app_instance):
    app_instance.server_manager.state = {"pid": 1234, "status": "running"}
    mock_p = mock_psutil_process.return_value
    mock_p.is_running.return_value = True
    
    app_instance.log = MagicMock()
    app_instance.controller.recover_state()
    
    assert app_instance.server_process == 1234
    app_instance.log.assert_any_call("Recovered existing server process (PID: 1234)")

@patch("psutil.Process")
def test_recover_state_not_running(mock_psutil_process, app_instance):
    app_instance.server_manager.state = {"pid": 1234, "status": "running"}
    mock_p = mock_psutil_process.return_value
    mock_p.is_running.return_value = False
    
    app_instance.controller.reset_state = MagicMock()
    app_instance.controller.recover_state()
    
    app_instance.controller.reset_state.assert_called_once()

def test_on_server_exit_resets_ui(app_instance):
    app_instance.server_process = MagicMock()
    app_instance.orbital_launch_btn = MagicMock()
    
    with patch.object(app_instance.controller, "sync_saves") as mock_sync:
        app_instance.on_server_exit()
        
        assert app_instance.server_process is None
        app_instance.orbital_launch_btn.configure.assert_called()
        mock_sync.assert_called_once()
