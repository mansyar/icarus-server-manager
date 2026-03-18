import sys
from unittest.mock import MagicMock, patch

# Top-level mock to prevent Tcl/Tk issues
mock_ctk = MagicMock()
class MockCTkBase:
    def __init__(self, *args, **kwargs): self.tk = MagicMock()
    def grid_columnconfigure(self, *args, **kwargs): pass
    def grid_rowconfigure(self, *args, **kwargs): pass
    def configure(self, *args, **kwargs): pass
    def title(self, *args, **kwargs): pass
    def geometry(self, *args, **kwargs): pass
    def after(self, ms, func, *args): 
        if ms == 0: func(*args)
    def cget(self, param): return None

mock_ctk.CTk = MockCTkBase

def create_mock_comp(*args, **kwargs):
    m = MagicMock()
    m.grid = MagicMock()
    m.pack = MagicMock()
    m.configure = MagicMock()
    m.insert = MagicMock()
    m.see = MagicMock()
    # Store kwargs for later inspection if needed
    m._mock_kwargs = kwargs
    return m

mock_ctk.CTkFrame = create_mock_comp
mock_ctk.CTkTextbox = create_mock_comp
mock_ctk.CTkTabview = create_mock_comp
mock_ctk.CTkButton = create_mock_comp
mock_ctk.CTkLabel = create_mock_comp
mock_ctk.CTkProgressBar = create_mock_comp
mock_ctk.CTkScrollableFrame = create_mock_comp
mock_ctk.CTkEntry = create_mock_comp
mock_ctk.CTkSwitch = create_mock_comp
mock_ctk.CTkOptionMenu = create_mock_comp
mock_ctk.CTkCheckBox = create_mock_comp

mock_ctk.StringVar.return_value = MagicMock()
mock_ctk.BooleanVar.return_value = MagicMock()

sys.modules["customtkinter"] = mock_ctk

import pytest
from icarus_sentinel.app import App
from icarus_sentinel import style_config

@pytest.fixture
def app_instance():
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
    # Verify console is in the main content frame
    # In our implementation, it's grid(row=1, column=0) in main_content_frame

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
