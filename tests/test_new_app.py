import pytest
from unittest.mock import MagicMock, patch
import customtkinter as ctk
from icarus_sentinel.app import App
from icarus_sentinel import style_config
from contextlib import ExitStack

@pytest.fixture
def app_instance():
    with ExitStack() as stack:
        # Mocking standard dependencies
        stack.enter_context(patch("icarus_sentinel.app.SteamManager"))
        mock_spm = stack.enter_context(patch("icarus_sentinel.app.ServerProcessManager"))
        mock_bm = stack.enter_context(patch("icarus_sentinel.app.BackupManager"))
        stack.enter_context(patch("icarus_sentinel.app.INIManager"))
        mock_ssm = stack.enter_context(patch("icarus_sentinel.app.SaveSyncManager"))
        stack.enter_context(patch("icarus_sentinel.app.ModManager"))
        stack.enter_context(patch("icarus_sentinel.app.App.recover_state"))
        stack.enter_context(patch("icarus_sentinel.app.App.update_monitoring"))
        
        # Mocking CTk to avoid Tcl issues
        stack.enter_context(patch("customtkinter.CTk.__init__", return_value=None))
        stack.enter_context(patch("customtkinter.CTk.grid"))
        stack.enter_context(patch("customtkinter.CTk.grid_columnconfigure"))
        stack.enter_context(patch("customtkinter.CTk.grid_rowconfigure"))
        stack.enter_context(patch("customtkinter.CTk.configure"))
        stack.enter_context(patch("customtkinter.CTk.cget"))
        stack.enter_context(patch("customtkinter.CTk.title"))
        stack.enter_context(patch("customtkinter.CTk.geometry"))
        stack.enter_context(patch("customtkinter.CTk.after"))
        
        # Mocking components
        mock_frame = stack.enter_context(patch("customtkinter.CTkFrame"))
        mock_scroll_frame = stack.enter_context(patch("customtkinter.CTkScrollableFrame"))
        mock_textbox = stack.enter_context(patch("customtkinter.CTkTextbox"))
        mock_tabview = stack.enter_context(patch("customtkinter.CTkTabview"))
        stack.enter_context(patch("customtkinter.CTkButton"))
        stack.enter_context(patch("customtkinter.CTkLabel"))
        stack.enter_context(patch("customtkinter.CTkEntry"))
        stack.enter_context(patch("customtkinter.CTkSwitch"))
        stack.enter_context(patch("customtkinter.CTkOptionMenu"))
        stack.enter_context(patch("customtkinter.CTkCheckBox"))
        stack.enter_context(patch("customtkinter.BooleanVar"))
        stack.enter_context(patch("customtkinter.StringVar"))
        stack.enter_context(patch("customtkinter.IntVar"))
        stack.enter_context(patch("customtkinter.DoubleVar"))
        
        # Mocking OS calls
        stack.enter_context(patch("os.makedirs"))
        stack.enter_context(patch("os.path.exists", return_value=True))
        stack.enter_context(patch("os.listdir", return_value=[]))

        # Configure mocks
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

        def create_mock_component(master=None, **kwargs):
            m = MagicMock()
            m.cget.side_effect = lambda p: kwargs.get(p)
            return m

        mock_frame.side_effect = create_mock_component
        mock_scroll_frame.side_effect = create_mock_component
        mock_textbox.side_effect = create_mock_component
        mock_tabview.side_effect = create_mock_component

        original_init = App.__init__
        def patched_init(self, *args, **kwargs):
            self.tk = MagicMock()
            original_init(self, *args, **kwargs)

        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=[]), \
             patch.object(App, "__init__", patched_init):
            app = App()
            app.cget = lambda p: style_config.APP_BG if p == "fg_color" else None
            yield app

def test_app_new_layout_structure(app_instance):
    assert hasattr(app_instance, "sidebar_frame")
    assert hasattr(app_instance, "main_content_frame")
    assert hasattr(app_instance, "console_output")
    
    assert isinstance(app_instance.sidebar_frame, MagicMock)
    assert isinstance(app_instance.main_content_frame, MagicMock)
    assert isinstance(app_instance.console_output, MagicMock)

def test_app_styling(app_instance):
    assert app_instance.cget("fg_color") == style_config.APP_BG
    assert app_instance.sidebar_frame.cget("fg_color") == style_config.SIDEBAR_BG
    assert app_instance.console_output.cget("fg_color") == style_config.CONSOLE_BG
    assert app_instance.console_output.cget("text_color") == style_config.CONSOLE_TEXT

def test_app_grid_configuration(app_instance):
    # We can check calls to grid_columnconfigure
    # app.grid_columnconfigure(0, weight=0)
    # app.grid_columnconfigure(1, weight=1)
    
    # Since we mocked grid_columnconfigure on the CTk class, 
    # we need to check how it was called on the instance.
    # Note: mocking CTk.grid_columnconfigure means app.grid_columnconfigure is a mock.
    
    calls = app_instance.grid_columnconfigure.call_args_list
    # Find call for col 0 and col 1
    col0_call = next(c for c in calls if c[0][0] == 0)
    col1_call = next(c for c in calls if c[0][0] == 1)
    
    assert col0_call[1]["weight"] == 0
    assert col1_call[1]["weight"] == 1
