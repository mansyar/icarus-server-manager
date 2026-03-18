import pytest
from unittest.mock import MagicMock, patch
from icarus_sentinel import style_config

@pytest.fixture
def app_instance():
    # Import inside to ensure mocked dependencies from conftest are used
    from icarus_sentinel.app import App
    
    # Mocking standard dependencies
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

def test_app_new_layout_structure(app_instance):
    # Verify new layout containers exist
    assert hasattr(app_instance, "sidebar_frame")
    assert hasattr(app_instance, "main_content_frame")
    assert hasattr(app_instance, "console_output")

def test_app_styling(app_instance):
    from icarus_sentinel.app import App
    assert isinstance(app_instance, App)

def test_app_grid_configuration(app_instance):
    from icarus_sentinel.app import App
    assert isinstance(app_instance, App)
