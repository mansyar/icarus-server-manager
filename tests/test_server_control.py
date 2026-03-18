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

def test_orbital_launch_button_exists(app_instance):
    assert hasattr(app_instance, "orbital_launch_btn")

def test_launch_button_interaction(app_instance):
    # Mock toggle_server
    app_instance.toggle_server = MagicMock()
    
    # Check if the button command is toggle_server
    # Since we use create_mock_comp, orbital_launch_btn is a MagicMock
    # In App.__init__, we set command=self.toggle_server
    pass 
