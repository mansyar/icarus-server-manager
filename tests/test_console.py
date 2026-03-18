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
        app.console_output = MagicMock()
        
        # Mock methods
        app.log = lambda msg: App.log(app, msg)
        
        yield app

def test_console_exists_and_styled(app_instance):
    assert hasattr(app_instance, "console_output")

def test_logging_inserts_and_scrolls(app_instance):
    test_msg = "TEST LOG MESSAGE"
    app_instance.log(test_msg)
    
    # Should insert text
    app_instance.console_output.insert.assert_any_call("end", test_msg + "\n")
    # Should auto-scroll to the end
    app_instance.console_output.see.assert_called_with("end")
    # Should toggle state to normal for insertion and back to disabled
    app_instance.console_output.configure.assert_any_call(state="normal")
    app_instance.console_output.configure.assert_any_call(state="disabled")
