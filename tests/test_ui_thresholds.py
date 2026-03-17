import pytest
from unittest.mock import MagicMock, patch
from app import App
import customtkinter as ctk

@pytest.fixture
def app_instance(tmp_path):
    state_file = tmp_path / "server_state.json"
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
        
        app = App(state_file=str(state_file))
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
    
    # Mock get_server_executable to return None to skip smart restart path search
    with patch.object(app_instance, "get_server_executable", return_value=None):
        app_instance.update_monitoring_once()
    
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
    
    # Mock get_server_executable to return None to skip smart restart path search
    with patch.object(app_instance, "get_server_executable", return_value=None), \
         patch.object(app_instance.server_manager, "should_smart_restart", return_value=False):
        app_instance.update_monitoring_once()
    
    app_instance.log.assert_any_call("WARNING: High RAM usage detected! (>16.0GB)")

def test_save_settings_updates_threshold(app_instance):
    app_instance.threshold_entry = MagicMock()
    app_instance.threshold_entry.get.return_value = "18.5"
    app_instance.smart_restart_var = MagicMock()
    app_instance.smart_restart_var.get.return_value = False
    app_instance.restart_time_entry = MagicMock()
    app_instance.restart_time_entry.get.return_value = "04:00"
    
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
    
    with patch.object(app_instance, "get_server_executable", return_value="C:/test/exe"), \
         patch.object(app_instance.server_manager, "should_smart_restart", return_value=True), \
         patch.object(app_instance, "restart_server") as mock_restart:
        
        app_instance.update_monitoring_once()
        mock_restart.assert_called_once()
        app_instance.log.assert_any_call("Smart Idle Restart condition met. Triggering restart...")

def test_start_server_triggers_dialog_on_low_ram(app_instance):
    app_instance.path_entry = MagicMock()
    app_instance.path_entry.get.return_value = "C:/test"
    
    with patch("os.path.exists", return_value=True), \
         patch.object(app_instance, "get_server_executable", return_value="C:/test/exe"), \
         patch.object(app_instance.server_manager, "get_available_system_ram_pct", return_value=5.0), \
         patch("app.RamOptimizationDialog") as MockDialog:
        
        app_instance.start_server()
        MockDialog.assert_called_once()

def test_start_server_launches_immediately_on_normal_ram(app_instance):
    app_instance.path_entry = MagicMock()
    app_instance.path_entry.get.return_value = "C:/test"
    
    with patch("os.path.exists", return_value=True), \
         patch.object(app_instance, "get_server_executable", return_value="C:/test/exe"), \
         patch.object(app_instance.server_manager, "get_available_system_ram_pct", return_value=15.0), \
         patch.object(app_instance, "launch_server") as mock_launch:
        
        app_instance.start_server()
        mock_launch.assert_called_once_with("C:/test/exe")
