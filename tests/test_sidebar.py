import pytest
from unittest.mock import MagicMock, patch
import customtkinter as ctk
from icarus_sentinel.app import App
from icarus_sentinel import style_config
from contextlib import ExitStack

@pytest.fixture
def app_instance():
    with ExitStack() as stack:
        stack.enter_context(patch("icarus_sentinel.app.SteamManager"))
        mock_spm = stack.enter_context(patch("icarus_sentinel.app.ServerProcessManager"))
        mock_bm = stack.enter_context(patch("icarus_sentinel.app.BackupManager"))
        stack.enter_context(patch("icarus_sentinel.app.INIManager"))
        mock_ssm = stack.enter_context(patch("icarus_sentinel.app.SaveSyncManager"))
        stack.enter_context(patch("icarus_sentinel.app.ModManager"))
        stack.enter_context(patch("icarus_sentinel.app.App.recover_state"))
        stack.enter_context(patch("icarus_sentinel.app.App.update_monitoring"))
        
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
        def create_mock_btn(master=None, **kwargs):
            m = MagicMock()
            m.invoke.side_effect = kwargs.get("command")
            return m

        stack.enter_context(patch("customtkinter.CTkFrame"))
        stack.enter_context(patch("customtkinter.CTkScrollableFrame"))
        stack.enter_context(patch("customtkinter.CTkTextbox"))
        stack.enter_context(patch("customtkinter.CTkTabview"))
        mock_btn = stack.enter_context(patch("customtkinter.CTkButton"))
        mock_btn.side_effect = create_mock_btn
        stack.enter_context(patch("customtkinter.CTkLabel"))
        stack.enter_context(patch("customtkinter.CTkEntry"))
        stack.enter_context(patch("customtkinter.CTkSwitch"))
        stack.enter_context(patch("customtkinter.CTkOptionMenu"))
        stack.enter_context(patch("customtkinter.CTkCheckBox"))
        stack.enter_context(patch("customtkinter.BooleanVar"))
        stack.enter_context(patch("customtkinter.StringVar"))

        # os mocks
        stack.enter_context(patch("os.makedirs"))
        stack.enter_context(patch("os.path.exists", return_value=True))
        stack.enter_context(patch("os.listdir", return_value=[]))

        mock_spm_inst = mock_spm.return_value
        mock_spm_inst.state = {"status": "stopped"}
        
        mock_bm_inst = mock_bm.return_value
        mock_bm_inst.backup_path = "C:/mock_backups"

        original_init = App.__init__
        def patched_init(self, *args, **kwargs):
            self.tk = MagicMock()
            original_init(self, *args, **kwargs)

        with patch.object(App, "__init__", patched_init):
            app = App()
            yield app

def test_sidebar_buttons_exist(app_instance):
    # Check for core navigation buttons
    assert hasattr(app_instance, "nav_dashboard_btn")
    assert hasattr(app_instance, "nav_settings_btn")
    assert hasattr(app_instance, "nav_backups_btn")
    assert hasattr(app_instance, "nav_mods_btn")

def test_sidebar_branding(app_instance):
    # Sidebar should have a title or logo label
    assert hasattr(app_instance, "sidebar_logo_label")

def test_sidebar_navigation_interaction(app_instance):
    # Mock tabview set method
    app_instance.tabview.set = MagicMock()
    
    # Test Dashboard button
    app_instance.nav_dashboard_btn.invoke()
    app_instance.tabview.set.assert_called_with("Server")
    
    # Test Settings button
    app_instance.nav_settings_btn.invoke()
    app_instance.tabview.set.assert_called_with("Configuration")
