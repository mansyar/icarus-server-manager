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
        
        mock_spm_inst = mock_spm.return_value
        mock_spm_inst.smart_restart_enabled = False
        mock_spm_inst.smart_restart_time = "00:00"
        mock_spm_inst.ram_threshold_gb = 16.0
        mock_spm_inst.state = {"status": "stopped"}
        
        mock_bm_inst = mock_bm.return_value
        mock_bm_inst.interval_minutes = 30.0
        mock_bm_inst.retention_limit = 10
        mock_bm_inst.backup_path = "C:/mock_backups"
        
        mock_ssm_inst = mock_ssm.return_value
        mock_ssm_inst.list_local_steam_ids.return_value = []

        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=[]):
            app = App()
            yield app

def test_app_grid_weights(app_instance):
    # Main window weights
    app_instance.grid_columnconfigure.assert_any_call(0, weight=0)
    app_instance.grid_columnconfigure.assert_any_call(1, weight=1)
    
    # main_content_frame weights
    app_instance.main_content_frame.grid_rowconfigure.assert_any_call(0, weight=1)
    app_instance.main_content_frame.grid_rowconfigure.assert_any_call(1, weight=0)

def test_server_view_responsiveness(app_instance):
    app_instance.metrics_frame.grid_columnconfigure.assert_any_call(0, weight=1)
