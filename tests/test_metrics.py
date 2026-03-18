import pytest
from unittest.mock import MagicMock, patch
from icarus_sentinel import style_config

@pytest.fixture
def app_instance():
    from icarus_sentinel.app import App
    with patch("icarus_sentinel.app.SteamManager"), \
         patch("icarus_sentinel.app.ServerProcessManager") as mock_spm, \
         patch("icarus_sentinel.app.BackupManager") as mock_bm, \
         patch("icarus_sentinel.app.INIManager"), \
         patch("icarus_sentinel.app.SaveSyncManager") as mock_ssm, \
         patch("icarus_sentinel.app.ModManager"), \
         patch("icarus_sentinel.app.App.recover_state"), \
         patch("icarus_sentinel.app.App.update_monitoring"), \
         patch("os.makedirs"):
        
        mock_ssm_inst = mock_ssm.return_value
        mock_ssm_inst.list_local_steam_ids.return_value = []

        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=[]):
            app = App()
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
    
    # Run update
    app_instance.update_monitoring_once()
    
    # Verify elements were configured/set
    assert app_instance.cpu_usage_label.configure.called
    assert app_instance.cpu_progress_bar.set.called
    assert app_instance.ram_usage_label.configure.called
    assert app_instance.ram_progress_bar.set.called
