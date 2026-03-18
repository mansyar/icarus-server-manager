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
         patch.object(App, "toggle_server"), \
         patch("os.makedirs"):
        
        mock_ssm_inst = mock_ssm.return_value
        mock_ssm_inst.list_local_steam_ids.return_value = []

        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=[]):
            app = App()
            yield app

def test_orbital_launch_button_exists(app_instance):
    assert hasattr(app_instance, "orbital_launch_btn")

def test_launch_button_interaction(app_instance):
    # In App.__init__, we set command=self.toggle_server
    # Since we patched App.toggle_server, app_instance.toggle_server is a Mock
    app_instance.orbital_launch_btn.invoke()
    app_instance.toggle_server.assert_called_once()
