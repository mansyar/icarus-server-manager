import pytest
from unittest.mock import MagicMock, patch
from icarus_sentinel.app import App
from icarus_sentinel.controller import Controller

@pytest.fixture
def app_instance(tmp_path):
    with patch("icarus_sentinel.app.App.__init__", return_value=None):
        app = App()
        app.tk = MagicMock()
        app.log = MagicMock()
        
        # Controller
        app.controller = Controller(app)
        
        # Mock dependencies
        app.server_manager = MagicMock()
        app.server_manager.ram_threshold_gb = 16.0
        app.server_manager.state = {"status": "running"}
        app.steam_manager = MagicMock()
        app.backup_manager = MagicMock()
        
        # Mock UI Elements
        app.ram_usage_label = MagicMock()
        app.cpu_usage_label = MagicMock()
        app.ram_progress_bar = MagicMock()
        app.cpu_progress_bar = MagicMock()
        app.orbital_launch_btn = MagicMock()
        app.path_entry = MagicMock()
        app.update_on_launch_var = MagicMock()
        app.threshold_entry = MagicMock()
        app.smart_restart_var = MagicMock()
        app.restart_time_entry = MagicMock()
        app.backup_interval_entry = MagicMock()
        app.backup_retention_entry = MagicMock()
        
        # Mock after to call the function immediately if delay is 0
        def side_effect(delay, func, *args):
            if delay == 0:
                if callable(func):
                    func(*args)
            return "mock_after_id"
        app.after = MagicMock(side_effect=side_effect)
        
        # Link methods
        app.update_monitoring_once = lambda: App.update_monitoring_once(app)
        app.restart_server = lambda: App.restart_server(app)
        app.start_server = lambda: App.start_server(app)
        app.launch_server = lambda path: App.launch_server(app, path)
        app.save_settings = lambda: App.save_settings(app)
        
        yield app

def test_update_monitoring_updates_ui_on_warning(app_instance):
    app_instance.server_process = 1234
    app_instance.server_manager.get_resource_usage = MagicMock(return_value={"cpu": 10.0, "ram_gb": 17.0})
    app_instance.server_manager.state["status"] = "warning"
    
    app_instance.update_monitoring_once()
    
    app_instance.ram_usage_label.configure.assert_any_call(text_color="orange")
    app_instance.ram_usage_label.configure.assert_any_call(text="RAM USAGE: 17.0GB / 16.0GB")

def test_update_monitoring_logs_warning_once(app_instance):
    app_instance.server_process = 1234
    
    # Initial state is running
    app_instance.server_manager.state["status"] = "running"
    
    # Trigger warning
    def side_effect(*args):
        app_instance.server_manager.state["status"] = "warning"
        return {"cpu": 10.0, "ram_gb": 17.0}
    
    app_instance.server_manager.get_resource_usage.side_effect = side_effect
    app_instance.server_manager.should_smart_restart.return_value = False
    
    app_instance.update_monitoring_once()
    
    app_instance.log.assert_any_call("WARNING: High RAM usage! (>16.0GB)")

def test_save_settings_updates_threshold(app_instance):
    app_instance.threshold_entry.get.return_value = "18.5"
    app_instance.smart_restart_var.get.return_value = False
    app_instance.restart_time_entry.get.return_value = "04:00"
    app_instance.backup_interval_entry.get.return_value = "30"
    app_instance.backup_retention_entry.get.return_value = "50"
    
    app_instance.save_settings()
    
    assert app_instance.server_manager.ram_threshold_gb == 18.5
    app_instance.log.assert_called_with("Settings saved.")

def test_save_settings_updates_smart_restart(app_instance):
    app_instance.threshold_entry.get.return_value = "16.0"
    app_instance.smart_restart_var.get.return_value = True
    app_instance.restart_time_entry.get.return_value = "05:30"
    app_instance.backup_interval_entry.get.return_value = "30"
    app_instance.backup_retention_entry.get.return_value = "50"
    
    app_instance.save_settings()
    
    assert app_instance.server_manager.smart_restart_enabled is True
    assert app_instance.server_manager.smart_restart_time == "05:30"
    app_instance.log.assert_called_with("Settings saved.")

def test_update_monitoring_triggers_smart_restart(app_instance):
    app_instance.server_process = MagicMock()
    app_instance.server_manager.get_resource_usage.return_value = {"cpu": 10.0, "ram_gb": 1.0}
    
    with patch.object(app_instance.server_manager, "should_smart_restart", return_value=True), \
         patch.object(app_instance, "restart_server") as mock_restart:
        
        app_instance.update_monitoring_once()
        mock_restart.assert_called_once()
        app_instance.log.assert_any_call("Smart Idle Restart condition met.")

def test_start_server_triggers_dialog_on_low_ram(app_instance):
    app_instance.path_entry.get.return_value = "C:/test"
    
    with patch("os.path.exists", return_value=True), \
         patch.object(app_instance.controller, "get_server_executable", return_value="C:/test/exe"), \
         patch.object(app_instance.server_manager, "get_available_system_ram_pct", return_value=5.0), \
         patch("icarus_sentinel.app.RamOptimizationDialog") as MockDialog:
        
        app_instance.start_server()
        MockDialog.assert_called_once()

def test_start_server_launches_immediately_on_normal_ram(app_instance):
    app_instance.path_entry.get.return_value = "C:/test"
    
    with patch("os.path.exists", return_value=True), \
         patch.object(app_instance.controller, "get_server_executable", return_value="C:/test/exe"), \
         patch.object(app_instance.server_manager, "get_available_system_ram_pct", return_value=15.0), \
         patch.object(app_instance, "launch_server") as mock_launch:
        
        app_instance.start_server()
        mock_launch.assert_called_once_with("C:/test/exe")
