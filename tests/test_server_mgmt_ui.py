import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import psutil

@pytest.fixture
def app_instance():
    from app import App
    with patch("app.ctk.CTk.title"), \
         patch("app.ctk.CTk.geometry"):
        app = App()
        yield app
        if hasattr(app, "destroy"):
            app.destroy()

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
    app_instance.path_entry.get.return_value = "C:/icarus"
    
    with patch.object(app_instance, "get_server_executable") as mock_get_exe:
        mock_get_exe.return_value = "C:/icarus/IcarusServer.exe"
        app_instance.start_server()
        
    mock_thread.assert_called_once()
    args, kwargs = mock_thread.call_args
    assert kwargs["target"] == app_instance.run_server

def test_run_server_streams_logs(app_instance):
    app_instance.server_manager = MagicMock()
    mock_process = MagicMock()
    app_instance.server_manager.start_server.return_value = mock_process
    
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
    
    app_instance.update_monitoring()
    
    app_instance.cpu_label.configure.assert_any_call(text="CPU: 25.0%")
    app_instance.ram_label.configure.assert_any_call(text="RAM: 1.2GB")

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

@patch("app.psutil.Process")
def test_recover_state_success(mock_psutil_process, app_instance):
    app_instance.server_manager.state = {"pid": 1234, "status": "running"}
    mock_p = mock_psutil_process.return_value
    mock_p.is_running.return_value = True
    
    app_instance.log = MagicMock()
    app_instance.recover_state()
    
    assert app_instance.server_process == 1234
    app_instance.log.assert_any_call("Recovered existing server process (PID: 1234)")

@patch("app.psutil.Process")
def test_recover_state_not_running(mock_psutil_process, app_instance):
    app_instance.server_manager.state = {"pid": 1234, "status": "running"}
    mock_p = mock_psutil_process.return_value
    mock_p.is_running.return_value = False
    
    app_instance.reset_state = MagicMock()
    app_instance.recover_state()
    
    app_instance.reset_state.assert_called_once()

def test_get_server_executable_resolves_shipping(app_instance):
    with patch("app.os.path.exists") as mock_exists:
        # Mocking exists to return True for the shipping exe
        mock_exists.side_effect = lambda path: "Shipping.exe" in path
        exe = app_instance.get_server_executable("C:/icarus")
        assert "Shipping.exe" in exe

def test_get_server_executable_fallback(app_instance):
    with patch("app.os.path.exists") as mock_exists:
        # Mocking exists to return True ONLY for the root exe
        mock_exists.side_effect = lambda path: path.endswith("IcarusServer.exe")
        exe = app_instance.get_server_executable("C:/icarus")
        assert exe == os.path.join("C:/icarus", "IcarusServer.exe")

def test_on_server_exit_resets_ui(app_instance):
    app_instance.server_process = MagicMock()
    app_instance.start_button = MagicMock()
    app_instance.cpu_label = MagicMock()
    
    app_instance.on_server_exit()
    
    assert app_instance.server_process is None
    app_instance.start_button.configure.assert_called_with(state="normal")
    app_instance.cpu_label.configure.assert_called_with(text="CPU: 0.0%")
