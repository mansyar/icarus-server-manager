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

def test_console_exists_and_styled(app_instance):
    assert hasattr(app_instance, "console_output")

def test_logging_inserts_and_scrolls(app_instance):
    # Mock the console_output to verify behavior
    app_instance.console_output = MagicMock()
    
    test_msg = "TEST LOG MESSAGE"
    app_instance.log(test_msg)
    
    # Should insert text
    app_instance.console_output.insert.assert_any_call("end", test_msg + "\n")
    # Should auto-scroll to the end
    app_instance.console_output.see.assert_called_with("end")
    # Should toggle state to normal for insertion and back to disabled
    app_instance.console_output.configure.assert_any_call(state="normal")
    app_instance.console_output.configure.assert_any_call(state="disabled")
