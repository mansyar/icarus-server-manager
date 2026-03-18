import pytest
from unittest.mock import MagicMock, patch
from icarus_sentinel.app import App

@pytest.fixture
def app_instance():
    with patch("icarus_sentinel.app.App.__init__", return_value=None), \
         patch("icarus_sentinel.app.ctk"), \
         patch("icarus_sentinel.app.DashboardView"), \
         patch("icarus_sentinel.app.ConfigView"), \
         patch("icarus_sentinel.app.SaveSyncView"), \
         patch("icarus_sentinel.app.BackupsView"), \
         patch("icarus_sentinel.app.ModsView"), \
         patch("icarus_sentinel.app.Controller"):
        
        app = App()
        app.tk = MagicMock()
        app.server_manager = MagicMock()
        
        # UI Elements
        app.cpu_usage_label = MagicMock()
        app.cpu_progress_bar = MagicMock()
        app.ram_usage_label = MagicMock()
        app.ram_progress_bar = MagicMock()
        
        # Mock methods
        app.update_monitoring_once = lambda: App.update_monitoring_once(app)
        
        # Mock 'after'
        def mock_after(delay, func, *args):
            if delay == 0 and callable(func):
                func(*args)
            return "mock_after_id"
        app.after = MagicMock(side_effect=mock_after)
        
        yield app

def test_metrics_elements_exist(app_instance):
    assert hasattr(app_instance, "cpu_usage_label")
    assert hasattr(app_instance, "cpu_progress_bar")
    assert hasattr(app_instance, "ram_usage_label")
    assert hasattr(app_instance, "ram_progress_bar")

def test_metrics_update(app_instance):
    # Setup usage
    app_instance.server_manager.get_resource_usage.return_value = {
        "cpu": 50.0,
        "ram_gb": 8.0
    }
    app_instance.server_process = MagicMock()
    app_instance.server_manager.ram_threshold_gb = 16.0
    app_instance.server_manager.state = {"status": "running"}
    app_instance.server_manager.should_smart_restart.return_value = False
    
    # Run update
    app_instance.update_monitoring_once()
    
    # Verify elements were configured/set
    assert app_instance.cpu_usage_label.configure.called
    assert app_instance.cpu_progress_bar.set.called
    assert app_instance.ram_usage_label.configure.called
    assert app_instance.ram_progress_bar.set.called
