import pytest
from unittest.mock import MagicMock, patch
from app import App
import customtkinter as ctk

@pytest.fixture
def app_instance():
    with patch("app.ctk.CTk.title"), \
         patch("app.ctk.CTk.geometry"), \
         patch("tkinter.Misc.after") as mock_after, \
         patch("app.App.update_monitoring"): # Don't start loop automatically
        
        # Mock after to call the function immediately if delay is 0
        def side_effect(delay, func, *args):
            if delay == 0:
                if callable(func):
                    func(*args)
            return "mock_after_id"
        mock_after.side_effect = side_effect
        
        app = App()
        app.ram_label = MagicMock(name="ram_label_mock")
        app.log = MagicMock()
        # Set a real value for threshold to avoid mock comparison issues
        app.server_manager.ram_threshold_gb = 16.0
        yield app
        if hasattr(app, "destroy"):
            app.destroy()

def test_update_monitoring_updates_ui_on_warning(app_instance):
    app_instance.server_process = 1234
    app_instance.server_manager.get_resource_usage = MagicMock(return_value={"cpu": 10.0, "ram_gb": 17.0})
    app_instance.server_manager.state["status"] = "warning"
    
    app_instance.update_monitoring_once() # We'll add this helper to avoid the 5s loop in tests
    
    # Check if ram_label was configured with warning color
    # CustomTkinter warning color might be "orange" or similar.
    app_instance.ram_label.configure.assert_any_call(text_color="orange")
    app_instance.ram_label.configure.assert_any_call(text="RAM: 17.0GB")

def test_update_monitoring_logs_warning_once(app_instance):
    app_instance.server_process = 1234
    app_instance.server_manager.get_resource_usage = MagicMock(return_value={"cpu": 10.0, "ram_gb": 17.0})
    
    # Initial state is running
    app_instance.server_manager.state["status"] = "running"
    
    # Trigger warning
    def side_effect(*args):
        app_instance.server_manager.state["status"] = "warning"
        return {"cpu": 10.0, "ram_gb": 17.0}
    
    app_instance.server_manager.get_resource_usage.side_effect = side_effect
    
    app_instance.update_monitoring_once()
    
    app_instance.log.assert_called_with("WARNING: High RAM usage detected! (>16.0GB)")

def test_save_settings_updates_threshold(app_instance):
    app_instance.threshold_entry = MagicMock()
    app_instance.threshold_entry.get.return_value = "18.5"
    
    app_instance.save_settings()
    
    assert app_instance.server_manager.ram_threshold_gb == 18.5
    app_instance.log.assert_called_with("Settings saved.")

def test_save_settings_updates_smart_restart(app_instance):
    app_instance.threshold_entry = MagicMock()
    app_instance.threshold_entry.get.return_value = "16.0"
    app_instance.smart_restart_var = MagicMock()
    app_instance.smart_restart_var.get.return_value = True
    app_instance.restart_time_entry = MagicMock()
    app_instance.restart_time_entry.get.return_value = "05:30"
    
    app_instance.save_settings()
    
    assert app_instance.server_manager.smart_restart_enabled is True
    assert app_instance.server_manager.smart_restart_time == "05:30"
    app_instance.log.assert_called_with("Settings saved.")

def test_update_monitoring_triggers_smart_restart(app_instance):
    app_instance.server_process = MagicMock()
    app_instance.path_entry = MagicMock()
    app_instance.path_entry.get.return_value = "C:/test"
    
    app_instance.get_server_executable = MagicMock(return_value="C:/test/exe")
    
    mock_new_proc = MagicMock()
    mock_new_proc.pid = 9999
    app_instance.server_manager.check_smart_restart = MagicMock(return_value=mock_new_proc)
    
    app_instance.update_monitoring_once()
    
    assert app_instance.server_process == mock_new_proc
    app_instance.log.assert_called_with("Smart Idle Restart triggered. New PID: 9999")
