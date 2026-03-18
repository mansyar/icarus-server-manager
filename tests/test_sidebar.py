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

def test_sidebar_buttons_exist(app_instance):
    assert hasattr(app_instance, "nav_dashboard_btn")
    assert hasattr(app_instance, "nav_settings_btn")
    assert hasattr(app_instance, "nav_backups_btn")
    assert hasattr(app_instance, "nav_mods_btn")
    assert hasattr(app_instance, "nav_sync_btn")

def test_sidebar_branding(app_instance):
    assert hasattr(app_instance, "sidebar_logo_label")

def test_sidebar_navigation_interaction(app_instance):
    assert app_instance.server_view.grid.called
    
    app_instance.nav_settings_btn.invoke()
    assert app_instance.config_view.grid.called
    assert app_instance.server_view.grid_forget.called
